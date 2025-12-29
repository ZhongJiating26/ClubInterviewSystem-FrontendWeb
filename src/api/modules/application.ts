import { get, post, put, del } from '../request'

export interface Application {
  id: number
  studentId: number
  studentName: string
  studentNo: string
  major: string
  phone: string
  email: string
  department: string
  introduction: string
  status: 'pending' | 'approved' | 'rejected'
  applyTime: string
  reviewTime?: string
  reviewBy?: string
  remark?: string
}

export interface ApplicationListParams {
  page: number
  pageSize: number
  status?: string
  department?: string
  keyword?: string
}

export function getApplicationList(params: ApplicationListParams) {
  return get('/applications', params)
}

export function getApplicationDetail(id: number) {
  return get(`/applications/${id}`)
}

export function approveApplication(id: number, remark?: string) {
  return put(`/applications/${id}/approve`, { remark })
}

export function rejectApplication(id: number, remark: string) {
  return put(`/applications/${id}/reject`, { remark })
}

export function exportApplications(params: any) {
  return post('/applications/export', params, { responseType: 'blob' })
}
