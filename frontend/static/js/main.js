function setMode(mode) {
    console.log("切换模式到:", mode);
    fetch('http://localhost:5000/api/set_mode', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mode: mode })
    })
    .then(response => response.json())
    .then(data => {
        alert("模式已切换为: " + mode);
    });
}

function clearCanvas() {
    fetch('http://localhost:5000/api/clear', { method: 'POST' })
    .then(response => response.json())
    .then(data => {
        console.log("画布已清空");
    });
}

function saveCard() {
    alert("✨ 贺卡保存成功！正在下载...");
    // 实际项目中可以这里调用 canvas.toDataURL 并保存
}