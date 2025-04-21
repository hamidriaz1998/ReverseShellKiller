import psutil
import os

SUSPICIOUS_CMDS = [
    "bash -i",
    "/dev/tcp",
    "nc ",
    "netcat",
    "ncat",
    "socat",
    "python -c",
    "perl -e",
    "sh -i",
    "0>&1",
    "1>&2",
]


def looks_like_reverse_shell(cmdline):
    joined = " ".join(cmdline).lower()
    return any(pattern in joined for pattern in SUSPICIOUS_CMDS)


def has_suspicious_connection(pid):
    try:
        p = psutil.Process(pid)
        for conn in p.connections(kind="inet"):
            if conn.status == psutil.CONN_ESTABLISHED and conn.raddr:
                return True
    except Exception:
        pass
    return False


def scan_processes(logger, dry_run=False):
    for proc in psutil.process_iter(["pid", "cmdline"]):
        try:
            pid = proc.info["pid"]
            cmdline = proc.info["cmdline"]
            if not cmdline:
                continue

            if looks_like_reverse_shell(cmdline) or has_suspicious_connection(pid):
                logger.warning(f"Suspicious PID {pid}: {' '.join(cmdline)}")
                if not dry_run:
                    os.kill(pid, 9)
                    logger.info(f"Killed PID {pid}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
