from flask import Blueprint, Response, jsonify, request
from flask_cors import cross_origin
import cv2
import numpy as np
# 确保你的路径能找到 mediapipe_controller
from mediapipe_controller.hand_tracking import HandTracker

card_bp = Blueprint('card', __name__)
tracker = HandTracker()
cap = cv2.VideoCapture(0)
# 🛠️ 新增这一行：设置缓存区大小为 1
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
canvas = np.zeros((480, 640, 3), dtype=np.uint8)

def gen_frames():
    global canvas
    while True:
        success, frame = cap.read()
        if not success: break
        
        frame = cv2.flip(frame, 1)
        # 这里的 process 需要对应你 hand_tracking.py 里的函数名
        frame, canvas, gest = tracker.get_frame_and_canvas(frame, canvas)
        combined = cv2.addWeighted(frame, 0.3, canvas, 0.7, 0)
        ret, buffer = cv2.imencode('.jpg', combined)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@card_bp.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@card_bp.route('/api/clear', methods=['POST'])
def clear_canvas():
    global canvas
    canvas = np.zeros((480, 640, 3), dtype=np.uint8)
    return jsonify({"status": "cleared"})
# === 👇 请把这段代码加到 card.py 的最后面 👇 ===

@card_bp.route('/api/set_mode', methods=['POST'])
@cross_origin()
def set_mode():
    data = request.json
    mode = data.get('mode', 'normal')
    # 假设你的 tracker 对象里有一个 mode 属性或者 set_mode 方法
    # 如果 tracker.mode 报错，请检查 mediapipe_controller/hand_tracking.py
    if hasattr(tracker, 'mode'):
        tracker.mode = mode
    else:
        # 如果 tracker 没有 mode 属性，可能是变量名不一样，这里做个备用处理
        print(f"Warning: Tracker does not support mode switching to {mode}")
    
    return jsonify({"status": "success", "current_mode": mode})