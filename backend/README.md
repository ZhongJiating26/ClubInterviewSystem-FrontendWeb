# Club Interview System Backend

## 📋 项目简介

校园社团招新与面试管理系统后端，基于 FastAPI + SQLModel + SQLite 开发。

### 核心功能

- ✅ 用户认证（注册、登录、账号初始化、密码修改）
- ✅ 社团管理（创建、查询、成员管理）
- ✅ 招新流程（招新活动、报名申请、审核）
- ✅ 面试管理（面试安排、结果录入）
- ✅ 权限控制（RBAC 角色权限管理）
- ✅ 字典数据（学校、专业查询）

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

创建 `.env` 文件：
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

### 3. 数据库迁移

```bash
alembic upgrade head
```

### 4. 创建预制账号（可选）

系统提供了预制账号创建脚本，用于快速创建测试账号：

```bash
python scripts/create_default_users.py
```

**预制账号信息：**

| 账号类型 | 手机号 | 密码 | 姓名 | 角色 |
|---------|--------|------|------|------|
| 普通学生 | 13800000001 | student123 | 张三 | 普通学生 |
| 系统管理员 | 13800000000 | admin123 | 系统管理员 | 系统管理员 |

**注意：**
- 这些账号仅用于开发和测试环境
- 生产环境请及时修改密码或删除这些账号
- 如果账号已存在，脚本会跳过创建，不会报错
- 使用项目根目录的 `start.py` 启动后端时会自动创建这些账号

### 5. 启动后端服务

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

或者使用项目根目录的启动脚本：

```bash
# 在项目根目录执行
python start.py backend
```

### API 文档

后端启动后，可访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📁 项目结构

```
backend/
├── app/                        # 应用代码
│   ├── api/                    # API路由层
│   │   ├── deps.py             # FastAPI 依赖注入 (JWT 认证)
│   │   ├── deps_permission.py  # 权限检查依赖
│   │   └── v1/
│   │       ├── auth.py         # 认证 API
│   │       ├── club.py          # 社团管理 API
│   │       ├── recruitment.py  # 招新管理 API
│   │       └── dict.py          # 字典数据 API
│   ├── core/                   # 核心配置
│   │   ├── config.py           # 配置管理
│   │   └── security.py          # 安全相关（JWT、密码）
│   ├── db/                     # 数据库
│   │   └── session.py           # 数据库会话管理
│   ├── models/                 # 数据模型层
│   │   ├── base.py             # 基础模型（软删除）
│   │   ├── user_account.py     # 用户账号模型
│   │   ├── club.py             # 社团模型
│   │   ├── recruitment.py      # 招新模型
│   │   └── ...
│   ├── repositories/           # 数据访问层
│   │   ├── base.py             # 基础仓储
│   │   ├── user_account.py     # 用户仓储
│   │   └── ...
│   ├── services/               # 业务逻辑层
│   │   ├── auth_service.py     # 认证服务
│   │   ├── club_service.py     # 社团服务
│   │   └── ...
│   ├── schemas/                # Pydantic Schema
│   │   ├── auth.py             # 认证 Schema
│   │   ├── club.py             # 社团 Schema
│   │   └── ...
│   └── main.py                 # FastAPI 应用入口
├── alembic/                    # 数据库迁移
│   ├── versions/               # 迁移版本文件
│   └── env.py                  # Alembic 环境配置
├── tests/                      # 测试
│   └── test_auth_init.py       # 认证初始化测试
├── requirements.txt            # Python 依赖
└── README.md                   # 后端文档（本文件）
```

## 🛠️ 技术栈

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

## 🏗️ 架构设计

项目采用**分层架构**：

1. **Router层** (`app/api/`) - 处理HTTP请求，参数验证
2. **Service层** (`app/services/`) - 封装业务逻辑
3. **Repository层** (`app/repositories/`) - 数据访问，CRUD操作
4. **Model层** (`app/models/`) - 数据模型定义

### 核心特性

- **软删除**: 所有业务表继承 `BaseModel`，支持软删除
- **JWT认证**: 基于 JWT 的 Token 认证机制
- **权限控制**: RBAC 角色权限管理系统
- **数据验证**: 使用 Pydantic 进行严格的输入/输出验证

## 📚 文档

- [项目总文档](../docs/README.md) - 项目总览
- [设计文档](../docs/设计文档.md) - 系统架构、数据库设计、API 设计
- [使用手册](../docs/使用手册.md) - API 使用说明、开发指南

## 🔧 开发指南

### 添加新模型

1. 在 `app/models/` 创建模型文件
2. 继承 `BaseModel` 获取软删除能力
3. 在 `app/models/__init__.py` 导入模型
4. 生成并执行迁移：
   ```bash
   alembic revision --autogenerate -m "add new table"
   alembic upgrade head
   ```

### 添加新 API

1. 在 `app/api/v1/` 创建路由文件
2. 使用 `APIRouter` 定义路由
3. 在 `app/main.py` 注册路由：
   ```python
   from app.api.v1.new_module import router as new_router
   app.include_router(new_router)
   ```

### 服务层使用

```python
from app.services.auth_service import AuthService
from app.db.session import get_session

auth_service = AuthService()
user = auth_service.register(session, phone="13800000001", password="123456")
```

### 仓储模式使用

```python
from app.repositories.user_account import UserAccountRepository
from app.db.session import get_session

repo = UserAccountRepository()
user = repo.get_by_phone(session, phone)
```

## 🧪 测试

### 运行测试

```bash
pytest tests/test_auth_init.py -v
```

### API 测试

使用 Swagger UI 直接测试：
1. 访问 `http://localhost:8000/docs`
2. 点击 "Authorize" 输入 Token
3. 直接在页面上测试 API

## 🎯 下一步开发

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
