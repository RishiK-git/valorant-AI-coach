import time
import torch
from ultralytics import YOLO

DATA_YAML_PATH = "/Users/rishikallepalli/Projects/valorant-coach-poc/valorant-vision-dataset/Valorant Object Detection.yolov11/data.yaml"
MODEL_NAME = "yolo11s.pt"  
TEST_EPOCHS = 2


def check_mps():
    available = torch.backends.mps.is_available()
    print(f"MPS available: {available}")
    if not available:
        print("WARNING: MPS not available - training will fall back to CPU and be much slower.")
    return available


def run_speed_test():
    check_mps()

    model = YOLO(MODEL_NAME)

    print(f"\nStarting {TEST_EPOCHS}-epoch test run with {MODEL_NAME}...\n")

    start = time.perf_counter()

    model.train(
        data=DATA_YAML_PATH,
        epochs=TEST_EPOCHS,
        imgsz=640,
        batch=8,
        device="mps",
        cache=True,
        patience=15,
        project="models",
        name="valorant_yolo11s_cache_test_2_epochs"
    )

    elapsed = time.perf_counter() - start
    per_epoch = elapsed / TEST_EPOCHS
    estimated_50 = per_epoch * 50

    print(f"\n--- TIMING RESULTS ---")
    print(f"Total time for {TEST_EPOCHS} epochs: {elapsed:.1f} seconds ({elapsed / 60:.1f} min)")
    print(f"Average per epoch: {per_epoch:.1f} seconds ({per_epoch / 60:.1f} min)")
    print(f"Rough estimate for 50 epochs: {estimated_50 / 60:.1f} min ({estimated_50 / 3600:.1f} hours)")
    print("\nNote: this is a rough linear estimate. Actual full runs can vary due to")
    print("caching effects, thermal throttling over long runs, or early stopping.")


if __name__ == "__main__":
    run_speed_test()