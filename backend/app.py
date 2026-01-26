import os
import sys  # 👈 新增：用于判断系统环境
import webbrowser  # 👈 新增：用于自动打开浏览器
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# === 1. 核心修改：智能路径判断 ===
# 这段逻辑保证了无论你是直接跑代码，还是打包成 exe，都能找到 frontend
if getattr(sys, 'frozen', False):
    # 📦 打包模式 (Exe Mode)
    # 路径就是 exe 文件所在的目录
    base_dir = os.path.dirname(sys.executable)
    # 我们约定：把 frontend 文件夹放在 exe 旁边
    frontend_folder = os.path.join(base_dir, "frontend")
    db_path = os.path.join(base_dir, "database.db")
else:
    # 💻 开发模式 (Dev Mode)
    # 路径是 app.py 所在的目录
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # 开发时 frontend 在上一级
    frontend_folder = os.path.join(base_dir, "..", "frontend")
    db_path = os.path.join(base_dir, "database.db")

# 打印一下路径，方便调试
print(f"✨ 当前模式: {'EXE打包版' if getattr(sys, 'frozen', False) else '开发版'}")
print(f"📂 前端路径: {frontend_folder}")

# === 初始化 Flask ===
app = Flask(__name__,
            static_folder=os.path.join(frontend_folder, "static"),
            template_folder=frontend_folder)

# 确保静态文件的路由正确
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory(app.static_folder, path)

CORS(app, resources={r"/*": {"origins": "*"}})

# 配置数据库路径 (使用绝对路径，防止报错)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'magic_air_card_secret'
db = SQLAlchemy(app)

# 2. 定义模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# 3. 导入路由
# 注意：确保 routes 文件夹里的文件没有写死绝对路径
from routes.auth import auth_bp
from routes.card import card_bp

app.register_blueprint(auth_bp)
app.register_blueprint(card_bp)

# === 路由部分 ===
@app.route('/')
def index():
    return send_from_directory(app.template_folder, 'index.html')

@app.route('/dashboard.html') # 👈 这里加个后缀兼容
def dashboard_html():
    return send_from_directory(app.template_folder, 'dashboard.html')

@app.route('/dashboard')
def dashboard():
    return send_from_directory(app.template_folder, 'dashboard.html')

# ... 上面的代码都不用动 ...

if __name__ == '__main__':
    try:
        # === 启动逻辑 ===
        with app.app_context():
            db.create_all()
        
        # 自动打开浏览器
        from threading import Timer
        def open_browser():
            webbrowser.open_new('http://localhost:5000/')
        
        Timer(1, open_browser).start()

        print("🚀 服务启动中... (如果窗口闪退，请查看下方报错)")
        # 注意：打包后的 exe 不要开 debug=True，否则会报错
        app.run(host='0.0.0.0', port=5000, debug=False)

    except Exception as e:
        # === 🛑 只有出错才会运行这里 🛑 ===
        import traceback
        print("\n" + "="*50)
        print("🔥🔥🔥 程序崩溃了！报错信息如下：")
        print("="*50)
        traceback.print_exc()  # 打印具体的红色报错
        print("="*50)
        # 👇 这行代码会让黑框框停住，直到你按回车
        input("\n按回车键退出...")