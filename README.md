# MagicAirCard-for-kids
# 🎨 Magic Air Card (空气贺卡)

**Magic Air Card** 是一个基于计算机视觉的创新型 Web 应用程序，允许用户通过手势在空气中绘制图案并生成电子贺卡。

本项目采用 **前后端分离** 架构，后端使用 **Flask** + **MediaPipe** 进行手势识别与图像处理，前端使用 **HTML5/JS** 进行交互展示。支持实时手势追踪、彩虹笔触、3D 伪厚度绘制等功能。

---

## 📂 项目目录结构

```text
magic_air_card/
│
├── backend/                  # 后端核心代码
│   ├── app.py                # Flask 启动主程序 (入口)
│   ├── camera.py             # 多线程无延迟摄像头类 (性能优化)
│   ├── routes/               # API 路由模块
│   │   ├── auth.py           # 登录注册接口
│   │   ├── card.py           # 核心业务接口 (绘图流、模式切换、清空)
│   │   └── user.py           # 用户信息接口
│   ├── models/               # 数据库模型
│   │   ├── user.py           # User 模型
│   │   └── card.py           # Card 模型
│   ├── mediapipe_controller/ # 视觉算法控制层
│   │   ├── hand_tracking.py  # MediaPipe 手势核心逻辑 (含彩虹/3D模式)
│   │   ├── draw_utils.py     # 辅助绘图工具
│   │   └── canvas_3d.py      # 伪3D画笔算法
│   └── database.db           # SQLite 数据库文件 (自动生成)
│
├── frontend/                 # 前端静态资源
│   ├── index.html            # 登录/注册界面
│   ├── dashboard.html        # 创作中心 (视频流画板)
│   ├── static/
│   │   ├── css/              # 样式文件 (Tailwind/Custom)
│   │   ├── js/               # 前端逻辑
│   │   │   ├── main.js       # 核心交互 (Fetch API, 按钮控制)
│   │   │   ├── canvas.js     # Canvas 渲染辅助
│   │   │   └── websocket.js  # WebSocket (可选扩展)
│   │   └── img/              # 图标资源
│
├── README.md                 # 项目说明文档
├── requirements.txt          # Python 依赖列表
└── .gitignore                # Git 忽略配置

