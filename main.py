from revshell_detector.config import get_config
from revshell_detector.logger import setup_logger
from revshell_detector.core import scan_processes
import time


def main():
    args = get_config()
    logger = setup_logger(args.logfile)

    logger.info("Reverse Shell Detector started.")
    while True:
        scan_processes(logger, dry_run=args.dry_run)
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
