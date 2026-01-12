import time
from pathlib import Path

MAX_AGE = 24 * 60 * 60  # 24 hours


def cleanup_old_outputs(output_dir: Path):
    now = time.time()

    for path in output_dir.glob("*"):
        if path.is_file():
            if now - path.stat().st_mtime > MAX_AGE:
                path.unlink()
