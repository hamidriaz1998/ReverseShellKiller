import logging


def setup_logger(logfile=None):
    logger = logging.getLogger("revshell_detector")
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(logfile) if logfile else logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
