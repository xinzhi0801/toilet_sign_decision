from pathlib import Path

PROJECT_ROOT = Path(r"C:\toilet_sign_decision")

NEGATIVE_DIR = PROJECT_ROOT / "dataset" / "negative"
OUTPUT_FILE = PROJECT_ROOT / "negatives.txt"

image_exts = [".jpg", ".jpeg", ".png", ".bmp", ".JPG", ".JPEG", ".PNG", ".BMP"]

lines = []

for file in sorted(NEGATIVE_DIR.iterdir()):
    if file.suffix in image_exts:
        lines.append(file.resolve().as_posix())

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for line in lines:
        f.write(line + "\n")

print("完成：", OUTPUT_FILE)
print("負樣本數量：", len(lines))