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

```
## ✨ 核心功能 (Core Features)

- **🖐️ 高精度手势追踪**
  - 集成 **Google MediaPipe Hands** 框架，实时检测手部 **21 个 3D 关键点**。
  - 智能状态机：精准区分“绘制状态”（食指伸出）与“控制状态”（握拳停止/切换）。

- **🎨 创意绘图模式**
  - **标准模式 (Normal)**：经典单色笔触，适合书写与勾线。
  - **🌈 彩虹模式 (Rainbow)**：基于指尖屏幕坐标 $(x, y)$ 动态映射 RGB 颜色空间，实现随手势移动的渐变流光效果。
  - **🖌️ 3D 景深模式 (Pseudo-3D)**：通过计算“食指-拇指”的相对距离估算深度，动态调整线条粗细，模拟真实书写的压感与立体感。

- **🚀 极速性能体验 (Performance)**
  - **多线程优化**：自定义 `NoDelayCamera` 类实现**生产者-消费者模型**，分离视频读取与图像处理线程，彻底解决 OpenCV 缓冲区积压导致的画面高延迟与卡顿。
  - **算法加速**：针对实时性优化 MediaPipe 模型参数 (`model_complexity=0`)，在保证精度的同时大幅降低 CPU 占用。

- **💻 交互式 Web 创作中心**
  - **前后端分离架构**：前端 (HTML/JS) 负责交互，后端 (Flask) 负责 AI 推理，通过 RESTful API 通信。
  - **功能完备**：支持**实时 MJPEG 视频流预览**、一键清空画布、作品本地保存 (Save to Local)、模式热切换（无刷新）。

## 🛠️ 技术栈 (Tech Stack)

| 模块 (Module) | 技术/库 (Technology) | 用途说明 (Description) |
| :--- | :--- | :--- |
| **Backend** | **Python 3.10** | 核心开发语言，保证 MediaPipe 兼容性 |
| | **Flask** | 轻量级 Web 框架，提供 API 和视频流服务 |
| | **Flask-CORS** | 解决前后端分离架构下的跨域资源共享问题 |
| **AI & CV** | **MediaPipe** | 高性能手部骨架提取与关键点检测 |
| | **OpenCV (cv2)** | 视频流捕获、图像预处理、透明画布叠加融合 |
| | **NumPy** | 高效矩阵运算，处理像素级图像数据 |
| **Frontend** | **HTML5 / CSS3** | 页面结构与样式 (Tailwind CSS) |
| | **JavaScript (ES6+)** | 处理用户交互，使用 `Fetch API` 发送控制指令 |
| **Data** | **SQLite** | 轻量级数据库，存储用户信息与作品记录 |
