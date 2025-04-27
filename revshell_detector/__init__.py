# reverse_shell_killer/revshell_detector/__init__.py
from .config import get_config
from .logger import setup_logger
from .process_arg_detector import scan_processes
from .llm_detector import analyze_with_llm, is_reverse_shell_by_llm
from .email_notifier import send_email_notification

__all__ = [
    "get_config",
    "setup_logger",
    "scan_processes",
    "analyze_with_llm",
    "is_reverse_shell_by_llm",
    "send_email_notification",
]
