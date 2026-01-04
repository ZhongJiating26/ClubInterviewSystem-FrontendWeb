import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import AdminLayout from '@/layouts/AdminLayout.vue'
import InterviewerLayout from '@/layouts/InterviewerLayout.vue'
import StudentLayout from '@/layouts/StudentLayout.vue'
import { useUserStore } from '@/stores/user'

// 公开页面，不需要登录
const publicPaths = ['/login', '/register', '/forget-password', '/role-select', '/init', '/404']

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    // 根路径由路由守卫处理重定向
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
  // 角色选择页（无布局）
  {
    path: '/role-select',
    name: 'RoleSelect',
    component: () => import('@/views/RoleSelect.vue'),
    meta: { title: '选择角色' }
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
        meta: { title: '报名管理' },
        redirect: { name: 'ApplicationsCreate' },
        children: [
          {
            path: 'create',
            name: 'ApplicationsCreate',
            component: () => import('@/views/admin/applications/Create.vue'),
            meta: { title: '发布报名' }
          },
          {
            path: 'session/:id',
            name: 'SessionWizard',
            component: () => import('@/views/admin/applications/SessionWizard.vue'),
            meta: { title: '招新场次向导' }
          },
          {
            path: 'history',
            name: 'ApplicationsHistory',
            component: () => import('@/views/admin/applications/History.vue'),
            meta: { title: '历史报名记录' }
          },
          {
            path: 'review',
            name: 'ApplicationsReview',
            component: () => import('@/views/admin/applications/Review.vue'),
            meta: { title: '报名审核' }
          }
        ]
      },
      {
        path: 'interviews',
        name: 'Interviews',
        component: () => import('@/views/admin/Interviews.vue'),
        meta: { title: '面试管理' },
        children: [
          {
            path: 'create',
            name: 'InterviewsCreate',
            component: () => import('@/views/admin/interviews/Create.vue'),
            meta: { title: '发布面试' }
          },
          {
            path: 'records',
            name: 'InterviewsRecords',
            component: () => import('@/views/admin/interviews/Records.vue'),
            meta: { title: '面试记录' }
          },
          {
            path: 'filter',
            name: 'InterviewsFilter',
            component: () => import('@/views/admin/interviews/Filter.vue'),
            meta: { title: '面试筛选' }
          }
        ]
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
      },
      {
        path: 'clubs',
        name: 'Clubs',
        meta: { title: '社团管理' },
        children: [
          {
            path: 'profile',
            name: 'ClubsProfile',
            component: () => import('@/views/admin/clubs/Profile.vue'),
            meta: { title: '社团资料' }
          },
          {
            path: 'departments',
            name: 'ClubsDepartments',
            component: () => import('@/views/admin/clubs/Departments.vue'),
            meta: { title: '部门管理' }
          },
          {
            path: 'positions',
            name: 'ClubsPositions',
            component: () => import('@/views/admin/clubs/Positions.vue'),
            meta: { title: '岗位管理' }
          },
          {
            path: 'members',
            name: 'ClubsMembers',
            component: () => import('@/views/admin/clubs/Members.vue'),
            meta: { title: '社团人员管理' }
          }
        ]
      },
      {
        path: 'settings',
        name: 'AdminSettings',
        component: () => import('@/views/admin/settings/Settings.vue'),
        meta: { title: '系统设置' }
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
        path: 'home',
        name: 'StudentHome',
        component: () => import('@/views/student/Home.vue'),
        meta: { title: '首页' }
      },
      {
        path: 'interviews',
        name: 'StudentInterviews',
        component: () => import('@/views/student/Interviews.vue'),
        meta: { title: '面试' }
      },
      {
        path: 'profile',
        name: 'StudentProfile',
        component: () => import('@/views/student/Profile.vue'),
        meta: { title: '我的' }
      }
    ]
  },
  // 404 页面
  {
    path: '/404',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
    meta: { title: '页面未找到' }
  },
  // 捕获所有未匹配路由
  {
    path: '/:pathMatch(.*)*',
    redirect: '/404'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫：权限验证
router.beforeEach(async (to, from, next) => {
  document.title = `${to.meta.title as string || '社团面试系统'} - 社团面试系统`

  const userStore = useUserStore()
  const isLoggedIn = !!userStore.token

  // 公开页面直接放行
  if (publicPaths.some(path => to.path.startsWith(path))) {
    // 如果已登录访问登录页，跳转到首页
    if (isLoggedIn && to.path === '/login') {
      next('/student/home')
    } else {
      next()
    }
    return
  }

  // 未登录则跳转到登录页
  if (!isLoggedIn) {
    next({ path: '/login', query: { redirect: to.fullPath } })
    return
  }

  // 如果没有用户信息，先获取
  if (!userStore.userInfo) {
    try {
      const { getMe } = await import('@/api/modules/auth')
      const userData = await getMe()
      userStore.setUserInfo(userData)
    } catch (e) {
      // 获取失败，清除 token 并跳转登录
      userStore.logout()
      next('/login')
      return
    }
  }

  // 根路径根据角色跳转
  if (to.path === '/') {
    const role = userStore.primaryRole || 'student'
    const redirectMap: Record<string, string> = {
      admin: '/admin/dashboard',
      interviewer: '/interviewer/tasks',
      student: '/student/home'
    }
    next(redirectMap[role] || '/student/home')
    return
  }

  next()
})

export default router
