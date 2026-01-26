# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all
import os
import mediapipe

# ========================================================
# 1. 暴力定位 MediaPipe 路径
# ========================================================
# 找到你电脑上 mediapipe 安装在哪里
mp_path = os.path.dirname(mediapipe.__file__)
print(f"📍 MediaPipe 安装路径: {mp_path}")

# ========================================================
# 2. 构造数据列表 (核心修复)
# ========================================================
# 自动收集所有依赖 (dll, pyd等)
mp_datas, mp_binaries, mp_hiddenimports = collect_all('mediapipe')

# 🛑 强制添加：把 modules 文件夹里的所有东西（不管后缀名）都搬过去
# 这一步是为了修复 FileNotFoundError
mp_manual_datas = [
    (os.path.join(mp_path, 'modules'), 'mediapipe/modules'),
    (os.path.join(mp_path, 'python'), 'mediapipe/python')
]

# 定位前端文件夹
current_dir = os.getcwd()
frontend_path = os.path.abspath(os.path.join(current_dir, '..', 'frontend'))

# 检查前端是否存在
if not os.path.exists(frontend_path):
    raise RuntimeError(f"❌ 找不到前端文件夹: {frontend_path}")

# 前端数据
frontend_datas = [ (frontend_path, 'frontend') ]

# 合并所有数据
all_datas = mp_datas + mp_manual_datas + frontend_datas

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=mp_binaries,
    datas=all_datas,  # 使用合并后的数据
    hiddenimports=mp_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MagicAirCard',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True, # 保持黑框，方便看日志
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MagicAirCard',
)