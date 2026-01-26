import os
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# 1. 先初始化 app 和插件

# 这里的路径一定要对应你实际的 frontend 文件夹位置
frontend_folder = os.path.abspath("../frontend")

app = Flask(__name__,
            static_folder=os.path.join(frontend_folder, "static"),
            template_folder=frontend_folder)

# 确保静态文件的路由正确
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory(app.static_folder, path)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'magic_air_card_secret'
db = SQLAlchemy(app)

# 2. 定义模型 (直接写在这里或者确保 models 导入 db 正常)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# 3. 在 db 初始化之后再导入路由，防止循环引用
from routes.auth import auth_bp
from routes.card import card_bp

app.register_blueprint(auth_bp)
app.register_blueprint(card_bp)

@app.route('/')
def index():
    return send_from_directory(app.template_folder, 'index.html')

@app.route('/dashboard')
def dashboard():
    return send_from_directory(app.template_folder, 'dashboard.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)