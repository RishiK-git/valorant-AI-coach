import os
import shutil
import yaml
from pathlib import Path

DATASET_DIR = "/Users/rishikallepalli/Projects/valorant-coach-poc/valorant-vision-dataset/Valorant Object Detection.yolov11/"          # your existing 77-class export
OUTPUT_DIR = "/Users/rishikallepalli/Projects/valorant-coach-poc/valorant-vision-dataset/Valorant Object Detection.yolov11-collapsed"  # new collapsed dataset, kept separate


def build_class_mapping(class_names: list[str]) -> dict[int, int]:
    """
    Maps each original class ID to 0 (ally), 1 (enemy), or -1 (drop entirely -
    e.g. 'Headshot splash' isn't an ally/enemy class at all).
    """
    mapping = {}
    for class_id, name in enumerate(class_names):
        normalized = name.lower()
        if "ally" in normalized:
            mapping[class_id] = 0
        elif "enemy" in normalized:
            mapping[class_id] = 1
        else:
            mapping[class_id] = -1  # dropped, e.g. "Headshot splash"
    return mapping


def remap_label_file(src_path: Path, dst_path: Path, mapping: dict[int, int]):
    """
    Rewrites one label file, remapping class IDs and dropping any lines
    whose class maps to -1.
    """
    lines_out = []
    with open(src_path) as f:
        for line in f:
            if not line.strip():
                continue
            parts = line.split()
            old_class_id = int(parts[0])
            new_class_id = mapping.get(old_class_id, -1)

            if new_class_id == -1:
                continue  # drop this instance entirely

            parts[0] = str(new_class_id)
            lines_out.append(" ".join(parts))

    with open(dst_path, "w") as f:
        f.write("\n".join(lines_out) + ("\n" if lines_out else ""))


def process_split(dataset_dir: str, output_dir: str, split: str, mapping: dict[int, int]):
    src_images_dir = Path(dataset_dir) / split / "images"
    src_labels_dir = Path(dataset_dir) / split / "labels"
    dst_images_dir = Path(output_dir) / split / "images"
    dst_labels_dir = Path(output_dir) / split / "labels"

    dst_images_dir.mkdir(parents=True, exist_ok=True)
    dst_labels_dir.mkdir(parents=True, exist_ok=True)

    for label_file in src_labels_dir.glob("*.txt"):
        remap_label_file(label_file, dst_labels_dir / label_file.name, mapping)

    for image_file in src_images_dir.iterdir():
        shutil.copy(image_file, dst_images_dir / image_file.name)

    print(f"Processed {split}: {len(list(src_labels_dir.glob('*.txt')))} label files")


def write_collapsed_data_yaml(output_dir: str):
    data = {
        "train": "train/images",
        "val": "valid/images",
        "test": "test/images",
        "nc": 2,
        "names": ["ally", "enemy"],
    }
    with open(Path(output_dir) / "data.yaml", "w") as f:
        yaml.dump(data, f, default_flow_style=False)


if __name__ == "__main__":
    with open(Path(DATASET_DIR) / "data.yaml") as f:
        original_data = yaml.safe_load(f)
    class_names = original_data["names"]

    mapping = build_class_mapping(class_names)

    print("Class mapping preview:")
    for class_id, name in enumerate(class_names):
        target = {0: "ally", 1: "enemy", -1: "DROPPED"}[mapping[class_id]]
        print(f"  {name} -> {target}")

    for split in ["train", "valid", "test"]:
        process_split(DATASET_DIR, OUTPUT_DIR, split, mapping)

    write_collapsed_data_yaml(OUTPUT_DIR)

    print(f"\nCollapsed dataset written to {OUTPUT_DIR}")