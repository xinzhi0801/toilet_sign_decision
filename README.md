# Toilet Sign Detection using Haar Cascade

## 1. 專題名稱

元智校園廁所標誌偵測系統
Toilet Sign Detection using OpenCV Haar Cascade

---

## 2. 專題簡介

本專題以元智大學校園中的廁所標誌作為偵測目標，使用自行拍攝與標註的影像資料集，透過 OpenCV Haar Cascade 訓練一個物件偵測模型。系統可針對圖片或攝影機畫面進行偵測，並在畫面中以綠色框線標示出廁所標誌的位置。

由於 Haar Cascade 對邊緣與局部形狀特徵較敏感，因此本專題的模型主要先偵測廁所標誌中的人形圖示特徵，再透過後處理方式將偵測框放大，使輸出結果能涵蓋主要的廁所標誌區域。

---

## 3. 專題目標

本專題的主要目標如下：

1. 自行收集校園內廁所標誌影像資料。
2. 使用 labelImg 工具對正樣本進行標註。
3. 使用 OpenCV Haar Cascade 訓練廁所標誌偵測模型。
4. 完成圖片偵測與攝影機即時偵測功能。
5. 將程式碼、模型、資料集與測試結果整理至 GitHub。
6. 撰寫 README，使其他使用者可以依照說明執行本專題。

---

## 4. 開發環境

本專題使用的開發環境如下：

| 項目   | 內容                      |
| ---- | ----------------------- |
| 作業系統 | Windows 10 / Windows 11 |
| 程式語言 | Python                  |
| 主要套件 | OpenCV, labelImg        |
| 標註工具 | labelImg                |
| 偵測方法 | Haar Cascade            |
| 開發工具 | VS Code / CMD           |
| 版本控制 | Git / GitHub            |

---

## 5. 專案資料夾結構

```text
toilet_sign_decision/
│
├── src/
│   ├── detect_image.py
│   ├── detect_camera.py
│   ├── xml_to_positives.py
│   └── make_negatives.py
│
├── dataset/
│   ├── positive/
│   ├── negative/
│   ├── annotations/
│   └── test/
│
├── model/
│   └── cascade.xml
│
├── result/
│   └── images/
│       └── result_final.jpg
│
├── train/
│   └── classifier/
│
├── positives.txt
├── negatives.txt
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 6. 資料集說明

本專題資料集分為正樣本、負樣本與測試圖片。

### 正樣本

正樣本放置於：

```text
dataset/positive/
```

正樣本內容為含有廁所標誌的圖片，主要包含男廁、女廁或廁所標誌牌等影像。

### 負樣本

負樣本放置於：

```text
dataset/negative/
```

負樣本內容為不含廁所標誌的校園環境圖片，例如牆面、走廊、門牌、公告欄、電梯標誌或其他非目標物件。

### 標註檔案

標註檔案放置於：

```text
dataset/annotations/
```

標註格式為 labelImg 產生的 Pascal VOC XML 格式。

### 測試圖片

測試圖片放置於：

```text
dataset/test/
```

目前圖片偵測程式預設讀取：

```text
dataset/test/test_001.jpg
```

---

## 7. 安裝方式

請先確認電腦已安裝 Python，接著在專案資料夾中建立虛擬環境。

```bat
python -m venv .venv
```

啟動虛擬環境：

```bat
.venv\Scripts\activate
```

安裝需要的套件：

```bat
pip install -r requirements.txt
```

若沒有 `requirements.txt`，也可以手動安裝：

```bat
pip install opencv-python labelImg lxml pillow
```

---

## 8. 產生訓練用文字檔

### 產生正樣本標註檔

```bat
python src\xml_to_positives.py
```

執行後會產生：

```text
positives.txt
```

### 產生負樣本列表

```bat
python src\make_negatives.py
```

執行後會產生：

```text
negatives.txt
```

---

## 9. Haar Cascade 模型訓練方式

本專題使用 OpenCV 提供的 `opencv_createsamples.exe` 與 `opencv_traincascade.exe` 進行訓練。

### 產生 samples.vec

```bat
opencv_createsamples.exe -info positives.txt -vec train\samples.vec -num 80 -w 32 -h 32
```

### 訓練 Haar Cascade

```bat
opencv_traincascade.exe -data train\classifier -vec train\samples.vec -bg negatives.txt -numPos 70 -numNeg 50 -numStages 10 -w 32 -h 32 -featureType HAAR -minHitRate 0.995 -maxFalseAlarmRate 0.5
```

訓練完成後，將模型複製到 `model` 資料夾：

```bat
copy train\classifier\cascade.xml model\cascade.xml
```

---

## 10. 圖片偵測執行方式

圖片偵測程式為：

```text
src/detect_image.py
```

執行方式：

```bat
python src\detect_image.py
```

程式會讀取：

```text
dataset/test/test_001.jpg
```

並輸出結果至：

```text
result/images/result_final.jpg
```

---

## 11. 攝影機即時偵測執行方式

攝影機偵測程式為：

```text
src/detect_camera.py
```

執行方式：

```bat
python src\detect_camera.py
```

執行後會開啟電腦攝影機，當畫面中出現廁所標誌時，系統會以綠色框線標示偵測結果。

若要結束程式，請按鍵盤：

```text
q
```

如果攝影機無法開啟，可以將程式中的：

```python
cap = cv2.VideoCapture(0)
```

改成：

```python
cap = cv2.VideoCapture(1)
```

---

## 12. 偵測方法說明

本專題採用 Haar Cascade 作為物件偵測方法。Haar Cascade 會透過大量正樣本與負樣本學習目標物件的影像特徵，例如邊緣、明暗差異與形狀結構。

在本系統中，模型主要偵測廁所標誌中的人形圖示區域。由於實際測試時模型較容易偵測到局部圖示，而不是完整標誌外框，因此程式加入後處理機制，將偵測到的局部框依照比例放大，使最後輸出的框線能涵蓋主要廁所標誌區域。

---

## 13. 測試結果

圖片測試結果如下：

```text
result/images/result_final.jpg
```

測試結果顯示，在近距離、正面拍攝且標誌清楚的情況下，系統能夠偵測到廁所標誌。若背景紋理複雜、光線反射明顯、角度過斜或目標太遠，仍可能產生誤判或漏偵測。

---

## 14. 遇到的問題與解決方式

### 問題一：模型容易產生誤判

一開始測試時，模型會將牆面紋理、窗框或其他高對比物件誤判為廁所標誌。

解決方式：

* 增加負樣本數量。
* 加入相似但不是廁所標誌的 hard negative 圖片。
* 調整 `scaleFactor`、`minNeighbors`、`minSize` 與 `maxSize`。
* 加入候選框過濾機制。

### 問題二：模型只偵測到局部圖示

Haar Cascade 訓練後較容易偵測到廁所標誌中的人形圖示局部，而不是完整標誌牌。

解決方式：

* 在偵測後加入 bounding box expansion。
* 將局部偵測框依照比例放大。
* 讓最後顯示結果能涵蓋主要廁所標誌區域。

### 問題三：資料集數量較少

由於資料集是自行收集，正樣本與負樣本數量有限，因此模型泛化能力仍有提升空間。

解決方式：

* 使用不同角度、距離與光線條件拍攝資料。
* 增加不同廁所標誌樣式。
* 補充更多背景負樣本。

---

## 15. 展示影片

Demo video：

```text
請在此貼上 Google Drive 或 YouTube 不公開影片連結
```

---

## 16. GitHub Repository

GitHub repository：

```text
https://github.com/xinzhi0801/toilet_sign_decision
```

---

## 17. 結論

本專題完成了以 OpenCV Haar Cascade 為基礎的廁所標誌偵測系統，包含資料收集、影像標註、模型訓練、圖片測試與攝影機即時偵測。實驗結果顯示，Haar Cascade 在固定目標、明顯圖形與近距離拍攝的情況下可以達成基本偵測效果，但面對複雜背景與不同拍攝條件時仍有誤判問題。

透過本專題可以了解傳統物件偵測方法的完整流程，也能觀察到資料集品質、正負樣本比例與參數設定對偵測結果的影響。未來若要提升準確率，可改用 YOLO、SSD 或 Faster R-CNN 等深度學習物件偵測方法，並收集更多不同場景下的資料進行訓練。

---

## 18. 參考資料

1. OpenCV Documentation
   https://docs.opencv.org/

2. OpenCV Cascade Classifier Training
   https://docs.opencv.org/3.4/dc/d88/tutorial_traincascade.html

3. labelImg GitHub
   https://github.com/HumanSignal/labelImg

4. GitHub Docs
   https://docs.github.com/
