import os
import re
from typing import Optional

import psutil

from .metrics import MetricsCollector

from .email_notifier import send_email_notification
from .llm_detector import analyze_with_llm

SUSPICIOUS_CMDS = [
    re.compile(r"bash -i"),
    re.compile(r"/dev/tcp"),
    re.compile(r"nc "),
    re.compile(r"netcat "),
    re.compile(r"ncat "),
    re.compile(r"socat "),
    re.compile(r'python -c ".*socket.*connect'),
    re.compile(r"python -c '.*socket.*connect"),
    re.compile(r"python -c '.*socket.*s\.connect"),
    re.compile(r"python -c '.*pty\.spawn"),
    re.compile(r"python -c '.*os\.dup2"),
    re.compile(r"export R(HOST|PORT).*python -c"),
    re.compile(r"perl -e '.*socket"),
    re.compile(r"sh -i"),
    re.compile(r"0>&1"),
    re.compile(r"1>&2"),
    re.compile(r"os\.dup2.*\(0,1,2\)"),
    re.compile(r"awk.*BEGIN.*tcp"),
    re.compile(r"bash.*dev/(tcp|udp)"),
    re.compile(r"bash.*dev/(tcp|udp).*exec"),
    re.compile(r"lua.*socket\.connect"),
    re.compile(r"ruby.*socket\.open"),
    re.compile(r"ruby.*rsocket.*TCPSocket"),
    re.compile(r"telnet.*exec"),
    re.compile(r"php.*fsockopen"),
    re.compile(r"php.*stream_socket_client"),
    re.compile(r"openssl.*s_client"),
    re.compile(r"socat.*stdio.*tcp"),
    re.compile(r"socat.*exec"),
    re.compile(r"node.*net\.connect"),
    re.compile(r"node.*child_process"),
    re.compile(r"java.*runtime\.exec"),
    re.compile(r"java.*socket"),
    re.compile(r"groovy.*socket"),
    re.compile(r"rust.*TcpStream"),
    re.compile(r"golang.*net\.Dial"),
    re.compile(r"perl.*IO::Socket"),
    re.compile(r"ognl.*runtime\.exec"),
    re.compile(r"/bin/(ba|)sh\s+-i"),
    re.compile(r"mknod.*[^/]+\s+p"),
    re.compile(r"-e /bin/(ba|)sh"),
    re.compile(r"subprocess\.call\(.*/bin/"),
    re.compile(r"[;|]\s*bash"),
    re.compile(r"python\s+-c\s+.*import\s+os"),
    re.compile(r"python\s+-c\s+.*subprocess"),
    re.compile(r"\w+\s*=\s*socket\("),
    re.compile(r"exec\s*/bin/(ba|)sh"),
    re.compile(r"\[\s*os\.dup2\s*\(.*for\s+fd\s+in"),
    re.compile(r"base64\s*-d.*bash"),
    re.compile(r"wget.*bash"),
    re.compile(r"curl.*bash"),
]

WHITE_LIST = ["/usr/bin/zsh -i"]

BENIGN_APPS = [
    re.compile(r"/snap/.*/brave/brave"),
    re.compile(r"/snap/.*/code"),
    re.compile(r"zed.app/libexec/zed-editor"),
    re.compile(r"network\.mojom\.NetworkService"),
    re.compile(r"node\.mojom\.NodeService"),
    re.compile(r"intellicode-api-usage-examples"),
    re.compile(r"microsoft\.com"),
    re.compile(r"intellisense"),
    re.compile(r"vscode"),
    re.compile(r"visualstudio"),
]


def is_benign_application(cmdline):
    """Check if this is a known benign application"""
    joined = " ".join(cmdline)
    for pattern in BENIGN_APPS:
        if pattern.search(joined):
            return True
    return False


def looks_like_reverse_shell(cmdline):
    joined = " ".join(cmdline).lower()
    if any(pattern.search(joined) for pattern in SUSPICIOUS_CMDS):
        if is_benign_application(cmdline):
            return False
        return True
    return False


def has_suspicious_connection(pid):
    """
    More nuanced check for suspicious connections that excludes common ports
    """
    try:
        p = psutil.Process(pid)

        try:
            cmdline = p.cmdline()

            if is_benign_application(cmdline):
                return False
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            pass

        safe_ports = {80, 443, 8080, 8443, 22, 53}

        for conn in p.net_connections(kind="inet"):
            if conn.status == psutil.CONN_ESTABLISHED and conn.raddr:
                # If connecting to a common legitimate port, less likely to be suspicious
                if conn.raddr.port in safe_ports:
                    continue

                # If connection is to a local address, less suspicious
                if (
                    conn.raddr.ip.startswith("127.")
                    or conn.raddr.ip.startswith("10.")
                    or conn.raddr.ip.startswith("192.168.")
                ):
                    continue

                return True
    except Exception:
        pass
    return False


marked_unsuspicious = []


def scan_processes(
    logger,
    dry_run=False,
    use_llm=True,
    metrics: Optional[MetricsCollector] = None,
    api_key: Optional[str] = None,
):
    for proc in psutil.process_iter(["pid", "cmdline"]):
        try:
            pid = proc.info["pid"]
            cmdline = proc.info["cmdline"]

            # Skip empty cmdline, already marked unsuspecious processes, white listed command, or known benign applications
            if (
                pid in marked_unsuspicious
                or not cmdline
                or " ".join(cmdline) in WHITE_LIST
                or is_benign_application(cmdline)
            ):
                continue

            is_suspicious = looks_like_reverse_shell(
                cmdline
            ) or has_suspicious_connection(pid)

            if is_suspicious and use_llm:
                # Analyze with LLM and get full result
                llm_result = analyze_with_llm(cmdline, pid, logger, api_key)

                # Determine if it's suspicious based on the result
                is_suspicious = (
                    llm_result
                    and llm_result.is_reverse_shell
                    and llm_result.confidence >= 0.7
                )

                # Send email if confirmed as suspicious and update detected counter
                if is_suspicious and llm_result:
                    if metrics:
                        metrics.detections_total.inc()
                    send_email_notification(pid, cmdline, llm_result.confidence)
                    logger.warning(
                        f"LLM confirmed PID {pid} as a reverse shell with {llm_result.confidence:.2f} confidence"
                    )
                else:
                    if metrics:
                        metrics.false_positive_total.inc()
                    marked_unsuspicious.append(pid)
                    logger.info(
                        f"LLM cleared PID {pid} that was initially flagged as suspicious"
                    )

            if is_suspicious:
                logger.warning(f"Suspicious PID {pid}: {' '.join(cmdline)}")
                if not dry_run:
                    os.kill(pid, 9)
                    logger.info(f"Killed PID {pid}")

                    # Send a notification even if LLM wasn't used
                    if not use_llm:
                        send_email_notification(pid, cmdline, None)

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
