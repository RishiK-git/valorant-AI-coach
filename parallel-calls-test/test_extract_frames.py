import sys
from pathlib import Path

# Make the project root importable regardless of where this script is run from
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from pipeline.extract_frames import extract_frames_every_n_seconds

VIDEO_PATH = PROJECT_ROOT / "skye-clip1.mp4"
FRAMES_DIR = PROJECT_ROOT / "test-frames"

if __name__ == "__main__":
    extract_frames_every_n_seconds(
        video_path=str(VIDEO_PATH),
        output_dir=str(FRAMES_DIR),
        interval_sec=0.25,
    )