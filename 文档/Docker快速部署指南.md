# Docker 快速部署指南

> 5 分钟快速部署社团面试系统前端

**技术栈**: Node.js + serve（无需 Nginx）

## 📥 从 GitHub 部署（新服务器）

### Windows PowerShell（最简单）

```powershell
# 1. 创建目录并进入
mkdir C:\projects
cd C:\projects

# 2. 克隆源码（修改为你的 GitHub 地址）
git clone https://github.com/你的用户名/ClubInterviewSystem-FrontendWeb.git
cd ClubInterviewSystem-FrontendWeb

# 3. 构建并启动
docker-compose up -d

# 4. 查看日志
docker-compose logs -f frontend
```

### Windows CMD（无 Git）

```cmd
mkdir C:\projects
cd C:\projects

# 下载源码 ZIP
curl -L -o frontend.zip https://github.com/你的用户名/ClubInterviewSystem-FrontendWeb/archive/refs/heads/main.zip

# 解压（使用 PowerShell）
powershell -Command "Expand-Archive -Path frontend.zip -DestinationPath . -Force"

# 进入目录
cd ClubInterviewSystem-FrontendWeb-main

# 构建并启动
docker-compose up -d
```

### 访问应用

```
http://localhost:3000
```

---

## 本地已有源码

### 前置条件

- 已安装 Docker
- 已安装 Docker Compose

### 一键部署

```bash
# 停止
docker-compose down

# 重启
docker-compose restart

# 查看日志
docker-compose logs -f frontend

# 重新构建
docker-compose build --no-cache
docker-compose up -d
```

## 修改端口

编辑 `docker-compose.yml`：

```yaml
ports:
  - "8080:3000"  # 将外部端口改为 8080
```

## 配置后端 API

编辑 `src/api/request.ts`：

```typescript
baseURL: 'http://your-backend-ip:8000'
```

重新构建：

```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## 问题排查

```bash
# 查看容器日志
docker logs club-interview-frontend

# 进入容器
docker exec -it club-interview-frontend sh

# 检查构建产物
docker exec club-interview-frontend ls -la /app/dist
```

## 生产环境

修改端口为 80：

```yaml
ports:
  - "80:3000"
```

配置域名和反向代理，详见 [完整部署教程](./Docker部署教程.md)。

---

**快速部署，遇到问题查看详细教程** 📚
