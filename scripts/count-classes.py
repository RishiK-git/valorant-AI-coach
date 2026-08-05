import os
from pathlib import Path
from collections import Counter

DATASET_DIR = "/Users/rishikallepalli/Projects/valorant-coach-poc/valorant-vision-dataset/Valorant Object Detection.yolov11/"  # wherever Roboflow's export landed
DATA_YAML_PATH = os.path.join(DATASET_DIR, "data.yaml")


def load_class_names(data_yaml_path: str) -> list[str]:
    import yaml
    with open(data_yaml_path) as f:
        data = yaml.safe_load(f)
    return data["names"]


def count_class_instances(dataset_dir: str, split: str = "train") -> Counter:
    """
    Counts how many labeled instances of each class exist in a given split
    (train/valid/test).
    """
    labels_dir = os.path.join(dataset_dir, split, "labels")
    counts = Counter()

    for label_file in Path(labels_dir).glob("*.txt"):
        with open(label_file) as f:
            for line in f:
                if line.strip():
                    class_id = int(line.split()[0])
                    counts[class_id] += 1

    return counts


if __name__ == "__main__":
    class_names = load_class_names(DATA_YAML_PATH)

    for split in ["train", "valid", "test"]:
        counts = count_class_instances(DATASET_DIR, split)
        print(f"\n--- {split.upper()} ---")
        for class_id, count in sorted(counts.items(), key=lambda x: -x[1]):
            name = class_names[class_id] if class_id < len(class_names) else f"unknown_id_{class_id}"
            print(f"{name}: {count}")