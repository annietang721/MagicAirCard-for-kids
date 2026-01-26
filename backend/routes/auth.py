from flask import Blueprint, request, jsonify
# 👇 必须引入这个，解决前后端端口不一样的问题
from flask_cors import cross_origin 

# 注意：这里暂时不导入 User 模型，避免循环导入，或者在函数内部导入
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/register', methods=['POST'])
@cross_origin() # 👈 加上这个通行证
def register():
    data = request.json
    # 简化版逻辑：直接告诉前端注册成功
    return jsonify({"message": "User registered", "status": "success"})

@auth_bp.route('/api/login', methods=['POST'])
@cross_origin() # 👈 加上这个通行证，否则前端fetch会报错
def login():
    # 这里将来可以加：if data['username'] == 'admin' ...
    
    # 直接返回成功信号和假的用户ID
    return jsonify({
        "message": "Login successful", 
        "status": "success", 
        "user_id": 1
    })