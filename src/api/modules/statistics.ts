import { get } from '../request'

export interface StatisticsData {
  totalApplications: number
  pendingApplications: number
  approvedApplications: number
  rejectedApplications: number
  totalInterviews: number
  completedInterviews: number
  upcomingInterviews: number
}

export interface DepartmentStatistics {
  department: string
  total: number
  approved: number
  rejected: number
  pending: number
}

export interface DailyStatistics {
  date: string
  applications: number
  interviews: number
}

export function getOverviewStatistics() {
  return get('/statistics/overview')
}

export function getDepartmentStatistics(department?: string) {
  return get('/statistics/department', { department })
}

export function getDailyStatistics(params: { startDate: string; endDate: string; type?: string }) {
  return get('/statistics/daily', params)
}

export function getInterviewStatistics(interviewId?: number) {
  return get('/statistics/interview', { interviewId })
}

export function exportStatistics(params: any) {
  return post('/statistics/export', params, { responseType: 'blob' })
}
