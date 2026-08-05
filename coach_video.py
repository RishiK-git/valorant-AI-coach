import shutil
import tempfile

from pipeline.extract_frames import extract_frames_every_n_seconds
from pipeline.select_frames import select_frames
from pipeline.select_frames_with_enemy_boost import select_frames_with_enemy_boost
from pipeline.analyze_frames import analyze_frames
from pipeline.report import SYSTEM_PROMPT, CoachingReport


def coach_video(video_path: str, interval_sec: float = 2.0, max_frames: int = None) -> dict:
    """
    End-to-end pipeline: video in, structured coaching report out.
    """
    frames_dir = tempfile.mkdtemp(prefix="coach_frames_")

    try:
        extract_frames_every_n_seconds(video_path, frames_dir, interval_sec=interval_sec)
        frames = select_frames(frames_dir, interval_sec=interval_sec, max_frames=max_frames)
        report = analyze_frames(frames, SYSTEM_PROMPT, response_schema=CoachingReport)
        return report.model_dump()

    finally:
        shutil.rmtree(frames_dir, ignore_errors=True)


if __name__ == "__main__":
    import json

    result = coach_video("skye-clip1.mp4")
    print(json.dumps(result, indent=2))