from pipeline.select_frames import select_frames


def select_frames_with_enemy_boost(
    frames_dir: str,
    fine_interval_sec: float,
    base_interval_sec: float,
    detections: dict[str, list],
) -> list[dict]:
    all_frames = select_frames(frames_dir, interval_sec=fine_interval_sec)

    base_step = int(base_interval_sec / fine_interval_sec)
    selected = set()

    # Rule 1: keep every Nth frame (the original base-interval grid)
    for i, frame in enumerate(all_frames):
        if i % base_step == 0:
            selected.add(frame["path"])

    # Rule 2: keep only the FIRST frame of each continuous enemy-detection streak
    in_streak = False
    for frame in all_frames:
        has_enemy = any(d["class"] == "enemy" for d in detections.get(frame["path"], []))
        if has_enemy and not in_streak:
            selected.add(frame["path"])
            in_streak = True
        elif not has_enemy:
            in_streak = False

    # Rule 3: always include the last 5 seconds of the clip (likely outcome/death)
    tail_count = max(1, int(5 / fine_interval_sec))
    for frame in all_frames[-tail_count:]:
        selected.add(frame["path"])

    result = [f for f in all_frames if f["path"] in selected]
    return sorted(result, key=lambda f: f["timestamp"])