# Club Interview System

## 📋 项目简介

校园社团招新与面试管理系统，包含前端和后端两部分。

- **前端**: Next.js 14 + TypeScript + Tailwind CSS + Shadcn/ui
- **后端**: FastAPI + SQLModel + SQLite

### 核心功能

- ✅ 用户认证（注册、登录、账号初始化、密码修改）
- ✅ 社团管理（创建、查询、成员管理）
- ✅ 招新流程（招新活动、报名申请、审核）
- ✅ 面试管理（面试安排、结果录入）
- ✅ 权限控制（RBAC 角色权限管理）
- ✅ 字典数据（学校、专业查询）

## 🚀 快速开始

### 方式一：使用启动脚本（推荐）

项目提供了便捷的启动脚本，可以一键启动前后端服务：

```bash
# 启动后端
python start.py backend

# 启动前端
python start.py frontend

# 同时启动前后端
python start.py both
```

**启动脚本会自动：**
- 检查依赖是否安装
- 创建预制账号（启动后端时）
- 启动对应服务

### 方式二：手动启动

#### 后端启动

1. **安装依赖**
```bash
cd backend
pip install -r requirements.txt
```

2. **配置环境变量**

创建 `backend/.env` 文件：
```env
APP_NAME=Club Interview System Backend
APP_ENV=dev
DEBUG=true
DB_NAME=club_interview.db
JWT_SECRET_KEY=your-secret-key-change-this
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

3. **数据库迁移**
```bash
cd backend
alembic upgrade head
```

4. **创建预制账号（可选）**
```bash
cd backend
python scripts/create_default_users.py
```

5. **启动后端服务**
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 前端启动

1. **安装依赖**
```bash
cd frontend
npm install
```

2. **配置环境变量**

创建 `frontend/.env.local` 文件：
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. **启动开发服务器**
```bash
cd frontend
npm run dev
```

访问 http://localhost:3000

### 预制账号

系统提供了预制账号，方便快速测试：

| 账号类型 | 手机号 | 密码 | 姓名 | 角色 |
|---------|--------|------|------|------|
| 普通学生 | 13800000001 | student123 | 张三 | 普通学生 |
| 系统管理员 | 13800000000 | admin123 | 系统管理员 | 系统管理员 |

**注意：**
- 使用 `start.py` 启动后端时会自动创建这些账号
- 这些账号仅用于开发和测试环境
- 生产环境请及时修改密码或删除这些账号

### API 文档

后端启动后，可访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📁 项目结构

```
ClubInterviewSystem-Backend/
├── backend/                    # 后端项目
│   ├── app/                    # 应用代码
│   │   ├── api/                # API 路由层
│   │   ├── core/               # 核心配置
│   │   ├── db/                 # 数据库
│   │   ├── models/             # 数据模型层
│   │   ├── repositories/       # 数据访问层
│   │   ├── services/           # 业务逻辑层
│   │   ├── schemas/            # Pydantic Schema
│   │   └── main.py             # FastAPI 应用入口
│   ├── alembic/                # 数据库迁移
│   ├── tests/                  # 测试
│   ├── requirements.txt        # Python 依赖
│   └── README.md               # 后端文档
│
├── frontend/                   # 前端项目
│   ├── app/                    # Next.js App Router
│   │   ├── layout.tsx          # 根布局
│   │   ├── page.tsx            # 首页
│   │   ├── login/              # 登录页
│   │   ├── register/           # 注册页
│   │   ├── dashboard/          # 仪表盘
│   │   ├── clubs/              # 社团管理
│   │   └── recruitments/       # 招新管理
│   ├── components/             # React 组件
│   │   ├── ui/                 # UI 组件库 (Shadcn/ui)
│   │   └── providers.tsx       # 全局 Provider
│   ├── lib/                    # 工具函数
│   │   ├── api.ts              # API 客户端
│   │   ├── auth.ts             # 认证相关
│   │   └── utils.ts            # 工具函数
│   ├── package.json            # Node.js 依赖
│   └── README.md               # 前端文档
│
└── docs/                       # 项目文档
    ├── README.md               # 项目总 README（本文件）
    ├── 设计文档.md             # 系统架构、数据库设计、API 设计
    └── 使用手册.md             # API 使用说明、开发指南
```

## 📚 文档

- [设计文档](./设计文档.md) - 系统架构、数据库设计、API 设计
- [使用手册](./使用手册.md) - API 使用说明、开发指南
- [后端文档](../backend/README.md) - 后端开发指南
- [前端文档](../frontend/README.md) - 前端开发指南

## 🛠️ 技术栈

### 前端技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| **Next.js** | 14.2+ | React 框架，App Router，服务端渲染 |
| **TypeScript** | 5.5+ | 静态类型检查，保障代码健壮性 |
| **Tailwind CSS** | 3.4+ | 原子化 CSS，构建现代 UI |
| **Shadcn/ui** | - | 基于 Radix UI 的高质量组件库 |
| **Axios** | 1.7+ | HTTP 客户端，API 请求 |
| **React Hook Form** | 7.5+ | 表单管理和验证 |
| **Zod** | 3.23+ | 类型安全的 Schema 验证 |

### 后端技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| **FastAPI** | - | 异步 Web 框架 |
| **SQLModel** | - | ORM + Pydantic 模型 |
| **SQLite** | - | 轻量级关系型数据库（Python内置） |
| **Alembic** | - | 数据库迁移工具 |
| **Passlib** | - | 密码哈希 (bcrypt) |
| **python-jose** | - | JWT 令牌处理 |
| **Pydantic Settings** | - | 环境变量配置管理 |
| **uvicorn** | - | ASGI 服务器 |

## 🎯 下一步开发

### 前端待开发

- [ ] 完善所有页面（社团详情、招新详情、申请详情等）
- [ ] 账号初始化页面
- [ ] 密码修改页面
- [ ] 文件上传组件
- [ ] 数据统计图表
- [ ] 实时通知（WebSocket）
- [ ] 响应式优化

### 后端待开发

- [ ] 权限管理 API - 角色分配、权限管理的完整 API 接口
- [ ] 文件上传 - 头像、身份证、学生证上传
- [ ] 短信验证码 - 手机号验证、登录/注册验证码
- [ ] API 限流 - 防止刷接口、DDoS 防护
- [ ] 日志系统 - 操作日志、审计日志
- [ ] 单元测试 - 覆盖率提升到 80%+
- [ ] 缓存优化 - Redis 缓存热点数据
- [ ] WebSocket - 实时通知、面试状态推送
- [ ] 消息通知 - 申请审核通知、面试安排通知
- [ ] 数据统计 - 招新数据统计、成员统计

## 📄 许可证

本项目仅供学习和内部使用。

---

**开发状态**: ✅ 核心业务模块已完成，系统功能完整可用

