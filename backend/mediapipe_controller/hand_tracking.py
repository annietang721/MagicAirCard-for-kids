import cv2
import mediapipe as mp
import numpy as np

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,         # 只检测一只手（画画通常用一只手，能省一半算力）
        model_complexity=0,      # ⚡️ 0=最快(Lite模型), 1=中等, 2=最慢
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
        )   
        self.colors = [(255, 105, 180), (100, 149, 237), (50, 205, 50), (255, 215, 0)]  # 可爱色系
        self.color_idx = 0
        self.prev_x, self.prev_y = 0, 0
        
        # === ✨ 修改点 1：在这里添加 self.mode ✨ ===
        # 这样 Tracker 就能自己记住现在是什么模式了
        self.mode = "normal" 

    # === ✨ 修改点 2：去掉参数里的 mode="normal" ✨ ===
    def get_frame_and_canvas(self, frame, canvas): 
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        h, w, _ = frame.shape
        gesture = "None"

        if results.multi_hand_landmarks:
            for hand_lms in results.multi_hand_landmarks:
                lm = hand_lms.landmark
                # 食指尖(8)和中指尖(12)
                ix, iy = int(lm[8].x * w), int(lm[8].y * h)
                mx, my = int(lm[12].x * w), int(lm[12].y * h)

                # 握拳逻辑：指尖低于关节
                is_fist = lm[8].y > lm[6].y and lm[12].y > lm[10].y

                if is_fist:
                    gesture = "Change Color"
                    self.color_idx = (self.color_idx + 1) % len(self.colors)
                    self.prev_x, self.prev_y = 0, 0
                else:
                    gesture = "Drawing"
                    # 伪3D：距离感应，食指和虎口(5)的距离
                    dist = np.hypot(lm[8].x - lm[5].x, lm[8].y - lm[5].y)
                    
                    # === ✨ 修改点 3：这里改成使用 self.mode ✨ ===
                    thickness = int(dist * 100) if self.mode == "3d" else 8

                    color = self.colors[self.color_idx]
                    
                    # === ✨ 修改点 4：这里改成使用 self.mode ✨ ===
                    if self.mode == "rainbow":
                        # 彩虹逻辑：根据坐标变色，(B, G, R)
                        # ix, iy 是坐标，% 255 确保颜色值在 0-255 之间
                        color = (int(ix % 255), int(iy % 255), 200)

                    if self.prev_x != 0:
                        cv2.line(canvas, (self.prev_x, self.prev_y), (ix, iy), color, thickness)
                    self.prev_x, self.prev_y = ix, iy

                # 在流画面画个引导点
                cv2.circle(frame, (ix, iy), 10, (255, 255, 255), cv2.FILLED)
        else:
            self.prev_x, self.prev_y = 0, 0

        return frame, canvas, gesture