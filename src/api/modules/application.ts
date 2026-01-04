import { get, post, put, del } from '../request'

// 报名状态
export type SignupStatus = 'PENDING' | 'APPROVED' | 'REJECTED'

// 报名的岗位项
export interface SignupItem {
  id: number
  signup_session_id: number
  department_id: number | null
  position_id: number
}

// 报名信息
export interface SignupApplication {
  id: number
  user_id: number
  recruitment_session_id: number
  self_intro: string | null
  status: SignupStatus
  audit_user_id: number | null
  audit_time: string | null
  audit_reason: string | null
  created_at: string
  updated_at: string
  items: SignupItem[]
  attachments: any[]
  // 额外字段（可能由后端返回）
  user_name?: string
  user_phone?: string
  user_email?: string
  session_name?: string
}

// 报名列表响应
export interface SignupListResponse {
  items: SignupApplication[]
  total: number
}

// 审核报名请求
export interface AuditSignupData {
  status: 'APPROVED' | 'REJECTED'
  reason?: string
}

// 获取报名审核列表参数
export interface SignupListParams {
  recruitment_session_id: number
  status?: SignupStatus
  page?: number
  page_size?: number
}

// ==================== 报名审核（社团管理员） ====================

// 获取报名审核列表
export function getSignupApplications(params: SignupListParams) {
  return get<SignupListResponse>('/admin/signup/applications', params)
}

// 获取报名详情
export function getSignupApplicationDetail(id: number) {
  return get<SignupApplication>(`/admin/signup/applications/${id}`)
}

// 审核报名
export function auditSignupApplication(id: number, data: AuditSignupData) {
  return post<{ detail: string; signup_id: number; new_status: string }>(
    `/admin/signup/applications/${id}/audit`,
    data
  )
}
