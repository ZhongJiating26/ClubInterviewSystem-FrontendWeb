import { get, post } from '../request'

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
