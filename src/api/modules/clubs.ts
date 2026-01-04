import axios, { get, post, put, del } from '../request'

export interface ClubInfo {
  id: number
  school_name: string
  name: string
  logo_url: string
  category: string
  description: string | null
  cert_file_url: string | null
  status: string
  created_at: string
}

export interface ClubProfileCheckResponse {
  club_id: number
  is_complete: boolean
  missing_fields: string[]
}

export interface ClubCheckResponse {
  exists: boolean
  club_id: number | null
  message: string
}

// 部门相关接口
export interface Department {
  id: number
  club_id: number
  name: string
  description: string | null
  created_at: string
  updated_at: string
}

// 岗位相关接口
export interface Position {
  id: number
  club_id: number
  department_id: number | null
  name: string
  description: string | null
  requirement: string | null
  created_at: string
  updated_at: string
}

// 社团资料检查
export function checkClubProfile(clubId: number) {
  return get<ClubProfileCheckResponse>(`/clubs/${clubId}/profile-check`)
}

// 检查社团是否存在
export function checkClub(data: { club_name: string; school_code: string }) {
  return post<ClubCheckResponse>('/clubs/check', data)
}

// 将用户关联到社团
export function bindUserToClub(clubId: number, data: { user_id: number; role_id: number }) {
  return post(`/clubs/${clubId}/bind-user`, data)
}

// 获取社团详情
export function getClub(clubId: number) {
  return get<ClubInfo>(`/clubs/${clubId}`)
}

// 更新社团信息（支持传文件）
export function updateClub(clubId: number, data: {
  name?: string
  category?: string
  description?: string
  logo?: File | null
}) {
  // 如果有 logo 文件，使用 multipart/form-data
  if (data.logo) {
    const formData = new FormData()
    if (data.name !== undefined) formData.append('name', data.name)
    if (data.category !== undefined) formData.append('category', data.category)
    if (data.description !== undefined) formData.append('description', data.description)
    formData.append('logo', data.logo)
    return axios.put(`/clubs/${clubId}`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  }

  // 否则使用 JSON
  return put(`/clubs/${clubId}`, {
    name: data.name,
    category: data.category,
    description: data.description
  })
}

// ==================== 部门管理 ====================

// 获取部门列表
export function getDepartments(clubId: number) {
  return get<Department[]>(`/clubs/${clubId}/departments`)
}

// 创建部门
export function createDepartment(clubId: number, data: {
  name: string
  description?: string
}) {
  return post<Department>(`/clubs/${clubId}/departments`, data)
}

// 更新部门
export function updateDepartment(clubId: number, deptId: number, data: {
  name?: string
  description?: string
}) {
  return put<Department>(`/clubs/${clubId}/departments/${deptId}`, data)
}

// 删除部门
export function deleteDepartment(clubId: number, deptId: number) {
  return del(`/clubs/${clubId}/departments/${deptId}`)
}

// ==================== 岗位管理 ====================

// 获取岗位列表
export function getPositions(clubId: number, params?: { department_id?: number }) {
  return get<Position[]>(`/clubs/${clubId}/positions`, params)
}

// 创建岗位
export function createPosition(clubId: number, data: {
  department_id?: number
  name: string
  description?: string
  requirement?: string
}) {
  return post<Position>(`/clubs/${clubId}/positions`, data)
}

// 更新岗位
export function updatePosition(clubId: number, posId: number, data: {
  name?: string
  description?: string
  requirement?: string
}) {
  return put<Position>(`/clubs/${clubId}/positions/${posId}`, data)
}

// 删除岗位
export function deletePosition(clubId: number, posId: number) {
  return del(`/clubs/${clubId}/positions/${posId}`)
}
