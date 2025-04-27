import os
import time
import threading

from dotenv import load_dotenv

from revshell_detector.config import get_config
from revshell_detector.logger import setup_logger
from revshell_detector.metrics import MetricsCollector
from revshell_detector.process_arg_detector import scan_processes


def main():
    load_dotenv()
    args = get_config()
    logger = setup_logger(args.logfile)

    logger.info("Reverse Shell Detector started.")
    if args.interval:
        logger.info(f"The interval is: {args.interval}")

    if args.use_llm:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            logger.warning(
                "LLM analysis enabled but no API key found. Using pattern-based detection only."
            )
        else:
            logger.info("LLM-based detection enabled.")
    else:
        api_key = None

    # Setup metrics collection
    if args.metrics:
        metrics = MetricsCollector()
        t = threading.Thread(target=metrics.update_resource_usage)
        t.daemon = True
        t.start()
        logger.info("Collecting Metrics.")
    else:
        metrics = None

    while True:
        try:
            scan_processes(
                logger,
                dry_run=args.dry_run,
                use_llm=args.use_llm,
                metrics=metrics,
                api_key=api_key,
            )
            time.sleep(args.interval)
        except Exception as e:
            logger.error(f"Error during scan: {str(e)}")
            time.sleep(args.interval)


if __name__ == "__main__":
    main()
