import math
import random
import tkinter as tk

# Cấu hình kích thước màn hình
WIDTH, HEIGHT = 1200, 1000


class MagneticSandArt:

    def __init__(self, root):
        self.root = root
        self.root.title("Tus")

        # Tạo canvas nền tối giống Pygame
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#05050a")
        self.canvas.pack()

        # Tạo danh sách các hạt cát: [x, y, vx, vy]
        self.particles = []
        for _ in range(600):
            self.particles.append([
                random.uniform(0, WIDTH),
                random.uniform(0, HEIGHT),
                random.uniform(-1, 1),
                random.uniform(-1, 1),
            ])

        # Khởi tạo tọa độ chuột mặc định ở tâm màn hình
        self.mx, self.my = WIDTH // 2, HEIGHT // 2

        # Lắng nghe sự kiện di chuyển chuột trên cửa sổ
        self.root.bind("<Motion>", self.update_mouse_pos)

        # Bắt đầu vòng lặp hoạt ảnh
        self.animate()

    def update_mouse_pos(self, event):
        """Cập nhật vị trí chuột khi người dùng di chuyển"""
        self.mx = event.x
        self.my = event.y

    def animate(self):
        # Xóa các hạt cũ để vẽ khung hình mới
        self.canvas.delete("all")

        for p in self.particles:
            # Tính khoảng cách từ hạt tới chuột
            dx = self.mx - p[0]
            dy = self.my - p[1]
            d = math.sqrt(dx * dx + dy * dy) + 0.1

            # Tính lực hút nam châm
            force = 250 / d
            p[2] += (dx / d) * force * 0.02
            p[3] += (dy / d) * force * 0.02

            # Lực ma sát nhẹ giúp hạt chuyển động mượt hơn
            p[2] *= 0.96
            p[3] *= 0.96

            # Cập nhật vị trí hạt
            p[0] += p[2]
            p[1] += p[3]

            # Xử lý khi hạt đi xuyên qua viền màn hình (Screen Wrap)
            if p[0] < 0:
                p[0] = WIDTH
            if p[0] > WIDTH:
                p[0] = 0
            if p[1] < 0:
                p[1] = HEIGHT
            if p[1] > HEIGHT:
                p[1] = 0

            # Tính vận tốc để đổi màu hạt dựa trên tốc độ chuyển động
            speed = math.sqrt(p[2] ** 2 + p[3] ** 2)
            r = min(255, int(100 + speed * 80))
            g = min(255, int(180 + speed * 40))
            b = 255
            color = f"#{r:02x}{g:02x}{b:02x}"

            # Vẽ hạt cát lên màn hình (kích thước bán kính bằng 2)
            self.canvas.create_oval(
                p[0] - 2, p[1] - 2, p[0] + 2, p[1] + 2, fill=color, outline=""
            )

        # Lặp lại hàm sau 16 mili-giây (~60 FPS tương đương clock.tick(60))
        self.root.after(16, self.animate)


if __name__ == "__main__":
    root = tk.Tk()
    app = MagneticSandArt(root)
    root.mainloop()
