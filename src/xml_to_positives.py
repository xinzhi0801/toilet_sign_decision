import xml.etree.ElementTree as ET
from pathlib import Path

PROJECT_ROOT = Path(r"C:\toilet_sign_decision")

ANNOTATION_DIR = PROJECT_ROOT / "dataset" / "annotations"
IMAGE_DIR = PROJECT_ROOT / "dataset" / "positive"
OUTPUT_FILE = PROJECT_ROOT / "positives.txt"

lines = []
skipped = 0

for xml_file in sorted(ANNOTATION_DIR.glob("*.xml")):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    filename_node = root.find("filename")

    if filename_node is None or filename_node.text is None:
        print(f"跳過 {xml_file.name}：找不到 filename")
        skipped += 1
        continue

    filename = filename_node.text.strip()
    image_path = IMAGE_DIR / filename

    if not image_path.exists():
        print(f"跳過 {xml_file.name}：找不到圖片 {image_path}")
        skipped += 1
        continue

    size_node = root.find("size")

    if size_node is not None:
        img_w = int(float(size_node.find("width").text))
        img_h = int(float(size_node.find("height").text))
    else:
        img_w = None
        img_h = None

    boxes = []

    for obj in root.findall("object"):
        bndbox = obj.find("bndbox")

        if bndbox is None:
            continue

        xmin = int(float(bndbox.find("xmin").text))
        ymin = int(float(bndbox.find("ymin").text))
        xmax = int(float(bndbox.find("xmax").text))
        ymax = int(float(bndbox.find("ymax").text))

        if img_w is not None and img_h is not None:
            xmin = max(0, min(xmin, img_w - 1))
            ymin = max(0, min(ymin, img_h - 1))
            xmax = max(0, min(xmax, img_w))
            ymax = max(0, min(ymax, img_h))

        w = xmax - xmin
        h = ymax - ymin

        if w > 0 and h > 0:
            boxes.append((xmin, ymin, w, h))

    if len(boxes) == 0:
        print(f"跳過 {xml_file.name}：沒有有效標註框")
        skipped += 1
        continue

    rel_image_path = f"dataset/positive/{filename}"

    line = rel_image_path + " " + str(len(boxes))

    for box in boxes:
        line += " {} {} {} {}".format(*box)

    lines.append(line)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for line in lines:
        f.write(line + "\n")

print("完成：", OUTPUT_FILE)
print("正樣本標註圖片數量：", len(lines))
print("跳過數量：", skipped)