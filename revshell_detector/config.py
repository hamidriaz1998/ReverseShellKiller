import argparse


def get_config():
    parser = argparse.ArgumentParser(description="Reverse Shell Detector")
    parser.add_argument(
        "--interval", type=int, default=10, help="Scan interval in seconds"
    )
    parser.add_argument("--logfile", type=str, help="Path to log file")
    parser.add_argument("--dry-run", action="store_true", help="Detect but do not kill")
    return parser.parse_args()
