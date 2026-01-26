from flask import Blueprint, Response, jsonify, request, send_file
from flask_cors import cross_origin
import cv2
import numpy as np
import os
import time

# 确保你的路径能找到 mediapipe_controller
from mediapipe_controller.hand_tracking import HandTracker

card_bp = Blueprint('card', __name__)
tracker = HandTracker()

# 1. 摄像头配置
cap = cv2.VideoCapture(0)
# 这一行非常关键，设置缓存为1，能极大减少卡顿延迟！
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

# 2. 全局变量
canvas = np.zeros((480, 640, 3), dtype=np.uint8)
latest_combined_frame = None  # 用于保存贺卡

def gen_frames():
    global canvas, latest_combined_frame
    while True:
        success, frame = cap.read()
        if not success:
            break
        
        # === 💡 1. 恢复自动提亮 (这会让画面清晰，识别更准) ===
        frame = cv2.convertScaleAbs(frame, alpha=1.3, beta=40)
        
        # === 🔄 2. 恢复镜像翻转 (解决“画面反了”的问题) ===
        frame = cv2.flip(frame, 1)
        
        # 3. 核心处理
        frame, canvas, gest = tracker.get_frame_and_canvas(frame, canvas)
        
        # 4. 合成画面
        combined = cv2.addWeighted(frame, 0.3, canvas, 0.7, 0)
        
        # 5. 留底（为了能保存）
        latest_combined_frame = combined.copy()
        
        # 6. 发送
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
    return jsonify({"status": "success", "current_mode": mode})

@card_bp.route('/api/save_card')
@cross_origin()
def save_card():
    global latest_combined_frame
    
    if latest_combined_frame is None:
        return jsonify({"status": "error", "message": "No frame available"}), 500

    save_dir = "saved_cards"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    filename = f"MagicCard_{timestamp}.jpg"
    filepath = os.path.join(save_dir, filename)
    
    # 直接保存刚才留底的图
    cv2.imwrite(filepath, latest_combined_frame)
    print(f"✨ 贺卡已保存: {filepath}")
    
    return send_file(filepath, as_attachment=True, download_name=filename)