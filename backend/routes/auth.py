from flask import Blueprint, request, jsonify
# 注意：这里暂时不导入 User 模型，避免循环导入，或者在函数内部导入
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.json
    # 简化版逻辑
    return jsonify({"message": "User registered", "status": "success"})

@auth_bp.route('/api/login', methods=['POST'])
def login():
    return jsonify({"message": "Login successful", "status": "success", "user_id": 1})