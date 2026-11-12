"""Check a deployed URL and write every attempt to logs/health_check.log."""

import argparse
import logging
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

LOG_FILE = Path(__file__).resolve().parents[1] / "logs" / "health_check.log"


def configure_logger():
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("devops-health")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    for handler in (logging.FileHandler(LOG_FILE, encoding="utf-8"), logging.StreamHandler(sys.stdout)):
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


def check(url: str, retries: int, delay: float) -> bool:
    logger = configure_logger()
    for attempt in range(1, retries + 1):
        try:
            with urlopen(url, timeout=10) as response:
                status = response.status
            if status == 200:
                logger.info("HEALTHY url=%s status=%s attempt=%s", url, status, attempt)
                return True
            logger.error("UNHEALTHY url=%s status=%s attempt=%s", url, status, attempt)
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            logger.error("UNHEALTHY url=%s attempt=%s error=%s", url, attempt, exc)
        if attempt < retries:
            time.sleep(delay)
    logger.error("Health check FAILED after %s attempts", retries)
    return False


def main():
    parser = argparse.ArgumentParser(description="HTTP health check that logs its results")
    parser.add_argument("url", help="Full /health URL")
    parser.add_argument("--retries", type=int, default=5)
    parser.add_argument("--delay", type=float, default=3)
    args = parser.parse_args()
    if args.retries < 1 or args.delay < 0:
        parser.error("--retries must be >= 1 and --delay must be >= 0")
    sys.exit(0 if check(args.url, args.retries, args.delay) else 1)


if __name__ == "__main__":
    main()
