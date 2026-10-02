import math
import tkinter as tk

# Cấu hình kích thước màn hình
WIDTH, HEIGHT = 500, 500
cx, cy = WIDTH // 2, HEIGHT // 2


class PlasmaRingApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Electric Plasma Ring")

        # Tạo canvas nền đen thay cho screen.fill((0, 0, 0))
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        self.angle = 0
        self.animate()

    def animate(self):
        # Xóa màn hình cũ trước khi vẽ khung hình mới
        self.canvas.delete("all")

        # 1. Vẽ vòng tròn chấm plasma ngoài cùng
        for i in range(180):
            a = math.radians(i * 2) + self.angle
            r = 170 + 12 * math.sin(i * 0.3 + self.angle * 6)
            x = cx + math.cos(a) * r
            y = cy + math.sin(a) * r

            # Tính toán màu sắc đổ về mã Hex để Tkinter hiểu được
            g = 180 + int(75 * math.sin(i * 0.2 + self.angle * 3))
            g = max(0, min(255, g))  # Giới hạn màu từ 0 -> 255
            color = f"#00{g:02x}ff"

            self.canvas.create_oval(
                x - 4, y - 4, x + 4, y + 4, fill=color, outline=""
            )

        # 2. Vẽ các đoạn thẳng tia sét điện
        for i in range(40):
            a = i * 0.6 + self.angle * 4
            r1 = 120 + 25 * math.sin(self.angle * 5 + i)
            r2 = 175 + 20 * math.cos(self.angle * 4 + i)
            x1 = cx + math.cos(a) * r1
            y1 = cy + math.sin(a) * r1
            x2 = cx + math.cos(a + 0.25) * r2
            y2 = cy + math.sin(a + 0.25) * r2

            self.canvas.create_line(x1, y1, x2, y2, fill="#64ffff", width=2)

        # 3. Vẽ các vòng tròn xung mạch ở tâm (Pulse)
        pulse = 55 + 8 * math.sin(self.angle * 6)
        self.canvas.create_oval(
            cx - pulse,
            cy - pulse,
            cx + pulse,
            cy + pulse,
            fill="#00ffff",
            outline="",
        )
        self.canvas.create_oval(
            cx - pulse / 2,
            cy - pulse / 2,
            cx + pulse / 2,
            cy + pulse / 2,
            fill="#ffffff",
            outline="",
        )

        # 4. Vẽ 12 hạt năng lượng chạy vòng quanh
        for i in range(12):
            a = self.angle * 2 + i * (math.pi / 6)
            x = cx + math.cos(a) * 230
            y = cy + math.sin(a) * 230
            self.canvas.create_oval(
                x - 5, y - 5, x + 5, y + 5, fill="#00ffb4", outline=""
            )

        # Tăng góc xoay và lặp lại hiệu ứng (~60 FPS)
        self.angle += 0.02
        self.root.after(16, self.animate)


if __name__ == "__main__":
    root = tk.Tk()
    app = PlasmaRingApp(root)
    root.mainloop()
