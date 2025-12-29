import { get, post, put, del } from '../request'

export interface Interview {
  id: number
  title: string
  department: string
  startTime: string
  endTime: string
  location: string
  interviewers: string[]
  status: 'pending' | 'ongoing' | 'completed' | 'cancelled'
  remark?: string
}

export interface InterviewListParams {
  page: number
  pageSize: number
  status?: string
  department?: string
  date?: string
}

export interface InterviewResult {
  id: number
  interviewId: number
  applicationId: number
  studentName: string
  studentNo: string
  interviewTime: string
  score?: number
  remark?: string
  status: 'pending' | 'scored' | 'absent'
}

export function getInterviewList(params: InterviewListParams) {
  return get('/interviews', params)
}

export function getInterviewDetail(id: number) {
  return get(`/interviews/${id}`)
}

export function createInterview(data: Partial<Interview>) {
  return post('/interviews', data)
}

export function updateInterview(id: number, data: Partial<Interview>) {
  return put(`/interviews/${id}`, data)
}

export function deleteInterview(id: number) {
  return del(`/interviews/${id}`)
}

export function getInterviewResults(interviewId: number, params?: any) {
  return get(`/interviews/${interviewId}/results`, params)
}

export function assignInterviewers(interviewId: number, interviewers: string[]) {
  return put(`/interviews/${interviewId}/interviewers`, { interviewers })
}

export function getMyInterviewTasks() {
  return get('/interviewer/tasks')
}

export function getStudentInterviewResult(studentId: number) {
  return get(`/students/${studentId}/interview-result`)
}
