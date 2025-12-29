import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import AdminLayout from '@/layouts/AdminLayout.vue'
import InterviewerLayout from '@/layouts/InterviewerLayout.vue'
import StudentLayout from '@/layouts/StudentLayout.vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  // 登录页（无布局）
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { title: '登录' }
  },
  // 注册页（无布局）
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue'),
    meta: { title: '注册' }
  },
  // 忘记密码页（无布局）
  {
    path: '/forget-password',
    name: 'ForgetPassword',
    component: () => import('@/views/ForgetPassword.vue'),
    meta: { title: '忘记密码' }
  },
  // 用户信息初始化页（无布局）
  {
    path: '/init',
    name: 'Init',
    component: () => import('@/views/Init.vue'),
    meta: { title: '初始化信息' }
  },
  // 管理员端（电脑web端布局）
  {
    path: '/admin',
    component: AdminLayout,
    meta: { roles: ['admin'] },
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/admin/Dashboard.vue'),
        meta: { title: '仪表盘' }
      },
      {
        path: 'applications',
        name: 'Applications',
        component: () => import('@/views/admin/Applications.vue'),
        meta: { title: '报名管理' }
      },
      {
        path: 'interviews',
        name: 'Interviews',
        component: () => import('@/views/admin/Interviews.vue'),
        meta: { title: '面试管理' }
      },
      {
        path: 'statistics',
        name: 'Statistics',
        component: () => import('@/views/admin/Statistics.vue'),
        meta: { title: '数据统计' }
      },
      {
        path: 'tickets',
        name: 'AdminTickets',
        component: () => import('@/views/admin/Tickets.vue'),
        meta: { title: '工单管理' }
      }
    ]
  },
  // 面试官端（电脑web端布局）
  {
    path: '/interviewer',
    component: InterviewerLayout,
    meta: { roles: ['interviewer'] },
    children: [
      {
        path: 'tasks',
        name: 'InterviewerTasks',
        component: () => import('@/views/interviewer/Tasks.vue'),
        meta: { title: '面试任务' }
      },
      {
        path: 'score/:id',
        name: 'Score',
        component: () => import('@/views/interviewer/Score.vue'),
        meta: { title: '评分' }
      }
    ]
  },
  // 学生端（手机h5端布局）
  {
    path: '/student',
    component: StudentLayout,
    meta: { roles: ['student'] },
    children: [
      {
        path: 'apply',
        name: 'Apply',
        component: () => import('@/views/student/Apply.vue'),
        meta: { title: '社团报名' }
      },
      {
        path: 'notifications',
        name: 'Notifications',
        component: () => import('@/views/student/Notifications.vue'),
        meta: { title: '通知中心' }
      },
      {
        path: 'tickets',
        name: 'StudentTickets',
        component: () => import('@/views/student/Tickets.vue'),
        meta: { title: '我的工单' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫：权限验证
router.beforeEach((to, _from, next) => {
  document.title = `${to.meta.title as string || '社团面试系统'} - 社团面试系统`
  // TODO: 从 Pinia 获取用户角色进行权限验证
  next()
})

export default router
