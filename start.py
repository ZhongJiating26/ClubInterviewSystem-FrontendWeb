#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
一键启动前后端服务
"""
import os
import sys
import subprocess
import time
import platform
import shutil
from pathlib import Path

# 获取项目根目录
PROJECT_ROOT = Path(__file__).parent.absolute()
BACKEND_DIR = PROJECT_ROOT / "backend"
FRONTEND_DIR = PROJECT_ROOT / "frontend"

def check_backend_dependencies():
    """检查后端依赖"""
    print("检查后端依赖...")
    try:
        import fastapi
        import sqlmodel
        import bcrypt
        print("✓ 后端依赖已安装")
        return True
    except ImportError as e:
        print(f"✗ 后端依赖缺失: {e}")
        print("请运行: cd backend && pip install -r requirements.txt")
        return False

def check_npm():
    """检查 npm 是否可用"""
    npm_path = shutil.which("npm")
    if npm_path:
        return npm_path
    return None

def check_frontend_dependencies():
    """检查前端依赖"""
    print("检查前端依赖...")
    
    # 检查 npm
    npm_path = check_npm()
    if not npm_path:
        print("✗ 未找到 npm 命令")
        print("请确保 Node.js 已安装并添加到 PATH")
        return False
    
    node_modules = FRONTEND_DIR / "node_modules"
    if node_modules.exists():
        print("✓ 前端依赖已安装")
        return True
    else:
        print("✗ 前端依赖未安装")
        print("请运行: cd frontend && npm install")
        return False

def create_default_users():
    """创建预制账号"""
    print("\n正在创建预制账号...")
    script_path = BACKEND_DIR / "scripts" / "create_default_users.py"
    
    if not script_path.exists():
        print("⚠ 警告: 未找到预制账号脚本，跳过创建")
        return
    
    try:
        os.chdir(BACKEND_DIR)
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print("✓ 预制账号创建完成")
        else:
            print(f"⚠ 预制账号创建警告: {result.stderr}")
    except subprocess.TimeoutExpired:
        print("⚠ 警告: 创建预制账号超时，跳过")
    except Exception as e:
        print(f"⚠ 警告: 创建预制账号失败: {e}")

def start_backend():
    """启动后端服务"""
    print("\n" + "="*50)
    print("启动后端服务...")
    print("="*50)
    
    os.chdir(BACKEND_DIR)
    
    # 检查 .env 文件
    env_file = BACKEND_DIR / ".env"
    if not env_file.exists():
        print("⚠ 警告: 未找到 .env 文件，使用默认配置")
    
    # 自动创建预制账号
    create_default_users()
    
    # 启动 uvicorn
    cmd = [
        sys.executable, "-m", "uvicorn",
        "app.main:app",
        "--reload",
        "--host", "0.0.0.0",
        "--port", "8000"
    ]
    
    print(f"\n执行命令: {' '.join(cmd)}")
    print(f"后端服务地址: http://localhost:8000")
    print(f"API 文档: http://localhost:8000/docs")
    print("\n按 Ctrl+C 停止后端服务\n")
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n后端服务已停止")

def start_frontend():
    """启动前端服务"""
    print("\n" + "="*50)
    print("启动前端服务...")
    print("="*50)
    
    # 检查 npm
    npm_path = check_npm()
    if not npm_path:
        print("✗ 错误: 未找到 npm 命令")
        print("请确保 Node.js 已安装并添加到 PATH")
        return
    
    os.chdir(FRONTEND_DIR)
    
    # 检查 .env.local 文件
    env_file = FRONTEND_DIR / ".env.local"
    if not env_file.exists():
        print("⚠ 警告: 未找到 .env.local 文件")
        print("请创建 .env.local 文件，内容: NEXT_PUBLIC_API_URL=http://localhost:8000")
    
    # 启动 Next.js
    # Windows 上需要使用 shell=True
    is_windows = platform.system() == "Windows"
    if is_windows:
        cmd = "npm run dev"
        print(f"执行命令: {cmd}")
    else:
        cmd = ["npm", "run", "dev"]
        print(f"执行命令: {' '.join(cmd)}")
    
    print(f"前端服务地址: http://localhost:3000")
    print("\n按 Ctrl+C 停止前端服务\n")
    
    try:
        if is_windows:
            subprocess.run(cmd, shell=True, check=True)
        else:
            subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n前端服务已停止")
    except FileNotFoundError:
        print("✗ 错误: 无法执行 npm 命令")
        print("请确保 Node.js 已正确安装")

def start_both():
    """同时启动前后端（使用线程）"""
    import threading
    
    print("\n" + "="*60)
    print("同时启动前后端服务")
    print("="*60)
    
    # 检查依赖
    if not check_backend_dependencies():
        return
    if not check_frontend_dependencies():
        return
    
    # 创建线程（Windows 上多进程可能有问题，改用线程）
    backend_thread = threading.Thread(target=start_backend, name="Backend", daemon=True)
    frontend_thread = threading.Thread(target=start_frontend, name="Frontend", daemon=True)
    
    try:
        # 启动后端
        print("\n启动后端线程...")
        backend_thread.start()
        time.sleep(2)  # 等待后端启动
        
        # 启动前端
        print("\n启动前端线程...")
        frontend_thread.start()
        
        print("\n" + "="*60)
        print("前后端服务已启动")
        print("="*60)
        print("后端: http://localhost:8000")
        print("前端: http://localhost:3000")
        print("\n按 Ctrl+C 停止所有服务\n")
        
        # 等待线程
        backend_thread.join()
        frontend_thread.join()
        
    except KeyboardInterrupt:
        print("\n\n正在停止服务...")
        print("所有服务已停止")

def main():
    """主函数"""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "backend" or command == "back" or command == "b":
            if check_backend_dependencies():
                start_backend()
        elif command == "frontend" or command == "front" or command == "f":
            if check_frontend_dependencies():
                start_frontend()
        elif command == "both" or command == "all" or command == "a":
            start_both()
        else:
            print_help()
    else:
        print_help()

def print_help():
    """打印帮助信息"""
    print("""
使用方法:
    python start.py [command]

命令:
    backend, back, b    启动后端服务 (http://localhost:8000)
    frontend, front, f  启动前端服务 (http://localhost:3000)
    both, all, a        同时启动前后端服务

示例:
    python start.py backend    # 只启动后端
    python start.py frontend   # 只启动前端
    python start.py both       # 同时启动前后端
    python start.py            # 显示帮助信息

注意:
    - 首次运行前，请确保已安装依赖:
      * 后端: cd backend && pip install -r requirements.txt
      * 前端: cd frontend && npm install
    
    - 确保已配置环境变量:
      * 后端: backend/.env
      * 前端: frontend/.env.local
    
    - 启动后端时会自动创建预制账号:
      * 普通学生: 13800000001 / student123
      * 系统管理员: 13800000000 / admin123
    """)

if __name__ == "__main__":
    main()

