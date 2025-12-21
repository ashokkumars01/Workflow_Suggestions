import os
import sys
import json
import logging
from datetime import datetime
from typing import List, Dict


# ---------------------------
# Logging Configuration
# ---------------------------
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


# ---------------------------
# Utility Functions
# ---------------------------
def load_data(file_path: str) -> List[Dict]:
    """
    Load JSON data from a file.
    """
    logger.info(f"Loading data from {file_path}")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def process_data(data: List[Dict]) -> Dict:
    """
    Perform basic analytics on input data.
    """
    logger.info("Processing data")

    total_records = len(data)
    active_records = sum(1 for item in data if item.get("active", False))

    return {
        "total_records": total_records,
        "active_records": active_records,
        "inactive_records": total_records - active_records,
        "processed_at": datetime.utcnow().isoformat() + "Z",
    }


def save_report(report: Dict, output_path: str) -> None:
    """
    Save processed report as JSON.
    """
    logger.info(f"Saving report to {output_path}")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)


# ---------------------------
# Main Execution
# ---------------------------
def main() -> None:
    """
    Main entry point for CI/CD execution.
    """

    logger.info("Starting GitHub Actions Python job")

    # Read config from environment variables
    input_file = os.getenv("INPUT_FILE", "data.json")
    output_file = os.getenv("OUTPUT_FILE", "report.json")

    try:
        data = load_dat(input_file)
        report = process_data(data)
        save_report(report, output_file)

        logger.info("Job completed successfully")
        logger.info(f"Summary: {report}")

    except Exception as exc:
        logger.error("Job failed", exc_info=True)
        sys.exit(1)  # ❌ Important for GitHub Actions (marks workflow as failed)

    sys.exit(0)  # ✅ Success


if __name__ == "__main__":
    main()
