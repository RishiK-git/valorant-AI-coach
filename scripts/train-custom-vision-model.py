import time
import torch
from ultralytics import YOLO

DATA_YAML_PATH = "/Users/rishikallepalli/Projects/valorant-coach-poc/valorant-vision-dataset/Valorant Object Detection.yolov11-collapsed/data.yaml"
MODEL_NAME = "yolo11s.pt"  
NUM_EPOCHS = 50


def check_mps():
    available = torch.backends.mps.is_available()
    print(f"MPS available: {available}")
    if not available:
        print("WARNING: MPS not available - training will fall back to CPU and be much slower.")
    return available


def run_full_training():
    check_mps()

    model = YOLO(MODEL_NAME)

    print(f"\nStarting {NUM_EPOCHS}-epoch test run with {MODEL_NAME}...\n")

    start = time.perf_counter()

    model.train(
        data=DATA_YAML_PATH,
        epochs=NUM_EPOCHS,
        imgsz=640,
        batch=8,
        device="mps",
        patience=15,
        project="runs/detect",
        name="valorant_yolo11s_50_collapsed"
    )

    elapsed = time.perf_counter() - start
    per_epoch = elapsed / NUM_EPOCHS
    estimated_50 = per_epoch * 50

    print(f"\n--- TIMING RESULTS ---")
    print(f"Total time for {NUM_EPOCHS} epochs: {elapsed:.1f} seconds ({elapsed / 60:.1f} min)")



if __name__ == "__main__":
    run_full_training()