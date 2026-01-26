import cv2
import mediapipe as mp
import numpy as np

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,        # 只检测一只手
            model_complexity=0,     # ⚡️ 速度优先
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )   
        self.colors = [(255, 105, 180), (100, 149, 237), (50, 205, 50), (255, 215, 0)]
        self.color_idx = 0
        self.prev_x, self.prev_y = 0, 0
        self.mode = "normal"

        # === 🛡️ 防抖核心变量 (新加的) ===
        self.smooth_x, self.smooth_y = 0, 0
        # 平滑系数 0.4：数字越小越平滑(但有延迟)，数字越大越灵敏(但会抖)
        # 0.4 是最佳平衡点，既不抖也不卡
        self.smooth_factor = 0.4

    def get_frame_and_canvas(self, frame, canvas): 
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        h, w, _ = frame.shape
        gesture = "None"

        if results.multi_hand_landmarks:
            for hand_lms in results.multi_hand_landmarks:
                lm = hand_lms.landmark
                # 获取原始坐标
                raw_ix, raw_iy = int(lm[8].x * w), int(lm[8].y * h)
                mx, my = int(lm[12].x * w), int(lm[12].y * h)

                # === 🛡️ 防抖计算 (新加的) ===
                if self.smooth_x == 0 and self.smooth_y == 0:
                    # 第一帧直接瞬移过去，不要平滑
                    self.smooth_x, self.smooth_y = raw_ix, raw_iy
                else:
                    # 后续帧：新位置 = 旧位置*0.6 + 新位置*0.4
                    self.smooth_x = self.smooth_x * (1 - self.smooth_factor) + raw_ix * self.smooth_factor
                    self.smooth_y = self.smooth_y * (1 - self.smooth_factor) + raw_iy * self.smooth_factor
                
                # 使用平滑后的坐标作为最终坐标 (ix, iy)
                ix, iy = int(self.smooth_x), int(self.smooth_y)
                # ==============================

                # 握拳逻辑：指尖低于关节
                is_fist = lm[8].y > lm[6].y and lm[12].y > lm[10].y

                if is_fist:
                    gesture = "Change Color"
                    # 简单防抖：只有当之前在画画(prev_x!=0)时突然握拳，才认为是切换，防止连续闪烁
                    if self.prev_x != 0:
                         self.color_idx = (self.color_idx + 1) % len(self.colors)
                    self.prev_x, self.prev_y = 0, 0
                    self.smooth_x, self.smooth_y = 0, 0 # 握拳时重置防抖
                else:
                    gesture = "Drawing"
                    # 伪3D：距离感应
                    dist = np.hypot(lm[8].x - lm[5].x, lm[8].y - lm[5].y)
                    
                    thickness = int(dist * 100) if self.mode == "3d" else 8

                    color = self.colors[self.color_idx]
                    
                    if self.mode == "rainbow":
                        # 彩虹逻辑
                        color = (int(ix % 255), int(iy % 255), 200)

                    if self.prev_x != 0:
                        # 用平滑后的 ix, iy 画线，绝对稳！
                        cv2.line(canvas, (self.prev_x, self.prev_y), (ix, iy), color, thickness)
                    
                    self.prev_x, self.prev_y = ix, iy

                # 在流画面画个引导点
                cv2.circle(frame, (ix, iy), 10, (255, 255, 255), cv2.FILLED)
        else:
            self.prev_x, self.prev_y = 0, 0
            self.smooth_x, self.smooth_y = 0, 0 # 手离开画面，重置防抖

        return frame, canvas, gesture