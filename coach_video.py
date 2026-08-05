import os
import shutil
import tempfile

from pipeline.extract_frames import extract_frames_every_n_seconds
from pipeline.detect_frames import detect_frames
from pipeline.select_frames import select_frames
from pipeline.select_frames_with_enemy_boost import select_frames_with_enemy_boost
from pipeline.analyze_frames import analyze_frames
from pipeline.report import SYSTEM_PROMPT, CoachingReport

# Fine interval for YOLO pass — more frames, better detection coverage
FINE_INTERVAL_SEC = 1.0

MODEL_PATH = os.path.join(
    os.path.dirname(__file__), "models", "valorant_yolo11s_collapsed.pt"
)


def coach_video(video_path: str, interval_sec: float = 2.0, max_frames: int = None) -> dict:
    """
    End-to-end pipeline: video in, structured coaching report out.

    Steps:
    1. Extract frames at a fine interval for YOLO coverage
    2. Run YOLO on all frames to detect enemies/allies
    3. Select frames using enemy-boost logic (base grid + enemy appearance events)
    4. Send selected frames to Gemini for coaching analysis
    """
    frames_dir = tempfile.mkdtemp(prefix="coach_frames_")

    try:
        # Extract at fine interval so YOLO sees enough frames to detect events
        extract_frames_every_n_seconds(video_path, frames_dir, interval_sec=FINE_INTERVAL_SEC)

        # Get all frame paths for YOLO inference
        all_frames = select_frames(frames_dir, interval_sec=FINE_INTERVAL_SEC)
        all_paths = [f["path"] for f in all_frames]

        # Run YOLO detections on every frame
        detections = detect_frames(all_paths, MODEL_PATH)

        # Select frames: base grid at caller's interval + bonus frames on enemy appearance
        frames = select_frames_with_enemy_boost(
            frames_dir,
            fine_interval_sec=FINE_INTERVAL_SEC,
            base_interval_sec=interval_sec,
            detections=detections,
        )

        if max_frames:
            frames = frames[:max_frames]

        report = analyze_frames(frames, SYSTEM_PROMPT, response_schema=CoachingReport)
        return report.model_dump()

    finally:
        shutil.rmtree(frames_dir, ignore_errors=True)


if __name__ == "__main__":
    import json

    result = coach_video("skye-clip1.mp4")
    print(json.dumps(result, indent=2))
