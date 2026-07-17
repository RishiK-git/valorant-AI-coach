import glob
import os


def select_frames(frames_dir: str, max_frames: int = None) -> list[str]:
    """
    Selects which extracted frames to send for analysis.
    Currently: returns all frames sorted in order (optionally capped).
    Future: can filter down to only "significant event" frames here.
    """
    frame_paths = sorted(glob.glob(os.path.join(frames_dir, "*.png")))
    if max_frames:
        frame_paths = frame_paths[:max_frames]
    return frame_paths