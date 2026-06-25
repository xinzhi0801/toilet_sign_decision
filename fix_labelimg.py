from pathlib import Path

path = Path(r"C:\toilet_sign_decision\.venv\Lib\site-packages\libs\canvas.py")

text = path.read_text(encoding="utf-8")

# 把 Tab 全部改成 4 個空白，避免 TabError
text = text.replace("\t", "    ")

lines = []

for line in text.splitlines():
    stripped = line.strip()
    indent = line[:len(line) - len(line.lstrip())]

    if stripped == "p.drawLine(self.prev_point.x(), 0, self.prev_point.x(), self.pixmap.height())":
        line = indent + "p.drawLine(int(self.prev_point.x()), 0, int(self.prev_point.x()), int(self.pixmap.height()))"

    elif stripped == "p.drawLine(0, self.prev_point.y(), self.pixmap.width(), self.prev_point.y())":
        line = indent + "p.drawLine(0, int(self.prev_point.y()), int(self.pixmap.width()), int(self.prev_point.y()))"

    elif stripped == "p.drawRect(left_top.x(), left_top.y(), rect_width, rect_height)":
        line = indent + "p.drawRect(int(left_top.x()), int(left_top.y()), int(rect_width), int(rect_height))"

    lines.append(line)

path.write_text("\n".join(lines) + "\n", encoding="utf-8")

print("labelImg canvas.py 修正完成")