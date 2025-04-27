import argparse
import os


def get_config():
    parser = argparse.ArgumentParser(description="Reverse Shell Detector")
    parser.add_argument(
        "--interval", type=int, default=10, help="Scan interval in seconds"
    )
    parser.add_argument(
        "--logfile", type=str, help="Path to log file", default="./revlogs.log"
    )
    parser.add_argument("--dry-run", action="store_true", help="Detect but do not kill")
    parser.add_argument(
        "--metrics",
        action="store_true",
        help="Use prometheus client to collect metrics",
        default=False,
    )

    # LLM configuration
    parser.add_argument("--use-llm", action="store_true", help="Use LLM for analysis")
    parser.add_argument(
        "--gemini-key",
        type=str,
        help="Google Gemini API key (overrides environment variable)",
    )

    args = parser.parse_args()

    # Set API key from argument if provided, otherwise use environment variable
    if args.gemini_key:
        os.environ["GEMINI_API_KEY"] = args.gemini_key

    return args
