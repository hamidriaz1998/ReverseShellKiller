import logging
import logging.handlers
import os


def setup_logger(logfile=None, debug=False):
    logger = logging.getLogger("revshell_detector")

    # Clear existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Set log level
    level = logging.DEBUG if debug else logging.INFO
    logger.setLevel(level)

    # Create formatters
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")

    # Always add file handler if logfile is specified
    if logfile:
        # Make sure directory exists
        log_dir = os.path.dirname(logfile)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Use rotating file handler to prevent huge log files
        file_handler = logging.handlers.RotatingFileHandler(
            logfile, maxBytes=10 * 1024 * 1024, backupCount=5
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
