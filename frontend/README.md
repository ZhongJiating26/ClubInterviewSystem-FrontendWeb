# Club Interview System Frontend

校园社团招新与面试管理系统前端，基于 Next.js 14 + TypeScript + Tailwind CSS 开发。

## 🚀 快速开始

### 方式一：使用启动脚本（推荐）

在项目根目录执行：

```bash
python start.py frontend
```

### 方式二：手动启动

### 1. 安装依赖

```bash
npm install
# 或
yarn install
# 或
pnpm install
```

### 2. 配置环境变量

复制 `.env.local.example` 为 `.env.local`：

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. 启动开发服务器

```bash
npm run dev
# 或
yarn dev
# 或
pnpm dev
```

访问 http://localhost:3000

### 4. 构建生产版本

```bash
npm run build
npm start
```

## 📁 项目结构

```
frontend/
├── app/                    # Next.js App Router
│   ├── layout.tsx         # 根布局
│   ├── page.tsx           # 首页
│   ├── login/             # 登录页
│   ├── register/          # 注册页
│   └── dashboard/         # 仪表盘
├── components/            # React 组件
│   ├── ui/               # UI 组件库 (Shadcn/ui)
│   └── providers.tsx     # 全局 Provider
├── lib/                  # 工具函数
│   ├── api.ts            # API 客户端
│   ├── auth.ts           # 认证相关
│   └── utils.ts          # 工具函数
└── public/               # 静态资源
```

## 🛠️ 技术栈

- **Next.js 14** - React 框架，App Router
- **TypeScript** - 类型安全
- **Tailwind CSS** - 原子化 CSS
- **Shadcn/ui** - 高质量组件库
- **Axios** - HTTP 客户端

## 🔑 测试账号

系统提供了预制测试账号，可以使用以下账号登录测试：

| 账号类型 | 手机号 | 密码 |
|---------|--------|------|
| 普通学生 | 13800000001 | student123 |
| 系统管理员 | 13800000000 | admin123 |

**注意：** 这些账号仅用于开发和测试环境。

