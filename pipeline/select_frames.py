import glob
import os
import re


def select_frames(frames_dir: str, interval_sec: float = 2.0, max_frames: int = None) -> list[dict]:
    """
    Selects which extracted frames to send for analysis.
    Returns a list of {"path": ..., "timestamp": "MM:SS"} dicts, in order.
    """
    frame_paths = sorted(glob.glob(os.path.join(frames_dir, "*.png")))
    if max_frames:
        frame_paths = frame_paths[:max_frames]

    frames = []
    for path in frame_paths:
        match = re.search(r"frame_(\d+)\.png", os.path.basename(path))
        frame_index = int(match.group(1)) - 1  # frame_00001 -> index 0
        seconds = frame_index * interval_sec

        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        timestamp = f"{minutes:02d}:{secs:02d}"

        frames.append({"path": path, "timestamp": timestamp})

    return frames