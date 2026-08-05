from ultralytics import YOLO

# Path to your trained model
MODEL_PATH = "/Users/rishikallepalli/Projects/valorant-coach-poc/runs/detect/runs/detect/valorant_yolo11s_50_collapsed/weights/best.pt"

# Image to test
IMAGE_PATH = "/Users/rishikallepalli/Projects/valorant-coach-poc/test-images/5576227_2376983_ls.jpg"

# Load model
model = YOLO(MODEL_PATH)

# Run inference
results = model.predict(
    source=IMAGE_PATH,
    conf=0.25,
    imgsz=640
)

# Display detections
for result in results:
    result.show()

    print("\nDetections:")
    if len(result.boxes) == 0:
        print("No objects detected.")
    else:
        for box in result.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])

            print(
                f"{result.names[cls]} "
                f"({conf:.2%})"
            )

print(model.names)