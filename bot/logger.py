from pathlib import Path

from loguru import logger

log_dir = Path(__file__).resolve().parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

logger.add(log_dir / "tghunter.log", rotation="1 MB", retention="10 days", enqueue=True)
