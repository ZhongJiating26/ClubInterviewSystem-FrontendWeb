import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { login as loginApi, getMe, type UserInfo } from '@/api/modules/auth'

export type UserRole = 'admin' | 'interviewer' | 'student'

export interface UserProfile extends UserInfo {
  primaryRole: UserRole | null
}

export const useUserStore = defineStore('user', () => {
  const router = useRouter()

  const token = ref<string>(localStorage.getItem('token') || '')
  const userInfo = ref<UserInfo | null>(null)

  // 获取主角色（优先级：admin > interviewer > student）
  const primaryRole = computed(() => {
    if (!userInfo.value?.roles.length) return null
    const roleCodes = userInfo.value.roles.map(r => r.code)
    if (roleCodes.includes('admin')) return 'admin'
    if (roleCodes.includes('interviewer')) return 'interviewer'
    if (roleCodes.includes('student')) return 'student'
    return null
  })

  // 设置 token
  function setToken(t: string) {
    token.value = t
    localStorage.setItem('token', t)
  }

  // 设置用户信息
  function setUserInfo(info: UserInfo) {
    userInfo.value = info
  }

  // 登录
  async function doLogin(phone: string, password: string) {
    const res = await loginApi({ phone, password })
    setToken(res.access_token)

    // 获取用户信息
    const userData = await getMe()
    setUserInfo(userData)

    return res
  }

  // 登出
  function logout() {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
    router.push('/login')
  }

  // 判断是否有某个角色
  function hasRole(role: UserRole): boolean {
    if (!userInfo.value?.roles.length) return false
    return userInfo.value.roles.some(r => r.code === role)
  }

  // 判断是否有任意角色
  function hasAnyRole(roles: UserRole[]): boolean {
    if (!userInfo.value?.roles.length) return false
    return userInfo.value.roles.some(r => roles.includes(r.code as UserRole))
  }

  return {
    token,
    userInfo,
    primaryRole,
    setToken,
    setUserInfo,
    doLogin,
    logout,
    hasRole,
    hasAnyRole
  }
})
