# 社团面试系统前端 Docker 部署教程

> 本文档提供详细的、手把手的 Docker 部署指南，适用于开发和生产环境。

**技术栈**: Node.js + serve（无需 Nginx）

## 📋 目录

1. [环境准备](#环境准备)
2. [从 GitHub 部署（推荐）](#从-github-部署)
3. [快速开始](#快速开始)
4. [详细部署步骤](#详细部署步骤)
5. [配置说明](#配置说明)
6. [常见问题排查](#常见问题排查)
7. [生产环境优化](#生产环境优化)
8. [CI/CD 集成](#cicd-集成)

---

## 🔧 环境准备

### 1. 安装 Docker

#### macOS / Windows

下载并安装 [Docker Desktop](https://www.docker.com/products/docker-desktop/):

```bash
# 验证安装
docker --version
docker-compose --version
```

#### Linux (Ubuntu/Debian)

```bash
# 更新包索引
sudo apt-get update

# 安装 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 安装 Docker Compose
sudo apt-get install docker-compose

# 将当前用户添加到 docker 组（免 sudo）
sudo usermod -aG docker $USER

# 重新登录或运行
newgrp docker

# 验证安装
docker --version
docker-compose --version
```

### 2. 准备项目文件

确保你的项目目录包含以下文件：

```
ClubInterviewSystem-FrontendWeb/
├── Dockerfile                  # Docker 构建文件 ✅
├── .dockerignore              # Docker 忽略文件 ✅
├── docker-compose.yml         # Docker Compose 配置 ✅
├── package.json
├── vite.config.ts
└── src/
```

---

## 📥 从 GitHub 部署（推荐）

> **适用于新服务器部署**：直接从 GitHub 下载源码并部署

### 方法一：使用 PowerShell（推荐）

#### 1. 打开 PowerShell

在 Windows 上按 `Win + X`，选择 "Windows PowerShell" 或 "终端"

#### 2. 创建项目目录

```powershell
# 创建目录
mkdir C:\projects
cd C:\projects
```

#### 3. 下载源码

```powershell
# 方式 A: 使用 curl（Windows 10+ 自带）
curl -L -o frontend.zip https://github.com/你的用户名/ClubInterviewSystem-FrontendWeb/archive/refs/heads/main.zip

# 方式 B: 使用 Invoke-WebRequest（PowerShell 自带）
Invoke-WebRequest -Uri "https://github.com/你的用户名/ClubInterviewSystem-FrontendWeb/archive/refs/heads/main.zip" -OutFile "frontend.zip"

# 方式 C: 如果有 Git，直接克隆（推荐）
git clone https://github.com/你的用户名/ClubInterviewSystem-FrontendWeb.git
cd ClubInterviewSystem-FrontendWeb
```

#### 4. 解压文件

如果使用 ZIP 下载方式：

```powershell
# 解压到当前目录
Expand-Archive -Path frontend.zip -DestinationPath . -Force

# 进入解压后的目录
cd ClubInterviewSystem-FrontendWeb-main
```

#### 5. 验证文件

```powershell
# 查看目录内容
dir

# 确认关键文件存在
dir Dockerfile
dir docker-compose.yml
dir package.json
```

#### 6. 构建并启动

```powershell
# 构建并启动容器
docker-compose up -d

# 查看日志
docker-compose logs -f frontend
```

#### 7. 访问应用

打开浏览器访问：`http://localhost:3000`

---

### 方法二：使用命令提示符 (CMD)

#### 1. 打开 CMD

按 `Win + R`，输入 `cmd`，回车

#### 2. 创建项目目录并下载

```cmd
mkdir C:\projects
cd C:\projects

# 下载源码（需要安装 curl 或 wget）
curl -L -o frontend.zip https://github.com/你的用户名/ClubInterviewSystem-FrontendWeb/archive/refs/heads/main.zip
```

#### 3. 解压并部署

```cmd
# 使用 PowerShell 解压
powershell -Command "Expand-Archive -Path frontend.zip -DestinationPath . -Force"

# 进入目录
cd ClubInterviewSystem-FrontendWeb-main

# 构建并启动
docker-compose up -d
```

---

### 方法三：使用 Git Bash（推荐）

#### 1. 打开 Git Bash

如果安装了 Git for Windows，右键菜单选择 "Git Bash Here"

#### 2. 克隆或下载源码

```bash
# 创建目录
mkdir -p ~/projects
cd ~/projects

# 方式 A: Git 克隆（推荐）
git clone https://github.com/你的用户名/ClubInterviewSystem-FrontendWeb.git
cd ClubInterviewSystem-FrontendWeb

# 方式 B: 下载 ZIP
wget https://github.com/你的用户名/ClubInterviewSystem-FrontendWeb/archive/refs/heads/main.zip
unzip main.zip
cd ClubInterviewSystem-FrontendWeb-main
```

#### 3. 构建并启动

```bash
# 构建并启动
docker-compose up -d

# 查看日志
docker-compose logs -f frontend
```

---

### 完整一键部署脚本（PowerShell）

创建 `deploy.ps1` 文件：

```powershell
# 从 GitHub 部署前端项目

# 配置
$GITHUB_REPO = "https://github.com/你的用户名/ClubInterviewSystem-FrontendWeb"
$PROJECT_DIR = "C:\projects\ClubInterviewSystem-FrontendWeb"

Write-Host "=== 社团面试系统前端部署 ===" -ForegroundColor Green

# 1. 创建目录
Write-Host "1. 创建项目目录..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "C:\projects" | Out-Null
Set-Location "C:\projects"

# 2. 下载源码
Write-Host "2. 从 GitHub 下载源码..." -ForegroundColor Yellow
if (Test-Path "ClubInterviewSystem-FrontendWeb") {
    Write-Host "   项目目录已存在，删除旧版本..." -ForegroundColor Cyan
    Remove-Item -Recurse -Force "ClubInterviewSystem-FrontendWeb"
}

# 使用 Git 克隆
git clone $GITHUB_REPO
if ($LASTEXITCODE -ne 0) {
    Write-Host "   Git 克隆失败，尝试下载 ZIP..." -ForegroundColor Red
    Invoke-WebRequest -Uri "$GITHUB_REPO/archive/refs/heads/main.zip" -OutFile "frontend.zip"
    Expand-Archive -Path "frontend.zip" -DestinationPath . -Force
    Move-Item -Path "ClubInterviewSystem-FrontendWeb-main" -Destination "ClubInterviewSystem-FrontendWeb"
    Remove-Item "frontend.zip"
}

Set-Location "ClubInterviewSystem-FrontendWeb"

# 3. 验证文件
Write-Host "3. 验证项目文件..." -ForegroundColor Yellow
if (!(Test-Path "Dockerfile")) {
    Write-Host "   错误：Dockerfile 不存在！" -ForegroundColor Red
    exit 1
}
if (!(Test-Path "docker-compose.yml")) {
    Write-Host "   错误：docker-compose.yml 不存在！" -ForegroundColor Red
    exit 1
}

# 4. 构建并启动
Write-Host "4. 构建 Docker 镜像..." -ForegroundColor Yellow
docker-compose build

Write-Host "5. 启动容器..." -ForegroundColor Yellow
docker-compose up -d

# 6. 等待容器启动
Write-Host "6. 等待服务启动..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# 7. 检查状态
Write-Host "7. 检查服务状态..." -ForegroundColor Yellow
docker-compose ps

# 8. 显示日志
Write-Host "`n=== 查看日志（Ctrl+C 退出）===" -ForegroundColor Green
docker-compose logs -f frontend
```

**使用方法**：

```powershell
# 保存上面的代码为 deploy.ps1
# 右键点击文件 -> 使用 PowerShell 运行

# 或者在 PowerShell 中运行
.\deploy.ps1
```

---

### 配置后端 API 地址

**重要**：部署后需要修改后端 API 地址

#### 临时测试（直接访问）

修改 `src/api/request.ts`：

```typescript
const request = axios.create({
  baseURL: 'http://你的后端服务器IP:8000', // 修改为实际地址
  timeout: 10000
})
```

重新构建：

```powershell
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

### 常见问题

#### 1. 端口被占用

```powershell
# 查看占用 3000 端口的进程
netstat -ano | findstr :3000

# 停止占用端口的进程
taskkill /PID <进程ID> /F

# 或者修改 docker-compose.yml 使用其他端口
```

#### 2. Git 未安装

下载并安装 Git：https://git-scm.com/download/win

或者直接下载 ZIP：访问 GitHub 页面，点击 "Code" -> "Download ZIP"

#### 3. 解压失败

确保使用 PowerShell 的 `Expand-Archive` 命令，或使用 7-Zip 等第三方工具。

#### 4. Docker 未启动

打开 Docker Desktop，确保引擎正在运行。

---

## 🚀 快速开始

### 本地已有源码

如果你已经在本地有项目源码：

### 步骤 1: 配置后端 API 地址

在部署前，需要确认前端如何访问后端 API。

#### 直接访问外部后端（推荐）

如果你的后端部署在其他服务器，修改 `src/api/request.ts`：

```typescript
const request = axios.create({
  baseURL: 'http://your-backend-server:8000', // 修改为实际后端地址
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})
```

或者使用环境变量（需要配置 Vite）：

```typescript
const request = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: 10000
})
```

### 步骤 2: 构建 Docker 镜像

#### 方式 A: 使用 docker-compose（推荐）

```bash
# 构建镜像
docker-compose build

# 查看镜像
docker images | grep club-interview-frontend
```

#### 方式 B: 手动构建

```bash
# 构建镜像
docker build -t club-interview-frontend:latest .

# 查看镜像
docker images | grep club-interview-frontend
```

### 步骤 3: 运行容器

#### 开发环境

```bash
# 使用 docker-compose
docker-compose up -d

# 查看运行状态
docker-compose ps

# 查看日志
docker-compose logs -f frontend
```

#### 生产环境（自定义配置）

```bash
# 运行容器，映射到 80 端口
docker run -d \
  --name club-interview-frontend \
  -p 80:3000 \
  --restart unless-stopped \
  club-interview-frontend:latest

# 查看日志
docker logs -f club-interview-frontend
```

### 步骤 4: 验证部署

```bash
# 1. 检查容器状态
docker ps | grep club-interview-frontend

# 2. 查看容器日志
docker logs club-interview-frontend

# 3. 测试访问
curl http://localhost:3000

# 4. 浏览器访问
# 打开: http://localhost:3000
```

### 步骤 5: 与其他服务集成

如果你的系统包含后端、MySQL、RustFS 等服务，可以在根目录创建完整的 `docker-compose.yml`：

```yaml
version: '3.8'

services:
  # 前端服务
  frontend:
    build:
      context: ./ClubInterviewSystem-FrontendWeb
      dockerfile: Dockerfile
    container_name: club-interview-frontend
    ports:
      - "3000:3000"
    restart: unless-stopped
    networks:
      - club-interview-network
    depends_on:
      - backend

  # 后端服务（示例）
  # backend:
  #   build: ./backend
  #   container_name: club-interview-backend
  #   ports:
  #     - "8000:8000"
  #   environment:
  #     - DATABASE_URL=mysql://user:pass@mysql:3306/dbname
  #   networks:
  #     - club-interview-network
  #   depends_on:
  #     - mysql

  # MySQL 数据库（示例）
  # mysql:
  #   image: mysql:8.0
  #   container_name: club-interview-mysql
  #   environment:
  #     MYSQL_ROOT_PASSWORD: rootpass
  #     MYSQL_DATABASE: club_interview
  #     MYSQL_USER: user
  #     MYSQL_PASSWORD: pass
  #   volumes:
  #     - mysql-data:/var/lib/mysql
  #   networks:
  #     - club-interview-network

networks:
  club-interview-network:
    driver: bridge

# volumes:
#   mysql-data:
```

---

## ⚙️ 配置说明

### 端口配置

修改 `docker-compose.yml` 中的端口映射：

```yaml
ports:
  - "外部端口:3000"  # 例如 "8080:3000"
```

### 环境变量

如果需要使用环境变量，修改 `Dockerfile`：

```dockerfile
# 在构建阶段传递参数
ARG VITE_API_URL=http://localhost:8000

# 在运行时设置环境变量
ENV NODE_ENV=production
```

修改 `docker-compose.yml`：

```yaml
services:
  frontend:
    build:
      args:
        - VITE_API_URL=http://production-api:8000
    environment:
      - NODE_ENV=production
```

### Serve 配置

`serve` 是一个轻量级的静态文件服务器，默认配置已经足够使用。如果需要自定义，可以修改 Dockerfile 中的 CMD：

```dockerfile
# 更多 serve 选项
CMD ["serve", "-s", "dist", "-l", "3000", "--no-clipboard"]
```

---

## 🐛 常见问题排查

### 问题 1: 容器启动失败

**症状**: `docker-compose up` 后容器立即退出

**排查步骤**:

```bash
# 1. 查看容器日志
docker-compose logs frontend

# 2. 检查构建是否成功
docker images | grep club-interview-frontend

# 3. 手动运行容器查看详细错误
docker run -it --rm club-interview-frontend:latest sh
```

**常见原因**:
- Dockerfile 构建失败
- 端口被占用
- 依赖安装问题

### 问题 2: 页面 404

**症状**: 访问页面显示 404 Not Found

**解决方案**:

1. 检查构建产物是否存在：

```bash
# 进入容器查看
docker exec -it club-interview-frontend sh
ls -la /app/dist
```

2. 检查 serve 是否正常运行：

```bash
# 查看进程
docker exec club-interview-frontend ps aux

# 测试内部访问
docker exec club-interview-frontend wget -O- http://localhost:3000
```

3. 重新构建：

```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### 问题 3: API 请求失败

**症状**: 前端页面可以访问，但 API 请求失败

**解决方案**:

1. 检查后端服务是否运行：

```bash
# 测试后端连接（如果后端在同一网络）
docker exec club-interview-frontend wget -O- http://backend:8000/api/health
```

2. 检查网络配置：

```bash
# 查看网络
docker network ls
docker network inspect club-interview-network

# 确保前后端在同一网络
docker-compose ps
```

3. 修改 API 地址配置：

- 在代码中修改 `baseURL`
- 或使用环境变量

### 问题 4: 端口被占用

**症状**: 启动时报错 `port is already allocated`

**解决方案**:

```bash
# 1. 查看占用端口的进程
sudo lsof -i :3000

# 2. 停止占用端口的容器或进程
docker stop <container-id>

# 3. 或者修改 docker-compose.yml 使用其他端口
ports:
  - "8080:3000"  # 使用 8080 端口
```

### 问题 5: 页面样式丢失

**症状**: 页面可以访问但样式混乱

**解决方案**:

```bash
# 1. 检查静态资源
docker exec club-interview-frontend ls -la /app/dist/assets/

# 2. 检查构建日志
docker-compose logs frontend | grep -i error

# 3. 清除缓存重新构建
docker-compose down
docker system prune -a
docker-compose build --no-cache
docker-compose up -d
```

---

## 🚀 生产环境优化

### 1. 多阶段构建优化

已实现的 `Dockerfile` 使用了多阶段构建，确保：
- 构建产物体积小
- 最终镜像只包含运行时必需文件
- 不包含开发依赖

### 2. 镜像优化

```dockerfile
# 使用 alpine 基础镜像（体积小）
FROM node:20-alpine AS builder
FROM node:20-alpine

# 清理不必要的文件
RUN apk add --no-cache curl && \
    rm -rf /var/cache/apk/*
```

### 3. 性能优化

使用 `serve` 的优势：
- 轻量级，资源占用少
- 自动 gzip 压缩
- 支持 SPA 路由
- 自动缓存静态资源

### 4. 健康检查

在 `docker-compose.yml` 中添加（已配置）：

```yaml
services:
  frontend:
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:3000"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### 5. 日志管理

```yaml
services:
  frontend:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### 6. 资源限制

```yaml
services:
  frontend:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

---

## 🔄 CI/CD 集成

### GitHub Actions 示例

创建 `.github/workflows/deploy.yml`：

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2

    - name: Login to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}

    - name: Build and push
      uses: docker/build-push-action@v4
      with:
        context: .
        file: ./Dockerfile
        push: true
        tags: |
          yourusername/club-interview-frontend:latest
          yourusername/club-interview-frontend:${{ github.sha }}

    - name: Deploy to server
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.SERVER_HOST }}
        username: ${{ secrets.SERVER_USER }}
        key: ${{ secrets.SSH_PRIVATE_KEY }}
        script: |
          cd /path/to/app
          docker-compose pull
          docker-compose up -d
          docker image prune -f
```

### GitLab CI 示例

创建 `.gitlab-ci.yml`：

```yaml
stages:
  - build
  - deploy

build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t registry.gitlab.com/yourgroup/club-interview-frontend:$CI_COMMIT_SHA .
    - docker login -u gitlab-ci-token -p $CI_JOB_TOKEN registry.gitlab.com
    - docker push registry.gitlab.com/yourgroup/club-interview-frontend:$CI_COMMIT_SHA

deploy:
  stage: deploy
  image: alpine:latest
  script:
    - apk add --no-cache docker-compose
    - docker-compose pull
    - docker-compose up -d
  only:
    - main
```

---

## 📝 维护命令

### 日常维护

```bash
# 查看容器状态
docker-compose ps

# 查看资源使用情况
docker stats club-interview-frontend

# 查看日志
docker-compose logs -f --tail=100 frontend

# 重启服务
docker-compose restart frontend

# 更新镜像
docker-compose pull
docker-compose up -d

# 清理未使用的资源
docker system prune -a
```

### 备份与恢复

```bash
# 导出镜像
docker save club-interview-frontend:latest | gzip > frontend-backup.tar.gz

# 导入镜像
gunzip -c frontend-backup.tar.gz | docker load
```

---

## 🔐 安全建议

1. **不要在镜像中包含敏感信息**
   - 使用环境变量管理密钥
   - 不要提交 `.env` 文件到 Git

2. **定期更新基础镜像**
   ```bash
   docker pull node:20-alpine
   docker-compose build --no-cache
   ```

3. **最小权限原则**
   - 只开放必要的端口
   - 不要在容器内运行不必要的进程

4. **生产环境部署**
   - 使用反向代理（如 Nginx、Traefik）处理 HTTPS
   - 配置防火墙规则
   - 定期更新依赖

---

## 📞 支持

如果遇到问题，请检查：

1. Docker 版本是否满足要求（建议 20.x+）
2. 端口是否被占用
3. 网络连接是否正常
4. 防火墙设置是否正确

更多帮助请参考：
- [Docker 官方文档](https://docs.docker.com/)
- [serve 包文档](https://www.npmjs.com/package/serve)
- [项目 GitHub Issues](https://github.com/your-repo/issues)

---

**最后更新**: 2026-01-05
