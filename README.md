# 社团面试系统前端

基于 Vue 3 + TypeScript + Vite + shadcn-vue 构建的社团面试管理系统前端项目。

## 文档导航

- [待办列表 (TODO)](./TODO.md) - 当前开发任务和计划
- [更新日志 (CHANGELOG)](./CHANGELOG.md) - 已完成功能和更新记录
- [完整API接口文档](./文档/完整API接口文档.md) - 后端 API 接口文档
- [系统详细设计文档](./文档/系统详细设计文档v2.7.md) - 系统设计文档

## 技术栈

- **框架**: Vue 3 (Script Setup)
- **构建工具**: Vite
- **语言**: TypeScript
- **UI 组件库**: shadcn-vue (基于 reka-ui)
- **样式**: Tailwind CSS v4
- **状态管理**: Pinia
- **路由**: Vue Router
- **HTTP 客户端**: Axios
- **图标**: Lucide Vue Next

## 项目结构

```
src/
├── api/                 # API 接口封装
│   └── modules/         # 按模块组织的 API
│       ├── auth.ts      # 认证相关
│       ├── applications.ts
│       ├── clubs.ts
│       ├── interviews.ts
│       ├── notifications.ts
│       ├── schools.ts
│       ├── score.ts
│       ├── statistics.ts
│       └── tickets.ts
├── assets/              # 静态资源
├── components/          # 公共组件
│   ├── ui/              # shadcn-vue 组件
│   └── SchoolSelect.vue # 学校选择组件
├── layouts/             # 布局组件
│   ├── AdminLayout.vue      # 管理员端布局（桌面端）
│   ├── InterviewerLayout.vue # 面试官端布局（桌面端）
│   └── StudentLayout.vue     # 学生端布局（移动端 H5）
├── lib/                 # 工具函数
│   └── utils.ts         # 公共工具
├── router/              # 路由配置
│   └── index.ts
├── stores/              # Pinia 状态管理
│   └── user.ts
├── views/               # 页面组件
│   ├── Login.vue
│   ├── Register.vue
│   ├── ForgetPassword.vue
│   ├── RoleSelect.vue
│   ├── Init.vue
│   ├── NotFound.vue
│   ├── admin/           # 管理员端页面
│   │   ├── Dashboard.vue
│   │   ├── Applications.vue
│   │   ├── Interviews.vue
│   │   ├── Statistics.vue
│   │   ├── Tickets.vue
│   │   └── clubs/
│   │       └── Profile.vue     # 社团资料页面
│   ├── interviewer/     # 面试官端页面
│   └── student/         # 学生端页面
├── App.vue
├── main.ts
└── style.css
```

## 用户角色

1. **社团管理员 (admin)**: 管理社团招新、面试安排等（桌面端）
2. **面试官 (interviewer)**: 参与面试评分、评审工作（桌面端）
3. **普通学生 (student)**: 申请加入社团、参加面试（移动端 H5）

## 功能特性

### 认证流程
```
登录 → 注册 → 选择角色 → 初始化信息
```
- 未初始化用户登录后自动跳转到角色选择页
- 根据角色初始化不同的信息（社团管理员需填写社团名称）
- 初始化完成后根据角色跳转到对应首页

### 管理后台（社团管理员）
- **仪表盘**: 展示数据看板，社团资料不完整时提示完善
- **报名管理**: 发布报名、历史记录、报名审核
- **面试管理**: 发布面试、面试记录、面试筛选
- **社团管理**: 社团资料查看与编辑
- **系统设置**: 系统配置

### 社团资料页面
- **查看模式**: 展示社团 Logo、名称、分类、学校、简介、状态
- **编辑模式**: 支持修改名称、分类、简介、Logo
- **Logo 处理**: 选择图片后本地预览，确认后上传后端

### 学生端页面优化（最新）
- **个人资料页**: 完整信息展示（姓名、学号、手机号、邮箱、专业、学校）
- **面试记录页**: 标签固定顶部，不随内容滚动
- **样式优化**: 统一淡灰色边框，移除阴影效果
- **响应式布局**: 移动端 H5 适配

## 最近更新

### 2026-01-05
- ✅ 学生个人资料页面 API 集成，支持显示完整信息
- ✅ 面试记录页面 TabsList 固定顶部
- ✅ 所有页面 header 和底部按钮区域样式优化（淡灰色边框）
- ✅ HTML 语言设置为中文 (`lang="zh-CN"`)
- ✅ 首页卡片阴影移除

详细更新记录请查看 [CHANGELOG.md](./CHANGELOG.md)

## 后端接口需求

### 待实现的接口
- **GET `/api/student/profile`** - 获取学生详细信息
  - 响应格式：
    ```json
    {
      "code": 200,
      "data": {
        "id": 27,
        "phone": "18267692330",
        "name": "钟佳挺",
        "email": "example@email.com",
        "student_no": "202301001",
        "major": "计算机科学与技术",
        "school_code": "4133013021",
        "school_name": "浙大城市学院",
        "status": 1,
        "is_initialized": true,
        "avatar_url": null
      },
      "message": ""
    }
    ```

更多待开发任务请查看 [TODO.md](./TODO.md)

## 开发

### 安装依赖

```bash
npm install
```

### 启动开发服务器

```bash
npm run dev
```

默认访问地址: http://localhost:5173

### 网络访问

配置了 `host: '0.0.0.0'`，允许其他设备通过局域网 IP 访问。

### 构建生产版本

```bash
npm run build
```

## API 代理

开发环境下通过 Vite 代理访问后端 API:

- `/auth` - 认证接口
- `/applications` - 报名管理
- `/interviews` - 面试管理
- `/notifications` - 通知中心
- `/tickets` - 工单管理
- `/statistics` - 数据统计
- `/score` - 评分接口
- `/student` - 学生相关（含 `/api/student/profile` 获取详细信息）
- `/schools` - 学校信息
- `/clubs` - 社团管理
- `/invitations` - 邀请管理

代理目标: `http://localhost:8000`
