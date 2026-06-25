import cv2
import math

MODEL_PATH = "model/cascade.xml"

cascade = cv2.CascadeClassifier(MODEL_PATH)

if cascade.empty():
    raise RuntimeError("模型載入失敗，請確認 model/cascade.xml 是否存在")

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("無法開啟攝影機，請確認鏡頭是否被其他程式占用")

while True:
    ret, frame = cap.read()

    if not ret:
        print("無法讀取攝影機畫面")
        break

    img_h, img_w = frame.shape[:2]
    img_area = img_w * img_h

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    objects = cascade.detectMultiScale(
        gray,
        scaleFactor=1.05,
        minNeighbors=2,
        minSize=(30, 30),
        maxSize=(500, 500)
    )

    candidates = []

    for (x, y, w, h) in objects:
        area = w * h
        aspect_ratio = w / h

        if area < 1500:
            continue

        if area > img_area * 0.15:
            continue

        if aspect_ratio < 0.4 or aspect_ratio > 2.5:
            continue

        if x <= 5 or y <= 5 or x + w >= img_w - 5 or y + h >= img_h - 5:
            continue

        cx = x + w / 2
        cy = y + h / 2

        img_cx = img_w / 2
        img_cy = img_h / 2

        center_distance = math.sqrt((cx - img_cx) ** 2 + (cy - img_cy) ** 2)

        candidates.append({
            "box": (x, y, w, h),
            "area": area,
            "center_distance": center_distance
        })

    final_boxes = []

    if len(candidates) > 0:
        for item in candidates:
            item["score"] = item["area"] / (item["center_distance"] + 1)

        candidates = sorted(candidates, key=lambda item: item["score"], reverse=True)

        best_box = candidates[0]["box"]
        final_boxes.append(best_box)

    for (x, y, w, h) in final_boxes:
        new_x = int(x - 3.2 * w)
        new_y = int(y - 3.4 * h)
        new_w = int(7.2 * w)
        new_h = int(6.2 * h)

        new_x = max(0, new_x)
        new_y = max(0, new_y)
        new_w = min(new_w, img_w - new_x)
        new_h = min(new_h, img_h - new_y)

        cv2.rectangle(
            frame,
            (new_x, new_y),
            (new_x + new_w, new_y + new_h),
            (0, 255, 0),
            3
        )

        cv2.putText(
            frame,
            "Toilet Sign",
            (new_x, max(30, new_y - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    cv2.putText(
        frame,
        f"Detected: {len(final_boxes)}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (0, 255, 0),
        2
    )

    cv2.imshow("Toilet Sign Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()