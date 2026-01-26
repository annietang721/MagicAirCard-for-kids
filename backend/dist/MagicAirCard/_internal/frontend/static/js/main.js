const API_BASE = 'http://localhost:5000'; // 统一管理地址，以后改端口只改这里

// 1. 切换模式
function setMode(mode) {
    console.log("正在请求切换模式到:", mode);
    
    fetch(`${API_BASE}/api/set_mode`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ mode: mode })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('网络响应异常');
        }
        return response.json();
    })
    .then(data => {
        // 成功切换，给个小提示（或者只在控制台输出，避免弹窗太烦）
        console.log("模式切换成功:", data);
        // 如果想弹窗提示可以解开下面这行
        // alert("✨ 已切换到: " + (mode === 'normal' ? '标准模式' : mode === 'rainbow' ? '彩虹模式' : '3D模式'));
    })
    .catch(error => {
        console.error('切换模式失败:', error);
        alert("❌ 切换失败，请检查后端(5000端口)是否开启！");
    });
}

// 2. 清空画布
function clearCanvas() {
    fetch(`${API_BASE}/api/clear`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        console.log("画布已清空");
        // 可以加一个临时的视觉反馈，比如让按钮闪一下
    })
    .catch(error => {
        console.error('清空失败:', error);
    });
}

// 3. ✨ 保存贺卡 (真正实现下载功能)
function saveCard() {
    // 方案：直接让浏览器访问下载链接，后端触发文件下载
    const downloadUrl = `${API_BASE}/api/save_card`;
    
    // 创建一个临时的 a 标签来触发下载
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = `MagicCard_${new Date().getTime()}.jpg`; // 试图指定文件名
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    console.log("正在请求下载贺卡...");
}