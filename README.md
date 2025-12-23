# Club Interview System Backend

## 📋 项目简介

这是一个基于 FastAPI + SQLModel + MySQL 的校园社团招新与面试管理系统后端。项目采用现代化的 Python Web 开发架构，提供用户注册、登录认证、社团管理等核心功能。

### 🎯 核心功能
- ✅ **用户注册与登录** - 支持手机号注册、密码登录，返回 JWT Token
- ✅ **安全认证** - 使用 bcrypt 密码哈希 + JWT 令牌认证
- ✅ **软删除机制** - 所有数据表支持软删除，数据可恢复
- ✅ **数据库迁移** - 使用 Alembic 进行版本化数据库管理
- ✅ **API 文档** - 内置 Swagger UI，可直接用于前端联调

## 🏗️ 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| **FastAPI** | - | 异步 Web 框架 |
| **SQLModel** | - | ORM + Pydantic 模型 |
| **MySQL** | 8.0+ | 关系型数据库 |
| **Alembic** | - | 数据库迁移工具 |
| **Passlib** | - | 密码哈希 (bcrypt) |
| **python-jose** | - | JWT 令牌处理 |
| **Pydantic Settings** | - | 配置管理 |

## 📁 项目结构

```
ClubInterviewSystem-Backend/
├── app/
│   ├── api/v1/
│   │   └── auth.py              # 认证相关 API (注册/登录)
│   ├── core/
│   │   ├── config.py            # 配置管理 (环境变量)
│   │   └── security.py          # 安全工具 (JWT)
│   ├── db/
│   │   └── session.py           # 数据库连接与 Session 管理
│   ├── models/
│   │   ├── base.py              # 基础模型 (软删除/时间戳)
│   │   ├── school.py            # 学校表模型
│   │   └── user_account.py      # 用户账号表模型
│   ├── repositories/
│   │   ├── base.py              # 通用仓储基类
│   │   └── user_account.py      # 用户账号仓储
│   └── main.py                  # FastAPI 应用入口
├── alembic/
│   ├── versions/                # 数据库迁移历史
│   │   ├── c0d912eb30e0_init.py
│   │   ├── 7906d6cae979_create_school_table.py
│   │   └── 9e13212a1495_create_user_account_table.py
│   └── env.py                   # Alembic 配置
├── .env                         # 环境变量配置
└── tmp_test_user_repo.py        # 用户仓储测试脚本
```

## 🗄️ 数据库设计

### 表结构

#### 1. `user_account` 用户账号表
```sql
-- 核心字段
id, phone, password_hash, token_version, status
-- 个人信息
name, id_card_no, school_id, major, student_no, avatar_url, email
-- 软删除 & 时间戳
is_deleted, deleted_at, created_at, updated_at
-- 认证相关
is_verified_campus, last_login_at
```

**特点：**
- ✅ 手机号唯一约束 (排除软删除数据)
- ✅ 密码使用 bcrypt 哈希存储
- ✅ token_version 用于强制登出/令牌吊销

#### 2. `school` 学校表
```sql
id, name, code, province, city, status
-- 软删除 & 时间戳
is_deleted, deleted_at, created_at, updated_at
```

### 软删除规范
所有业务表继承 `BaseModel`，包含：
- `is_deleted`: 0=正常, 1=已删除
- `deleted_at`: 删除时间
- `created_at`: 创建时间
- `updated_at`: 更新时间
- `touch()`: 更新时间戳方法
- `soft_delete()`: 软删除方法
- `restore()`: 恢复方法

## 🚀 快速开始

### 1. 环境准备

```bash
# 安装依赖
pip install -r requirements.txt

# 或者使用 pip
pip install fastapi sqlmodel pymysql alembic passlib python-jose pydantic-settings uvicorn
```

### 2. 配置环境变量

创建 `.env` 文件（已存在，可直接修改）：

```env
# ========== 基础 ==========
APP_NAME=Club Interview System Backend
APP_ENV=dev
DEBUG=true

# ========== 数据库 ==========
DB_HOST=10.62.1.230
DB_PORT=3306
DB_USER=root
DB_PASSWORD=123456
DB_NAME=campus_club_interview

# ========== JWT ==========
JWT_SECRET_KEY=dev_secret_change_me
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 3. 数据库迁移

```bash
# 生成迁移文件 (自动检测模型变更)
alembic revision --autogenerate -m "描述信息"

# 执行迁移
alembic upgrade head

# 回滚迁移
alembic downgrade -1

# 查看当前版本
alembic current

# 查看迁移历史
alembic history
```

### 4. 运行服务

```bash
# 开发模式运行
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 或使用 python
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. 测试 API

访问 Swagger UI:
```
http://localhost:8000/docs
```

## 📡 API 接口

### 认证模块 (`/auth`)

#### 1. 用户注册
```http
POST /auth/register
Content-Type: application/json

{
  "phone": "13800000001",
  "password": "123456",
  "name": "张三",
  "school_id": 1
}

# 响应
{
  "id": 1,
  "phone": "13800000001",
  "name": "张三"
}
```

#### 2. 用户登录
```http
POST /auth/login
Content-Type: application/json

{
  "phone": "13800000001",
  "password": "123456"
}

# 响应
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR...",
  "token_type": "bearer"
}
```

### 健康检查

```http
GET /health

# 响应
{
  "status": "ok",
  "env": "dev"
}
```

## 🔐 安全特性

### 1. 密码安全
- 使用 **bcrypt** 算法进行密码哈希
- 自动加盐，防止彩虹表攻击
- 密码验证使用 `passlib` 库

### 2. JWT 认证
- 算法：HS256
- Payload 包含：`user_id`, `token_version`
- 支持令牌过期时间配置
- 通过 `token_version` 实现强制登出

### 3. 数据安全
- 所有 API 参数使用 Pydantic 验证
- 数据库唯一约束防止重复数据
- 软删除防止数据丢失

## 🛠️ 开发指南

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

### 仓储模式

所有数据库操作通过 Repository 类：

```python
from app.repositories.user_account import UserAccountRepository
from app.db.session import get_session

repo = UserAccountRepository()
user = repo.get_by_phone(session, phone)
```

## 🧪 测试

### 手动测试脚本

使用 `tmp_test_user_repo.py` 测试用户仓储：

```bash
python tmp_test_user_repo.py
```

### API 测试

使用 Swagger UI 直接测试：
1. 访问 `http://localhost:8000/docs`
2. 点击 "Authorize" 输入 Token
3. 直接在页面上测试 API

## 📝 开发规范

### 代码风格
- 使用类型注解
- 遵循 PEP 8
- 函数和类要有文档字符串
- 中文注释说明业务逻辑

### Git 提交规范
```
feat: 新功能
fix: 修复 bug
docs: 文档更新
refactor: 代码重构
test: 测试相关
chore: 构建/工具变动
```

### 分支管理
- `main`: 主分支，稳定版本
- `develop`: 开发分支
- `feature/xxx`: 功能分支

## 🔧 常见问题

### Q: 如何重置数据库？
```bash
# 回滚所有迁移
alembic downgrade base

# 重新执行所有迁移
alembic upgrade head
```

### Q: 如何查看 SQL 语句？
在 `.env` 中设置：
```env
DEBUG=true
```
SQL 语句将在控制台输出。

### Q: 如何修改 JWT 过期时间？
修改 `app/core/config.py`：
```python
jwt_expire_minutes: int = Field(60 * 24)  # 1天
access_token_expire_minutes: int = 30
```

## 📚 依赖说明

### 核心依赖
- **fastapi**: 异步 Web 框架，自动生成 API 文档
- **sqlmodel**: SQLModel = SQLAlchemy + Pydantic，简化 ORM
- **pymysql**: MySQL 数据库驱动
- **alembic**: 数据库迁移工具
- **passlib**: 密码哈希库 (bcrypt)
- **python-jose**: JWT 令牌处理
- **pydantic-settings**: 环境变量配置管理
- **uvicorn**: ASGI 服务器

## 🎯 下一步开发计划

- [ ] 添加社团管理模块
- [ ] 添加招新流程管理
- [ ] 添加面试安排功能
- [ ] 添加权限控制 (RBAC)
- [ ] 添加文件上传 (头像/资料)
- [ ] 添加短信验证码注册
- [ ] 添加 Redis 缓存
- [ ] 添加单元测试
- [ ] 添加 API 限流
- [ ] 添加日志系统

## 📄 许可证

本项目仅供学习和内部使用。

## 📞 联系方式

如有问题，请通过以下方式联系：
- 提交 Issue
- 发送邮件
- 创建 Pull Request

---

**开发状态**: ✅ 基础架构完成，核心功能可用