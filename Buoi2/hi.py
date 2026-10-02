import math
import tkinter as tk

# Cấu hình màn hình hiển thị
WIDTH, HEIGHT = 1000, 800

# Cấu hình cấu trúc sinh vật tinh chỉnh theo mẫu xương
NUM_SEGMENTS = 60      # Số lượng đốt dài mịn
SEGMENT_DISTANCE = 8   # Các đốt khít nhau tạo xương sống liên tục
BASE_RADIUS = 12       # Độ rộng của xương sườn ở phần đầu

segments = [[WIDTH // 2, HEIGHT // 2] for _ in range(NUM_SEGMENTS)]
time_counter = 0

class ExactMatchCreatureSimulation:
    def __init__(self, root):
        self.root = root
        self.root.title("Exact Match Centipede IK")

        # Tạo canvas nền trắng
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.pack()

        self.canvas.bind("<Motion>", self.update_mouse_position)

        self.target_x = WIDTH // 2
        self.target_y = HEIGHT // 2
        self.last_target_x = WIDTH // 2
        self.last_target_y = WIDTH // 2
        
        self.follow_goal_x = WIDTH // 2
        self.follow_goal_y = HEIGHT // 2

        self.update_frame()

    def update_mouse_position(self, event):
        self.target_x = event.x
        self.target_y = event.y

    def update_frame(self):
        global time_counter, segments

        self.canvas.delete("all")

        # --- LOGIC KIỂM TRA CHUỘT DI CHUYỂN ĐỂ NGOE NGUẨY CHÂN ---
        mouse_moved = math.hypot(self.target_x - self.last_target_x, self.target_y - self.last_target_y)
        if mouse_moved > 0.5:
            time_counter += 0.2
            
        self.last_target_x = self.target_x
        self.last_target_y = self.target_y

        # --- LOGIC ĐUỔI THEO CÁCH ĐOẠN ---
        dx_target = self.target_x - segments[0][0]
        dy_target = self.target_y - segments[0][1]
        dist_to_mouse = math.hypot(dx_target, dy_target)

        KEEP_DISTANCE = 70   # Khoảng cách đuổi theo giữ khoảng cách với chuột
        EASING_FACTOR = 0.08 # Độ trễ quán tính mượt mà

        if dist_to_mouse > KEEP_DISTANCE:
            self.follow_goal_x = self.target_x - (dx_target / dist_to_mouse) * KEEP_DISTANCE
            self.follow_goal_y = self.target_y - (dy_target / dist_to_mouse) * KEEP_DISTANCE

            segments[0][0] += (self.follow_goal_x - segments[0][0]) * EASING_FACTOR
            segments[0][1] += (self.follow_goal_y - segments[0][1]) * EASING_FACTOR

        # --- THUẬT TOÁN INVERSE KINEMATICS ---
        for i in range(1, NUM_SEGMENTS):
            leader = segments[i - 1]
            follower = segments[i]
            dx = follower[0] - leader[0]
            dy = follower[1] - leader[1]
            distance = math.hypot(dx, dy)

            if distance > 0:
                follower[0] = leader[0] + (dx / distance) * SEGMENT_DISTANCE
                follower[1] = leader[1] + (dy / distance) * SEGMENT_DISTANCE

        # --- VẼ HỆ THỐNG XƯƠNG VÀ CHÂN NHỌN THEO MẪU ---
        # BƯỚC 1: Vẽ chân trước để xương sống đè lên trên tạo chiều sâu giống ảnh
        for i in range(NUM_SEGMENTS - 1, -1, -1):
            x, y = segments[i]
            radius = max(1, BASE_RADIUS - (i * 0.2)) # Nhỏ dần về đuôi thành một sợi gai nhọn

            if i < NUM_SEGMENTS - 1:
                next_x, next_y = segments[i + 1]
                angle = math.atan2(y - next_y, x - next_x)
            else:
                angle = math.atan2(segments[i - 1][1] - y, segments[i - 1][0] - x) + math.pi

            # Cứ cách 2 đốt vẽ cặp chân khớp dài bẻ gập nhọn hoắt ra sau
            if i % 2 == 0 and 4 < i < NUM_SEGMENTS - 5:
                thigh_length = radius * 3.5
                calf_length = radius * 3.0
                wave = math.sin(time_counter - i * 0.4) * 0.35

                # Chân trái gập gối nhọn ra sau
                left_thigh_angle = angle + math.pi / 2 + wave
                lk_x = x + math.cos(left_thigh_angle) * thigh_length
                lk_y = y + math.sin(left_thigh_angle) * thigh_length
                left_calf_angle = left_thigh_angle - math.pi / 2 + wave * 0.3
                lf_x = lk_x + math.cos(left_calf_angle) * calf_length
                lf_y = lk_y + math.sin(left_calf_angle) * calf_length

                self.canvas.create_line(x, y, lk_x, lk_y, fill="black", width=1.5)
                self.canvas.create_line(lk_x, lk_y, lf_x, lf_y, fill="black", width=1.2)

                # Chân phải gập gối đối xứng
                right_thigh_angle = angle - math.pi / 2 - wave
                rk_x = x + math.cos(right_thigh_angle) * thigh_length
                rk_y = y + math.sin(right_thigh_angle) * thigh_length
                right_calf_angle = right_thigh_angle + math.pi / 2 - wave * 0.3
                rf_x = rk_x + math.cos(right_calf_angle) * calf_length
                rf_y = rk_y + math.sin(right_calf_angle) * calf_length

                self.canvas.create_line(x, y, rk_x, rk_y, fill="black", width=1.5)
                self.canvas.create_line(rk_x, rk_y, rf_x, rf_y, fill="black", width=1.2)

            # BƯỚC 2: Vẽ xương sườn tủa ra ngang hai bên của từng đốt
            perp_angle = angle + math.pi / 2
            rib_x1 = x + math.cos(perp_angle) * radius
            rib_y1 = y + math.sin(perp_angle) * radius
            rib_x2 = x - math.cos(perp_angle) * radius
            rib_y2 = y - math.sin(perp_angle) * radius
            self.canvas.create_line(rib_x1, rib_y1, rib_x2, rib_y2, fill="black", width=1.5)

        # BƯỚC 3: Vẽ đường xương sống trung tâm nối liền từ đầu đến cuối đuôi
        for i in range(NUM_SEGMENTS - 1):
            x1, y1 = segments[i]
            x2, y2 = segments[i + 1]
            self.canvas.create_line(x1, y1, x2, y2, fill="black", width=2.5)

        self.root.after(16, self.update_frame)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExactMatchCreatureSimulation(root)
    root.mainloop()
