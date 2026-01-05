# 校园社团招新与面试管理系统 - 完整 API 接口文档

## 文档信息

- **系统名称**：校园社团招新与面试管理系统
- **版本**：v1.0.0
- **更新日期**：2026-01-05
- **Base URL**：`http://192.168.1.100:8000/api`（局域网访问）

---

## 目录

- [通用说明](#通用说明)
- [1. 用户认证模块](#1-用户认证模块)
- [2. 学校管理模块](#2-学校管理模块)
- [3. 社团管理模块](#3-社团管理模块)
- [4. 部门管理模块](#4-部门管理模块)
- [5. 岗位管理模块](#5-岗位管理模块)
- [6. 招新场次管理模块](#6-招新场次管理模块)
- [7. 报名管理模块](#7-报名管理模块)
- [8. 面试管理模块](#8-面试管理模块)
- [9. 学生端模块](#9-学生端模块)
- [数据模型](#数据模型)
- [错误码说明](#错误码说明)

---

## 通用说明

### 认证方式

所有需要认证的接口都需要在请求头中携带 JWT Token：

```
Authorization: Bearer {token}
```

### 响应格式

成功响应：
```json
{
  "code": 200,
  "data": {},
  "message": "success"
}
```

错误响应：
```json
{
  "detail": "错误描述信息"
}
```

### 分页参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| page | int | 1 | 页码 |
| page_size | int | 20 | 每页数量 |

---

## 1. 用户认证模块

### 1.1 发送验证码

发送手机验证码（注册/登录场景）。

**接口地址：**
```
POST /api/auth/send-code
```

**请求体：**
```json
{
  "phone": "13800138000",
  "scene": "REGISTER"
}
```

**参数说明：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| phone | string | 是 | 手机号 |
| scene | string | 是 | 场景：REGISTER（注册）/LOGIN（登录） |

**响应：**
```json
{
  "detail": "验证码已发送"
}
```

---

### 1.2 用户注册

使用手机号+验证码注册账号。

**接口地址：**
```
POST /api/auth/register
```

**请求体：**
```json
{
  "phone": "13800138000",
  "code": "123456"
}
```

**响应：**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**业务规则：**
- 手机号未注册时创建新用户
- 手机号已注册但未初始化则返回现有 token
- 手机号已注册且已初始化则报错

---

### 1.3 用户登录

使用手机号+密码登录。

**接口地址：**
```
POST /api/auth/login
```

**请求体：**
```json
{
  "phone": "13800138000",
  "password": "password123"
}
```

**响应：**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**业务规则：**
- 账号未初始化则返回错误，提示先完善信息
- 密码错误则返回错误提示

---

### 1.4 获取当前用户信息

获取当前登录用户的详细信息。

**接口地址：**
```
GET /api/auth/me
Authorization: Bearer {token}
```

**响应：**
```json
{
  "id": 1,
  "phone": "13800138000",
  "name": "张三",
  "status": 1,
  "is_initialized": true,
  "school_code": "4133013021",
  "school_name": "浙大城市学院",
  "roles": [
    {
      "id": 1,
      "code": "STUDENT",
      "name": "学生",
      "club_id": null
    }
  ]
}
```

---

### 1.5 初始化账号

设置密码和个人信息（首次登录必填）。

**接口地址：**
```
POST /api/auth/init
Authorization: Bearer {token}
```

**请求体：**
```json
{
  "password": "password123",
  "name": "张三",
  "id_card_no": "330106200001011234",
  "school_code": "4133013021",
  "major": "计算机科学与技术",
  "student_no": "202001001",
  "email": "zhangsan@example.com",
  "avatar_url": "http://example.com/avatar.jpg"
}
```

**响应：**
```json
{}
```

**业务规则：**
- 只能初始化一次
- 已初始化的账号再次调用将返回 409 错误

---

### 1.6 分配角色

为用户分配角色（管理员功能）。

**接口地址：**
```
POST /api/auth/assign-role
Authorization: Bearer {token}
```

**请求体：**
```json
{
  "user_id": 10,
  "role_id": 2,
  "club_id": 1
}
```

**响应：**
```json
{
  "detail": "角色分配成功",
  "user_role": {
    "id": 5,
    "user_id": 10,
    "role_id": 2,
    "club_id": 1
  }
}
```

---

### 1.7 撤销角色

撤销用户的角色。

**接口地址：**
```
POST /api/auth/revoke-role
Authorization: Bearer {token}
```

**请求体：**
```json
{
  "user_id": 10,
  "role_id": 2,
  "club_id": 1
}
```

**响应：**
```json
{
  "detail": "角色撤销成功"
}
```

---

## 2. 学校管理模块

### 2.1 获取学校列表

获取所有学校列表。

**接口地址：**
```
GET /api/schools
```

**响应：**
```json
[
  {
    "id": 1,
    "name": "浙大城市学院",
    "code": "4133013021",
    "created_at": "2026-01-01T00:00:00"
  }
]
```

---

### 2.2 根据代码获取学校

根据学校代码查询学校信息。

**接口地址：**
```
GET /api/schools/by-code/{code}
```

**路径参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| code | string | 学校代码 |

**响应：**
```json
{
  "id": 1,
  "name": "浙大城市学院",
  "code": "4133013021"
}
```

---

## 3. 社团管理模块

### 3.1 创建社团

提交社团创建申请。

**接口地址：**
```
POST /api/clubs/init
Authorization: Bearer {token}
```

**请求体：**
```json
{
  "school_code": "4133013021",
  "name": "编程社",
  "category": "学术科技类",
  "description": "专注于编程技术交流的学生社团",
  "logo_url": "http://example.com/logo.png"
}
```

**响应：**
```json
{
  "club_id": 1
}
```

---

### 3.2 更新社团资料

更新社团基本信息。

**接口地址：**
```
PUT /api/clubs/{club_id}
Authorization: Bearer {token}
```

**路径参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| club_id | number | 社团ID |

**请求体：**
```json
{
  "name": "编程社",
  "category": "学术科技类",
  "description": "专注于编程技术交流",
  "logo_url": "http://example.com/logo.png"
}
```

**响应：**
```json
{
  "id": 1,
  "school_code": "4133013021",
  "name": "编程社",
  "logo_url": "http://192.168.1.100:9000/club-interview-system/dev/clubs/logos/logo.png",
  "category": "学术科技类",
  "description": "专注于编程技术交流",
  "status": "PENDING",
  "created_at": "2026-01-01T00:00:00"
}
```

---

### 3.3 上传社团认证证书

上传社团认证证书文件。

**接口地址：**
```
POST /api/clubs/{club_id}/cert
Authorization: Bearer {token}
Content-Type: multipart/form-data
```

**表单参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file | File | 是 | 证书文件（PDF/PNG/JPG） |

**响应：**
```json
{
  "cert_file_url": "http://192.168.1.100:9000/club-interview-system/dev/clubs/certs/cert.pdf"
}
```

---

### 3.4 检查社团名称是否可用

检查社团名称是否已被使用。

**接口地址：**
```
POST /api/clubs/check-name
Authorization: Bearer {token}
```

**请求体：**
```json
{
  "name": "编程社"
}
```

**响应：**
```json
{
  "available": true,
  "message": "名称可用"
}
```

---

### 3.5 绑定用户到社团

将用户添加到社团（管理员功能）。

**接口地址：**
```
POST /api/clubs/{club_id}/bind-user
Authorization: Bearer {token}
```

**请求体：**
```json
{
  "user_id": 10,
  "role_code": "CLUB_ADMIN"
}
```

**响应：**
```json
{
  "detail": "用户绑定成功"
}
```

---

### 3.6 获取首页社团列表

获取首页展示的社团卡片列表。

**接口地址：**
```
GET /api/clubs/home-list?school_code={code}&status={status}
```

**查询参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| school_code | string | 是 | 学校代码 |
| status | string | 否 | 状态筛选 |

**响应：**
```json
[
  {
    "id": 1,
    "name": "编程社",
    "logo_url": "http://192.168.1.100:9000/club-interview-system/dev/clubs/logos/logo.png",
    "category": "学术科技类",
    "description": "专注于编程技术交流",
    "recruiting": true
  }
]
```

---

### 3.7 获取社团详情

获取社团完整信息（包含部门、岗位、招新场次）。

**接口地址：**
```
GET /api/clubs/{id}/detail
```

**路径参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| id | number | 社团ID |

**响应：**
```json
{
  "id": 6,
  "school_name": "浙大城市学院",
  "name": "书法社",
  "logo_url": "http://192.168.1.100:9000/club-interview-system/dev/clubs/logos/logo.png",
  "category": "文化艺术类",
  "description": "这是测试",
  "cert_file_url": "http://192.168.1.100:9000/club-interview-system/dev/clubs/certs/cert.pdf",
  "status": "APPROVED",
  "created_at": "2026-01-01T00:00:00",
  "departments": [
    {
      "id": 4,
      "club_id": 6,
      "name": "部门1",
      "description": "测试部门",
      "created_at": "2026-01-01T00:00:00"
    }
  ],
  "positions": [
    {
      "id": 1,
      "club_id": 6,
      "department_id": 4,
      "name": "测试1",
      "description": "12",
      "requirement": "12",
      "created_at": "2026-01-01T00:00:00"
    }
  ],
  "recruitment_sessions": [
    {
      "id": 1,
      "name": "2026年春季招新",
      "start_time": "2026-01-04T11:30:00",
      "end_time": "2026-01-07T11:30:00",
      "status": "PUBLISHED",
      "positions": [
        {
          "id": 2,
          "session_id": 1,
          "position_id": 1,
          "department_id": 4,
          "department_name": "部门1",
          "position_name": "测试1",
          "position_description": "12",
          "position_requirement": "12",
          "recruit_quota": 1
        }
      ]
    }
  ]
}
```

---

## 4. 部门管理模块

### 4.1 创建部门

创建社团部门。

**接口地址：**
```
POST /api/departments
Authorization: Bearer {token}
```

**请求体：**
```json
{
  "club_id": 1,
  "name": "技术部",
  "description": "负责技术相关工作"
}
```

**响应：**
```json
{
  "id": 1,
  "club_id": 1,
  "name": "技术部",
  "description": "负责技术相关工作",
  "created_at": "2026-01-01T00:00:00"
}
```

---

### 4.2 获取社团部门列表

获取指定社团的所有部门。

**接口地址：**
```
GET /api/departments?club_id={club_id}
```

**查询参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| club_id | number | 是 | 社团ID |

**响应：**
```json
[
  {
    "id": 1,
    "club_id": 1,
    "name": "技术部",
    "description": "负责技术相关工作",
    "created_at": "2026-01-01T00:00:00"
  }
]
```

---

### 4.3 更新部门

更新部门信息。

**接口地址：**
```
PUT /api/departments/{id}
Authorization: Bearer {token}
```

**请求体：**
```json
{
  "name": "技术研发部",
  "description": "负责技术研发相关工作"
}
```

**响应：**
```json
{
  "id": 1,
  "name": "技术研发部",
  "description": "负责技术研发相关工作"
}
```

---

### 4.4 删除部门

删除指定部门。

**接口地址：**
```
DELETE /api/departments/{id}
Authorization: Bearer {token}
```

**响应：** 204 No Content

---

## 5. 岗位管理模块

### 5.1 创建岗位

创建社团岗位。

**接口地址：**
```
POST /api/positions
Authorization: Bearer {token}
```

**请求体：**
```json
{
  "club_id": 1,
  "department_id": 1,
  "name": "技术部干事",
  "description": "负责技术支持工作",
  "requirement": "热爱编程，有基础"
}
```

**响应：**
```json
{
  "id": 1,
  "club_id": 1,
  "department_id": 1,
  "name": "技术部干事",
  "description": "负责技术支持工作",
  "requirement": "热爱编程，有基础",
  "created_at": "2026-01-01T00:00:00"
}
```

---

### 5.2 获取社团岗位列表

获取指定社团的所有岗位。

**接口地址：**
```
GET /api/positions?club_id={club_id}
```

**响应：**
```json
[
  {
    "id": 1,
    "club_id": 1,
    "department_id": 1,
    "name": "技术部干事",
    "description": "负责技术支持工作",
    "requirement": "热爱编程，有基础"
  }
]
```

---

### 5.3 更新岗位

更新岗位信息。

**接口地址：**
```
PUT /api/positions/{id}
Authorization: Bearer {token}
```

**请求体：**
```json
{
  "name": "高级技术干事",
  "description": "负责高级技术支持",
  "requirement": "有项目经验"
}
```

---

### 5.4 删除岗位

删除指定岗位。

**接口地址：**
```
DELETE /api/positions/{id}
Authorization: Bearer {token}
```

---

## 6. 招新场次管理模块

### 6.1 获取招新场次列表

获取招新场次列表，支持筛选。

**接口地址：**
```
GET /api/recruitment/sessions?club_id={club_id}&status={status}
```

**查询参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| club_id | number | 否 | 筛选指定社团的场次 |
| status | string | 否 | 筛选指定状态 |

**响应：**
```json
[
  {
    "id": 1,
    "club_id": 1,
    "name": "2026年春季招新",
    "description": "春季招新活动",
    "start_time": "2026-01-01T00:00:00",
    "end_time": "2026-01-31T23:59:59",
    "max_candidates": 100,
    "status": "PUBLISHED",
    "created_by": 1,
    "created_at": "2026-01-01T00:00:00",
    "updated_at": "2026-01-01T00:00:00",
    "positions": [
      {
        "id": 1,
        "session_id": 1,
        "position_id": 1,
        "position_name": "技术部干事",
        "position_description": "负责技术支持",
        "position_requirement": "热爱编程",
        "recruit_quota": 10
      }
    ]
  }
]
```

---

### 6.2 创建招新场次

创建新的招新场次。

**接口地址：**
```
POST /api/recruitment/sessions?club_id={club_id}
Authorization: Bearer {token}
```

**请求体：**
```json
{
  "name": "2026年春季招新",
  "description": "春季招新活动",
  "start_time": "2026-01-01T00:00:00",
  "end_time": "2026-01-31T23:59:59",
  "max_candidates": 100
}
```

**响应：** 返回创建的场次对象

---

### 6.3 获取招新场次详情

获取指定招新场次的详细信息。

**接口地址：**
```
GET /api/recruitment/sessions/{session_id}
```

**响应：** 返回场次对象（包含关联的岗位列表）

---

### 6.4 更新招新场次

更新招新场次信息。

**接口地址：**
```
PUT /api/recruitment/sessions/{session_id}
Authorization: Bearer {token}
```

**请求体：** 所有字段可选
```json
{
  "name": "2026年春季招新（更新）",
  "status": "PUBLISHED"
}
```

---

### 6.5 删除招新场次

删除招新场次（软删除）。

**接口地址：**
```
DELETE /api/recruitment/sessions/{session_id}
Authorization: Bearer {token}
```

**响应：** 204 No Content

---

### 6.6 添加岗位到招新场次

将岗位关联到招新场次。

**接口地址：**
```
POST /api/recruitment/sessions/{session_id}/positions
Authorization: Bearer {token}
```

**请求体：**
```json
{
  "position_id": 1,
  "recruit_quota": 10
}
```

---

### 6.7 更新岗位招聘配额

更新招新场次中某岗位的招聘配额。

**接口地址：**
```
PUT /api/recruitment/sessions/{session_id}/positions/{pos_id}
Authorization: Bearer {token}
```

**请求体：**
```json
{
  "recruit_quota": 15
}
```

---

### 6.8 移除招新场次的岗位

取消岗位与招新场次的关联。

**接口地址：**
```
DELETE /api/recruitment/sessions/{session_id}/positions/{pos_id}
Authorization: Bearer {token}
```

---

### 6.9 获取场次岗位列表

获取招新场次关联的所有岗位。

**接口地址：**
```
GET /api/recruitment/sessions/{session_id}/positions
```

---

## 7. 报名管理模块

### 7.1 学生端 - 提交报名

提交新的报名申请。

**接口地址：**
```
POST /api/student/signup/applications
Authorization: Bearer {token}
```

**请求体：**
```json
{
  "recruitment_session_id": 1,
  "position_ids": [1, 2, 3],
  "self_intro": "我是一名对编程充满热情的学生"
}
```

**响应：**
```json
{
  "code": 200,
  "data": {
    "signup_id": 123,
    "status": "PENDING"
  },
  "message": "报名成功"
}
```

---

### 7.2 学生端 - 获取我的报名列表

获取当前用户的报名列表。

**接口地址：**
```
GET /api/student/signup/applications?recruitment_session_id={id}&status={status}&page={page}&page_size={size}
Authorization: Bearer {token}
```

**响应：**
```json
{
  "code": 200,
  "data": {
    "items": [
      {
        "id": 123,
        "user_id": 10,
        "recruitment_session_id": 1,
        "self_intro": "我是一名对编程充满热情的学生",
        "status": "PENDING",
        "audit_time": null,
        "audit_reason": null,
        "created_at": "2026-01-05T10:00:00",
        "items": [
          {
            "id": 1,
            "signup_session_id": 123,
            "department_id": 4,
            "position_id": 1
          }
        ]
      }
    ],
    "total": 15
  },
  "message": ""
}
```

---

### 7.3 学生端 - 获取报名详情

获取指定报名记录的详细信息。

**接口地址：**
```
GET /api/student/applications/{application_id}
Authorization: Bearer {token}
```

---

### 7.4 学生端 - 更新报名

更新待审核状态的报名申请。

**接口地址：**
```
PUT /api/student/applications/{application_id}
Authorization: Bearer {token}
```

---

### 7.5 学生端 - 取消报名

取消待审核状态的报名申请。

**接口地址：**
```
DELETE /api/student/applications/{application_id}
Authorization: Bearer {token}
```

**响应：** 204 No Content

---

### 7.6 管理端 - 获取报名审核列表

获取指定招新场次的报名列表。

**接口地址：**
```
GET /api/admin/signup/applications?recruitment_session_id={id}&status={status}&page={page}&page_size={size}
Authorization: Bearer {token}
```

**响应：**
```json
{
  "items": [
    {
      "id": 123,
      "user_id": 10,
      "user_name": "张三",
      "user_phone": "13800138000",
      "user_email": "zhangsan@example.com",
      "recruitment_session_id": 1,
      "self_intro": "我是一名对编程充满热情的学生",
      "status": "PENDING",
      "audit_time": null,
      "audit_reason": null,
      "created_at": "2026-01-05T10:00:00",
      "items": [...],
      "attachments": []
    }
  ],
  "total": 45
}
```

---

### 7.7 管理端 - 获取报名详情

获取指定报名记录的完整详情（包含用户信息）。

**接口地址：**
```
GET /api/admin/signup/applications/{signup_id}
Authorization: Bearer {token}
```

---

### 7.8 管理端 - 审核报名

审核报名申请，通过或拒绝。

**接口地址：**
```
POST /api/admin/signup/applications/{signup_id}/audit
Authorization: Bearer {token}
```

**请求体：**
```json
{
  "status": "APPROVED"
}
```

或拒绝：
```json
{
  "status": "REJECTED",
  "reason": "该岗位已满员"
}
```

**响应：**
```json
{
  "detail": "审核完成",
  "signup_id": 123,
  "new_status": "APPROVED"
}
```

---

### 7.9 管理端 - 删除报名记录

删除指定的报名记录（软删除）。

**接口地址：**
```
DELETE /api/admin/signup/applications/{signup_id}
Authorization: Bearer {token}
```

---

## 8. 面试管理模块

### 8.1 创建面试场次

创建新的面试场次。

**接口地址：**
```
POST /api/interview/sessions
Authorization: Bearer {token}
```

**请求体：**
```json
{
  "club_id": 1,
  "name": "第一轮面试",
  "description": "技术面试",
  "start_time": "2026-01-10T09:00:00",
  "end_time": "2026-01-10T18:00:00"
}
```

---

### 8.2 获取面试场次列表

获取社团的面试场次列表。

**接口地址：**
```
GET /api/interview/sessions?club_id={club_id}&status={status}
Authorization: Bearer {token}
```

---

### 8.3 安排候选人

为候选人安排面试时间。

**接口地址：**
```
POST /api/interview/candidates
Authorization: Bearer {token}
```

**请求体：**
```json
{
  "session_id": 1,
  "candidate_user_id": 10,
  "interviewer_ids": [1, 2],
  "planned_start_time": "2026-01-10T10:00:00",
  "planned_end_time": "2026-01-10T11:00:00"
}
```

---

### 8.4 确认面试

候选人确认或拒绝面试邀请。

**接口地址：**
```
PUT /api/interviews/{interview_id}/confirmation
Authorization: Bearer {token}
```

**请求体：**
```json
{
  "status": "CONFIRMED"
}
```

---

### 8.5 提交面试记录

面试官提交面试记录和评分。

**接口地址：**
```
POST /api/interviews/{interview_id}/records
Authorization: Bearer {token}
```

---

### 8.6 获取面试结果

查看面试成绩和录取结果。

**接口地址：**
```
GET /api/interviews/{interview_id}/result
Authorization: Bearer {token}
```

---

## 9. 学生端模块

### 9.1 获取我的面试列表

获取当前用户的所有面试安排。

**接口地址：**
```
GET /api/student/interviews/my
Authorization: Bearer {token}
```

**响应：**
```json
[
  {
    "id": 1,
    "session_id": 1,
    "signup_session_id": 123,
    "candidate_user_id": 10,
    "planned_start_time": "2026-01-10T10:00:00",
    "planned_end_time": "2026-01-10T11:00:00",
    "actual_start_time": null,
    "actual_end_time": null,
    "status": "SCHEDULED",
    "final_score": null,
    "created_at": "2026-01-05T10:00:00"
  }
]
```

---

### 9.2 获取通知列表

获取用户的通知列表。

**接口地址：**
```
GET /api/student/notifications?unread_only={true|false}
Authorization: Bearer {token}
```

**响应：**
```json
[
  {
    "id": 1,
    "type": "AUDIT_RESULT",
    "title": "报名审核结果",
    "content": "您的报名已通过审核",
    "biz_id": 123,
    "sent_at": "2026-01-05T10:00:00",
    "created_at": "2026-01-05T10:00:00"
  }
]
```

---

### 9.3 标记通知为已读

标记指定通知为已读。

**接口地址：**
```
PUT /api/student/notifications/{id}/read
Authorization: Bearer {token}
```

---

### 9.4 标记所有通知为已读

标记所有通知为已读。

**接口地址：**
```
PUT /api/student/notifications/read-all
Authorization: Bearer {token}
```

---

### 9.5 获取未读通知数量

获取未读通知数量。

**接口地址：**
```
GET /api/student/notifications/count
Authorization: Bearer {token}
```

**响应：**
```json
{
  "count": 5
}
```

---

### 9.6 提交工单

提交问题咨询工单。

**接口地址：**
```
POST /api/student/tickets
Authorization: Bearer {token}
```

**请求体：**
```json
{
  "title": "报名相关问题",
  "content": "请问如何修改我的报名信息？",
  "category": "报名咨询",
  "club_id": 1
}
```

---

### 9.7 获取我的工单列表

获取当前用户提交的工单列表。

**接口地址：**
```
GET /api/student/tickets/my
Authorization: Bearer {token}
```

---

### 9.8 获取工单详情

获取指定工单的详情和回复列表。

**接口地址：**
```
GET /api/student/tickets/{ticket_id}
Authorization: Bearer {token}
```

---

### 9.9 添加工单回复

为工单添加新的回复。

**接口地址：**
```
POST /api/student/tickets/{ticket_id}/messages
Authorization: Bearer {token}
```

**请求体：**
```json
{
  "content": "请问什么时候能回复？",
  "attachment_url": "http://example.com/file.pdf"
}
```

---

### 9.10 获取个人资料

获取当前用户的个人资料。

**接口地址：**
```
GET /api/student/students/profile
Authorization: Bearer {token}
```

**响应：**
```json
{
  "id": 10,
  "phone": "13800138000",
  "name": "张三",
  "id_card_no": "330106200001011234",
  "school_code": "4133013021",
  "major": "计算机科学与技术",
  "student_no": "202001001",
  "avatar_url": "http://example.com/avatar.jpg",
  "email": "zhangsan@example.com",
  "is_verified_campus": true,
  "created_at": "2026-01-01T00:00:00"
}
```

---

### 9.11 更新个人资料

更新当前用户的个人资料。

**接口地址：**
```
PUT /api/student/students/profile
Authorization: Bearer {token}
```

**请求体：**
```json
{
  "name": "李四",
  "email": "lisi@example.com",
  "major": "软件工程"
}
```

---

### 9.12 获取报名统计

获取当前用户的报名统计数据。

**接口地址：**
```
GET /api/student/students/applications/stats
Authorization: Bearer {token}
```

**响应：**
```json
{
  "total": 5,
  "pending": 2,
  "approved": 2,
  "rejected": 1
}
```

---

### 9.13 获取FAQ列表

获取常见问题列表。

**接口地址：**
```
GET /api/student/faqs?category={category}&club_id={club_id}
```

**查询参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| category | string | 否 | 筛选指定分类 |
| club_id | number | 否 | 筛选指定社团的FAQ |

**响应：**
```json
[
  {
    "id": 1,
    "club_id": null,
    "category": "报名相关",
    "question": "如何修改我的报名信息？",
    "answer": "请在报名审核前通过个人中心修改...",
    "order_no": 1,
    "is_pinned": true,
    "created_at": "2026-01-01T00:00:00"
  }
]
```

---

## 数据模型

### 状态枚举

#### 社团状态 (Club Status)
| 值 | 说明 |
|-----|------|
| PENDING | 待审核 |
| APPROVED | 已通过 |
| REJECTED | 已拒绝 |
| ACTIVE | 活跃中 |

#### 招新场次状态 (Recruitment Session Status)
| 值 | 说明 |
|-----|------|
| DRAFT | 草稿 |
| PUBLISHED | 已发布 |
| CLOSED | 已结束 |

#### 报名状态 (Signup Status)
| 值 | 说明 |
|-----|------|
| PENDING | 待审核 |
| APPROVED | 已通过 |
| REJECTED | 已拒绝 |
| CANCELLED | 已取消 |

#### 面试状态 (Interview Status)
| 值 | 说明 |
|-----|------|
| PENDING | 待确认 |
| CONFIRMED | 已确认 |
| DECLINED | 已拒绝 |
| SCHEDULED | 已排期 |
| IN_PROGRESS | 面试中 |
| COMPLETED | 已完成 |
| CANCELLED | 已取消 |

### 通用响应结构

#### 成功响应
```json
{
  "code": 200,
  "data": {},
  "message": "操作成功"
}
```

#### 错误响应
```json
{
  "detail": "错误描述信息"
}
```

---

## 错误码说明

| HTTP状态码 | 说明 |
|-----------|------|
| 200 | 请求成功 |
| 201 | 创建成功 |
| 204 | 删除成功（无响应体） |
| 400 | 请求参数错误 |
| 403 | 无权限访问 |
| 404 | 资源不存在 |
| 409 | 资源冲突 |
| 422 | 参数验证失败 |
| 500 | 服务器内部错误 |

### 常见错误示例

**重复报名：**
```json
{
  "detail": "您已经报名过该招新场次"
}
```

**无权访问：**
```json
{
  "detail": "无权访问他人的报名记录"
}
```

**资源不存在：**
```json
{
  "detail": "招新场次不存在"
}
```

**状态不允许操作：**
```json
{
  "detail": "只有待审核状态可以修改"
}
```

---

## 附录

### 完整请求流程示例

#### 学生报名流程

1. **登录获取Token**
```bash
POST /api/auth/login
{
  "phone": "13800138000",
  "password": "password123"
}
```

2. **查看招新场次**
```bash
GET /api/recruitment/sessions?club_id=1&status=PUBLISHED
```

3. **提交报名**
```bash
POST /api/student/signup/applications
Authorization: Bearer {token}
{
  "recruitment_session_id": 1,
  "position_ids": [1, 2],
  "self_intro": "我想加入技术部"
}
```

4. **查看报名状态**
```bash
GET /api/student/signup/applications
Authorization: Bearer {token}
```

#### 管理员审核流程

1. **获取待审核列表**
```bash
GET /api/admin/signup/applications?recruitment_session_id=1&status=PENDING
Authorization: Bearer {token}
```

2. **查看报名详情**
```bash
GET /api/admin/signup/applications/123
Authorization: Bearer {token}
```

3. **审核通过**
```bash
POST /api/admin/signup/applications/123/audit
Authorization: Bearer {token}
{
  "status": "APPROVED"
}
```

---

## 更新日志

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0.0 | 2026-01-05 | 初始版本，完成所有核心功能接口 |
