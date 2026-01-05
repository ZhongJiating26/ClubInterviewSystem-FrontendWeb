# Windows Docker 部署说明

## 快速开始（3 步完成部署）

### 方法一：使用自动化脚本（推荐）

1. **下载源码**
   - 访问你的 GitHub 仓库
   - 点击 "Code" -> "Download ZIP"
   - 解压到任意目录（如 `C:\projects`）

2. **运行部署脚本**
   - 右键点击 `deploy.ps1` 文件
   - 选择 "使用 PowerShell 运行"
   - 按照提示操作

3. **访问应用**
   - 打开浏览器访问 `http://localhost:3000`

---

### 方法二：手动命令（PowerShell）

```powershell
# 1. 进入项目目录
cd C:\projects\ClubInterviewSystem-FrontendWeb

# 2. 启动 Docker Desktop（如果未启动）

# 3. 构建并启动
docker-compose up -d

# 4. 查看日志
docker-compose logs -f frontend
```

---

## 前置要求

### 1. 安装 Docker Desktop

下载地址：https://www.docker.com/products/docker-desktop

安装后启动 Docker Desktop

### 2. 验证安装

打开 PowerShell，运行：

```powershell
docker --version
docker-compose --version
```

---

## 配置后端 API 地址

**重要**：首次使用需要配置后端地址

### 步骤

1. 编辑 `src/api/request.ts` 文件

2. 修改 `baseURL`：
```typescript
baseURL: 'http://你的后端IP:8000'
```

3. 重新构建：
```powershell
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

## 常用命令

```powershell
# 查看容器状态
docker-compose ps

# 查看日志
docker-compose logs -f frontend

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 重新构建
docker-compose build --no-cache
docker-compose up -d
```

---

## 端口被占用？

### 检查端口占用
```powershell
netstat -ano | findstr :3000
```

### 修改端口

编辑 `docker-compose.yml`：
```yaml
ports:
  - "8080:3000"  # 将外部端口改为 8080
```

---

## 问题排查

### 1. 容器无法启动

```powershell
# 查看详细错误
docker-compose logs frontend

# 检查 Docker 状态
docker ps -a
```

### 2. 页面无法访问

```powershell
# 检查容器是否运行
docker ps | findstr frontend

# 查看日志
docker-compose logs -f --tail=50 frontend
```

### 3. 需要完全重置

```powershell
# 停止并删除容器
docker-compose down

# 删除镜像
docker rmi club-interview-frontend

# 重新构建
docker-compose build --no-cache
docker-compose up -d
```

---

## 更新部署

当 GitHub 上有更新时：

```powershell
cd C:\projects\ClubInterviewSystem-FrontendWeb

# 拉取最新代码
git pull

# 重新构建
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

## 卸载

```powershell
# 停止并删除容器
docker-compose down

# 删除镜像
docker rmi club-interview-frontend

# 删除项目文件
Remove-Item -Recurse -Force C:\projects\ClubInterviewSystem-FrontendWeb
```

---

## 支持

遇到问题请查看：
- [Docker 部署完整教程](./Docker部署教程.md)
- [项目 README](../README.md)
