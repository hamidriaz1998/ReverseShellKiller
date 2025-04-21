import psutil
import os
import re
from .llm_detector import is_reverse_shell_by_llm

SUSPICIOUS_CMDS = [
    "bash -i",
    "/dev/tcp",
    "nc ",  
    "netcat ",
    "ncat ", 
    "socat ",
    "python -c \".*socket.*connect",  
    "perl -e '.*socket",  
    "sh -i",
    "0>&1",
    "1>&2",
]

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
    if any(pattern in joined for pattern in SUSPICIOUS_CMDS):
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
            proc_name = p.name()
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
                if conn.raddr.ip.startswith('127.') or conn.raddr.ip.startswith('10.') or conn.raddr.ip.startswith('192.168.'):
                    continue
                    
                return True
    except Exception:
        pass
    return False


def scan_processes(logger, dry_run=False, use_llm=True):
    for proc in psutil.process_iter(["pid", "cmdline"]):
        try:
            pid = proc.info["pid"]
            cmdline = proc.info["cmdline"]
            
            if not cmdline:
                continue
                
            if is_benign_application(cmdline):
                continue
                
            is_suspicious = looks_like_reverse_shell(cmdline) or has_suspicious_connection(pid)
            
            if is_suspicious and use_llm:
                # Only kill if the LLM also confirms it's a reverse shell
                is_suspicious = is_reverse_shell_by_llm(cmdline, pid, logger)
                if not is_suspicious:
                    logger.info(f"LLM cleared PID {pid} that was initially flagged as suspicious")
            
            if is_suspicious:
                logger.warning(f"Suspicious PID {pid}: {' '.join(cmdline)}")
                if not dry_run:
                    os.kill(pid, 9)
                    logger.info(f"Killed PID {pid}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
