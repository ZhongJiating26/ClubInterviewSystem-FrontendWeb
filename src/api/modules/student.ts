import { get, post } from '../request'

export interface StudentApplication {
  id: number
  department: string
  introduction: string
  status: 'pending' | 'approved' | 'rejected'
  applyTime: string
  remark?: string
}

export function getMyApplication() {
  return get('/student/application')
}

export function submitApplication(data: {
  department: string
  introduction: string
}) {
  return post('/student/application', data)
}

export function getMyInterviewInfo() {
  return get('/student/interview')
}

export function updateProfile(data: {
  phone?: string
  email?: string
  nickname?: string
}) {
  return put('/student/profile', data)
}
