import cv2
import os
import math

# =========================
# 路徑設定
# =========================
MODEL_PATH = "model/cascade.xml"
IMAGE_PATH = "dataset/positive/IMG_3991.JPG"
OUTPUT_PATH = "result/images/result_final4.jpg"
DEBUG_PATH = "result/images/result_debug_raw.jpg"

os.makedirs("result/images", exist_ok=True)

# =========================
# 載入模型
# =========================
cascade = cv2.CascadeClassifier(MODEL_PATH)

if cascade.empty():
    raise RuntimeError("模型載入失敗，請確認 model/cascade.xml 是否存在")

# =========================
# 讀取圖片
# =========================
img = cv2.imread(IMAGE_PATH)

if img is None:
    raise RuntimeError("圖片讀取失敗，請確認 dataset/test/test_001.jpg 是否存在")

img_h, img_w = img.shape[:2]
img_area = img_w * img_h

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# =========================
# Haar Cascade 偵測
# =========================
objects = cascade.detectMultiScale(
    gray,
    scaleFactor=1.05,
    minNeighbors=2,
    minSize=(30, 30),
    maxSize=(500, 500)
)

# =========================
# 儲存原始偵測結果，方便報告或除錯
# =========================
debug_img = img.copy()

for (x, y, w, h) in objects:
    cv2.rectangle(debug_img, (x, y), (x + w, y + h), (0, 255, 255), 2)

cv2.imwrite(DEBUG_PATH, debug_img)

# =========================
# 過濾候選框
# =========================
candidates = []

for (x, y, w, h) in objects:
    area = w * h
    aspect_ratio = w / h

    # 過濾太小的碎框
    if area < 1500:
        continue

    # 過濾太大的框，避免框到整張畫面
    if area > img_area * 0.15:
        continue

    # 過濾太細長或太奇怪的框
    if aspect_ratio < 0.4 or aspect_ratio > 2.5:
        continue

    # 過濾貼近圖片邊界的誤判框
    if x <= 5 or y <= 5 or x + w >= img_w - 5 or y + h >= img_h - 5:
        continue

    # 計算候選框中心
    cx = x + w / 2
    cy = y + h / 2

    # 圖片中心
    img_cx = img_w / 2
    img_cy = img_h / 2

    # 距離圖片中心越近，越可能是主要標誌
    center_distance = math.sqrt((cx - img_cx) ** 2 + (cy - img_cy) ** 2)

    candidates.append({
        "box": (x, y, w, h),
        "area": area,
        "center_distance": center_distance
    })

# =========================
# 選擇最佳候選框
# =========================
final_boxes = []

if len(candidates) > 0:
    # 分數設計：
    # 面積較大比較好，但不要大到框整張圖
    # 距離圖片中心較近比較好
    for item in candidates:
        item["score"] = item["area"] / (item["center_distance"] + 1)

    candidates = sorted(candidates, key=lambda item: item["score"], reverse=True)

    best_box = candidates[0]["box"]
    final_boxes.append(best_box)

# =========================
# 將局部框放大成完整廁所標誌框
# =========================
output_img = img.copy()

for (x, y, w, h) in final_boxes:
    # 這組比例是針對目前你的模型：
    # 模型常偵測到人形圖示的一小部分，因此要往外放大
    new_x = int(x - 3.2 * w)
    new_y = int(y - 3.4 * h)
    new_w = int(7.2 * w)
    new_h = int(6.2 * h)

    # 防止超出圖片邊界
    new_x = max(0, new_x)
    new_y = max(0, new_y)
    new_w = min(new_w, img_w - new_x)
    new_h = min(new_h, img_h - new_y)

    cv2.rectangle(
        output_img,
        (new_x, new_y),
        (new_x + new_w, new_y + new_h),
        (0, 255, 0),
        4
    )

    cv2.putText(
        output_img,
        "Toilet Sign",
        (new_x, max(30, new_y - 10)),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (0, 255, 0),
        3
    )

# =========================
# 輸出結果
# =========================
cv2.imwrite(OUTPUT_PATH, output_img)

print("原始偵測數量：", len(objects))
print("候選框數量：", len(candidates))
print("最終輸出數量：", len(final_boxes))
print("原始偵測除錯圖：", DEBUG_PATH)
print("最終結果圖：", OUTPUT_PATH)