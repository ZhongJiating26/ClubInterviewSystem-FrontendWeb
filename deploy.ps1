# ============================================
# 社团面试系统前端 - Windows Docker 部署脚本
# ============================================

# =================== 配置区域 ===================
# 修改为你的 GitHub 仓库地址
$GITHUB_REPO = "https://github.com/你的用户名/ClubInterviewSystem-FrontendWeb"

# 项目部署目录
$PROJECT_DIR = "C:\projects\ClubInterviewSystem-FrontendWeb"

# 容器名称
$CONTAINER_NAME = "club-interview-frontend"

# 端口配置
$HOST_PORT = "3000"
# ==================================================

Write-Host ""
Write-Host "============================================"  -ForegroundColor Green
Write-Host "   社团面试系统前端 - Docker 部署脚本"      -ForegroundColor Green
Write-Host "============================================"  -ForegroundColor Green
Write-Host ""

# 检查 Docker 是否安装
Write-Host "[1/8] 检查 Docker 环境..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "      ✓ $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "      ✗ Docker 未安装，请先安装 Docker Desktop" -ForegroundColor Red
    Write-Host "      下载地址: https://www.docker.com/products/docker-desktop" -ForegroundColor Cyan
    exit 1
}

# 检查 Docker Compose
try {
    $composeVersion = docker-compose --version
    Write-Host "      ✓ $composeVersion" -ForegroundColor Green
} catch {
    Write-Host "      ✗ Docker Compose 不可用" -ForegroundColor Red
    exit 1
}

# 检查 Docker 是否运行
Write-Host "[2/8] 检查 Docker 服务状态..." -ForegroundColor Yellow
try {
    docker ps | Out-Null
    Write-Host "      ✓ Docker 服务正在运行" -ForegroundColor Green
} catch {
    Write-Host "      ✗ Docker 服务未运行，请启动 Docker Desktop" -ForegroundColor Red
    exit 1
}

# 创建项目目录
Write-Host "[3/8] 创建项目目录..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "C:\projects" | Out-Null
Set-Location "C:\projects"
Write-Host "      ✓ 项目目录: C:\projects" -ForegroundColor Green

# 下载或更新源码
Write-Host "[4/8] 从 GitHub 获取源码..." -ForegroundColor Yellow

if (Test-Path "ClubInterviewSystem-FrontendWeb") {
    Write-Host "      检测到已存在的项目目录" -ForegroundColor Cyan
    $choice = Read-Host "      是否删除并重新下载？(y/N)"
    if ($choice -eq 'y' -or $choice -eq 'Y') {
        Write-Host "      删除旧版本..." -ForegroundColor Cyan
        Remove-Item -Recurse -Force "ClubInterviewSystem-FrontendWeb"
    } else {
        Write-Host "      使用现有版本" -ForegroundColor Green
        Set-Location "ClubInterviewSystem-FrontendWeb"
    }
}

if (!(Test-Path "ClubInterviewSystem-FrontendWeb")) {
    Write-Host "      正在从 GitHub 克隆..." -ForegroundColor Cyan

    # 尝试使用 Git 克隆
    $gitInstalled = $false
    try {
        git --version | Out-Null
        $gitInstalled = $true
    } catch {
        # Git 未安装
    }

    if ($gitInstalled) {
        git clone $GITHUB_REPO
        if ($LASTEXITCODE -eq 0) {
            Write-Host "      ✓ Git 克隆成功" -ForegroundColor Green
            Set-Location "ClubInterviewSystem-FrontendWeb"
        } else {
            throw "Git 克隆失败"
        }
    } else {
        Write-Host "      Git 未安装，尝试下载 ZIP..." -ForegroundColor Cyan
        throw "使用 ZIP 下载"
    }
}

Set-Location "ClubInterviewSystem-FrontendWeb"

# 验证项目文件
Write-Host "[5/8] 验证项目文件..." -ForegroundColor Yellow
$missingFiles = @()

if (!(Test-Path "Dockerfile")) {
    $missingFiles += "Dockerfile"
}
if (!(Test-Path "docker-compose.yml")) {
    $missingFiles += "docker-compose.yml"
}
if (!(Test-Path "package.json")) {
    $missingFiles += "package.json"
}

if ($missingFiles.Count -gt 0) {
    Write-Host "      ✗ 缺少必要文件: $($missingFiles -join ', ')" -ForegroundColor Red
    exit 1
}
Write-Host "      ✓ 项目文件完整" -ForegroundColor Green

# 停止旧容器（如果存在）
Write-Host "[6/8] 停止旧容器..." -ForegroundColor Yellow
$oldContainer = docker ps -a --filter "name=$CONTAINER_NAME" --format "{{.Names}}"
if ($oldContainer) {
    Write-Host "      发现旧容器，正在停止..." -ForegroundColor Cyan
    docker-compose down
    Write-Host "      ✓ 旧容器已停止" -ForegroundColor Green
} else {
    Write-Host "      ✓ 没有旧容器" -ForegroundColor Green
}

# 构建镜像
Write-Host "[7/8] 构建 Docker 镜像..." -ForegroundColor Yellow
Write-Host "      这可能需要几分钟，请耐心等待..." -ForegroundColor Cyan
docker-compose build
if ($LASTEXITCODE -eq 0) {
    Write-Host "      ✓ 镜像构建成功" -ForegroundColor Green
} else {
    Write-Host "      ✗ 镜像构建失败" -ForegroundColor Red
    exit 1
}

# 启动容器
Write-Host "[8/8] 启动容器..." -ForegroundColor Yellow
docker-compose up -d
if ($LASTEXITCODE -eq 0) {
    Write-Host "      ✓ 容器启动成功" -ForegroundColor Green
} else {
    Write-Host "      ✗ 容器启动失败" -ForegroundColor Red
    exit 1
}

# 等待服务启动
Write-Host ""
Write-Host "正在等待服务启动..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# 检查容器状态
Write-Host ""
Write-Host "============================================"  -ForegroundColor Green
Write-Host "   部署状态检查"                              -ForegroundColor Green
Write-Host "============================================"  -ForegroundColor Green
docker-compose ps

# 检查端口占用
Write-Host ""
Write-Host "端口检查:" -ForegroundColor Yellow
try {
    $portCheck = netstat -ano | findstr ":$HOST_PORT.*LISTENING"
    if ($portCheck) {
        Write-Host "✓ 端口 $HOST_PORT 正在监听" -ForegroundColor Green
    } else {
        Write-Host "⚠ 端口 $HOST_PORT 未监听，容器可能还在启动" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠ 无法检查端口状态" -ForegroundColor Yellow
}

# 显示访问信息
Write-Host ""
Write-Host "============================================"  -ForegroundColor Green
Write-Host "   部署完成！"                                 -ForegroundColor Green
Write-Host "============================================"  -ForegroundColor Green
Write-Host ""
Write-Host "访问地址: " -NoNewline
Write-Host "http://localhost:$HOST_PORT" -ForegroundColor Cyan
Write-Host ""
Write-Host "常用命令:" -ForegroundColor Yellow
Write-Host "  查看日志: docker-compose logs -f frontend" -ForegroundColor White
Write-Host "  停止服务: docker-compose down" -ForegroundColor White
Write-Host "  重启服务: docker-compose restart" -ForegroundColor White
Write-Host "  查看状态: docker-compose ps" -ForegroundColor White
Write-Host ""

# 询问是否查看日志
$choice = Read-Host "是否查看实时日志？(Y/n)"
if ($choice -ne 'n' -and $choice -ne 'N') {
    Write-Host ""
    Write-Host "查看日志中... (Ctrl+C 退出)" -ForegroundColor Yellow
    Write-Host ""
    docker-compose logs -f frontend
}

Write-Host ""
Write-Host "部署脚本执行完成！" -ForegroundColor Green
