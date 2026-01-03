import axios, { get, post, put } from '../request'

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
