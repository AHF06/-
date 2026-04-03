#!/usr/bin/env python
from app import create_app

# 创建应用
app = create_app('development')

if __name__ == '__main__':
    # 获取本机IP
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print(f"""
    ╔══════════════════════════════════════════════════════╗
    ║     🌾 作物病虫害检测系统 - 后端服务启动中...        ║
    ╠══════════════════════════════════════════════════════╣
    ║  本地访问: http://localhost:5000                     ║
    ║  局域网访问: http://{local_ip}:5000                    ║
    ║  健康检查: http://localhost:5000/api/health          ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )