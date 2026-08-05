from ultralytics import YOLO

CONFIDENCE_THRESHOLD = 0.75


def detect_frames(frame_paths: list[str], model_path: str) -> dict[str, list[dict]]:
    """
    Runs YOLO inference on a list of frame paths.

    Returns a dict mapping each frame path to a list of detections:
        {
            "/path/to/frame.png": [
                {"class": "enemy", "confidence": 0.91},
                {"class": "ally",  "confidence": 0.83},
                ...
            ],
            ...
        }

    Only detections at or above CONFIDENCE_THRESHOLD are included.
    """
    model = YOLO(model_path)

    detections: dict[str, list[dict]] = {path: [] for path in frame_paths}

    results = model.predict(
        source=frame_paths,
        conf=CONFIDENCE_THRESHOLD,
        imgsz=640,
        verbose=False,
    )

    # results are returned in the same order as frame_paths
    for path, result in zip(frame_paths, results):
        for box in result.boxes:
            cls_name = result.names[int(box.cls[0])]
            confidence = float(box.conf[0])
            detections[path].append({"class": cls_name, "confidence": confidence})

    return detections
