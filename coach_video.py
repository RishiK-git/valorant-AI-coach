import shutil
import tempfile

from pipeline.extract_frames import extract_frames_every_n_seconds
from pipeline.select_frames import select_frames
from pipeline.analyze_frames import analyze_frames
from pipeline.report import SYSTEM_PROMPT, build_report


def coach_video(video_path: str, interval_sec: float = 2.0, max_frames: int = None) -> dict:
    """
    End-to-end pipeline: video in, coaching report out.
    """
    frames_dir = tempfile.mkdtemp(prefix="coach_frames_")

    try:
        extract_frames_every_n_seconds(video_path, frames_dir, interval_sec=interval_sec)
        frame_paths = select_frames(frames_dir, max_frames=max_frames)
        raw_analysis = analyze_frames(frame_paths, SYSTEM_PROMPT)
        report = build_report(raw_analysis)
        return report

    finally:
        shutil.rmtree(frames_dir, ignore_errors=True)


if __name__ == "__main__":
    result = coach_video("skye-clip1.mp4")
    print(result["raw_text"])