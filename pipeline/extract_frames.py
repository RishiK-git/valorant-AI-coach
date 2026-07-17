import os
import subprocess


def extract_frames_every_n_seconds(video_path: str, output_dir: str, interval_sec: float = 2.0) -> str:
    """
    Extracts one frame every `interval_sec` seconds from video_path
    and saves them as PNGs in output_dir. Returns the output_dir.
    """
    os.makedirs(output_dir, exist_ok=True)

    fps = 1 / interval_sec
    output_pattern = os.path.join(output_dir, "frame_%05d.png")

    subprocess.run(
        [
            "ffmpeg",
            "-i", video_path,
            "-vf", f"fps={fps}",
            "-q:v", "2",
            output_pattern,
        ],
        check=True,
    )

    return output_dir