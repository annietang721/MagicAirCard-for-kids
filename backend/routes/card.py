from flask import Blueprint, Response, jsonify, request, send_file
from flask_cors import cross_origin
import cv2
import numpy as np
import os
import time
from mediapipe_controller.hand_tracking import HandTracker

card_bp = Blueprint('card', __name__)
tracker = HandTracker()

# === 🚀 性能优化配置 ===
cap = cv2.VideoCapture(0)
# 强制降低分辨率到 640x480 (分辨率太高是卡顿的元凶)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# 限制缓存区，拒绝延迟
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

# 全局变量
canvas = np.zeros((480, 640, 3), dtype=np.uint8)
latest_combined_frame = None

def gen_frames():
    global canvas, latest_combined_frame
    while True:
        success, frame = cap.read()
        if not success:
            break
        
        # ⚠️ 这里我去掉了“自动提亮”，虽然画面暗一点，但速度会快一倍！
        
        # === 🔄 只保留镜像翻转 ===
        frame = cv2.flip(frame, 1)
        
        # 确保尺寸匹配 (防止摄像头不听话还是开了高清)
        if frame.shape[1] != 640 or frame.shape[0] != 480:
            frame = cv2.resize(frame, (640, 480))
            
        # 核心识别
        frame, canvas, gest = tracker.get_frame_and_canvas(frame, canvas)
        
        # 合成
        combined = cv2.addWeighted(frame, 0.3, canvas, 0.7, 0)
        latest_combined_frame = combined.copy()
        
        ret, buffer = cv2.imencode('.jpg', combined)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@card_bp.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@card_bp.route('/api/clear', methods=['POST'])
@cross_origin()
def clear_canvas():
    global canvas
    canvas = np.zeros((480, 640, 3), dtype=np.uint8)
    return jsonify({"status": "cleared"})

@card_bp.route('/api/set_mode', methods=['POST'])
@cross_origin()
def set_mode():
    data = request.json
    mode = data.get('mode', 'normal')
    if hasattr(tracker, 'mode'):
        tracker.mode = mode
    return jsonify({"status": "success"})

# ... 前面的 import 都不变 ...

@card_bp.route('/api/save_card')
@cross_origin()
def save_card():
    # 引用全局的画板变量
    global canvas
    
    # === 🎨 核心魔法：制作白板背景 ===
    # 1. 创建一个纯白的背景 (255,255,255 代表白色)
    # canvas.shape 获取的是 (360, 480, 3) 这种尺寸
    white_board = np.full(canvas.shape, 255, dtype=np.uint8)
    
    # 2. 提取你画的线条
    # 把画板转成灰度图，为了找哪里有颜色
    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    # 设定阈值：只要不是全黑(>10)的地方，就是你画的线条 (mask)
    _, mask = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
    
    # 3. 抠图合并
    # mask_inv 是“没有画画”的区域（背景区）
    mask_inv = cv2.bitwise_not(mask)
    
    # 在白纸上，挖掉你画画的那块区域
    bg_part = cv2.bitwise_and(white_board, white_board, mask=mask_inv)
    # 在画板上，把你画的线条抠出来
    drawing_part = cv2.bitwise_and(canvas, canvas, mask=mask)
    
    # 把“挖空的白纸”和“抠出来的线条”拼在一起
    final_card = cv2.add(bg_part, drawing_part)
    
    # === 保存流程 ===
    save_dir = "saved_cards"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    filename = f"MagicCard_Whiteboard_{timestamp}.jpg"
    filepath = os.path.join(save_dir, filename)
    
    # 保存这张处理过的精美白板图！
    cv2.imwrite(filepath, final_card)
    print(f"✨ 白板贺卡已保存: {filepath}")
    
    # 播放一个系统提示音 (Windows自带，不需要额外库)
    import winsound
    # 频率 1000Hz，持续 200毫秒 (清脆的“叮”一声)
    winsound.Beep(1000, 200) 
    
    return send_file(filepath, as_attachment=True, download_name=filename)