from revshell_detector.config import get_config
from revshell_detector.logger import setup_logger
from revshell_detector.process_arg_detector import scan_processes
from dotenv import load_dotenv
import time
import os


def main():
    load_dotenv()
    args = get_config()
    logger = setup_logger(args.logfile)

    logger.info("Reverse Shell Detector started.")

    if args.use_llm:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            logger.warning(
                "LLM analysis enabled but no API key found. Using pattern-based detection only."
            )
        else:
            logger.info("LLM-based detection enabled.")

    while True:
        scan_processes(logger, dry_run=args.dry_run, use_llm=args.use_llm)
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
