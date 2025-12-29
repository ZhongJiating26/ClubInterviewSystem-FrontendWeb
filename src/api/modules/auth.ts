import { get, post } from '../request'

export interface LoginParams {
  phone: string
  password: string
}

export interface LoginResult {
  access_token: string
  token_type: string
}

export interface UserRoleInfo {
  id: number
  code: string
  name: string
  club_id: number | null
}

export interface UserInfo {
  id: number
  phone: string
  name: string | null
  status: number
  is_initialized: boolean
  roles: UserRoleInfo[]
}

// 发送验证码
export function sendCode(data: { phone: string; scene: 'REGISTER' | 'LOGIN' }) {
  return post<{ message: string; dev_code: string | null }>('/auth/send-code', data)
}

// 注册（返回 access_token）
export function register(data: { phone: string; code: string }) {
  return post<{ access_token: string; token_type: string }>('/auth/register', data)
}

export function login(data: LoginParams) {
  return post<LoginResult>('/auth/login', data)
}

export function getMe() {
  return get<UserInfo>('/auth/me')
}

// 初始化账号（需要 token）
export function initAccount(data: {
  password: string
  name: string
  id_card_no: string
  school_code: string
  major: string
  student_no: string
  email?: string
  avatar_url?: string
}) {
  return post<{ detail: string }>('/auth/init', data)
}
