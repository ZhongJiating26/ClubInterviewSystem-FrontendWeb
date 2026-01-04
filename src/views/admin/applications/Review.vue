<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import {
  getSignupApplications,
  getSignupApplicationDetail,
  auditSignupApplication,
  type SignupApplication,
  type SignupStatus,
} from '@/api/modules/application'
import {
  getRecruitmentSessions,
  type RecruitmentSession,
} from '@/api/modules/recruitment'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Search, Check, X, Eye, Clock, User } from 'lucide-vue-next'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

// 报名列表
const applications = ref<SignupApplication[]>([])
const total = ref(0)
const loading = ref(false)
const error = ref('')
const success = ref('')

// 分页
const page = ref(1)
const pageSize = ref(20)
const statusFilter = ref<SignupStatus | ''>('')

// 招新场次列表（用于筛选）
const sessions = ref<RecruitmentSession[]>([])
const selectedSessionId = ref<number | null>(null)

// 详情弹窗
const showDetailDialog = ref(false)
const currentApplication = ref<SignupApplication | null>(null)

// 岗位详情缓存
const positionDetails = ref<Record<number, any>>({})

// 获取岗位名称
const getPositionName = (positionId: number) => {
  // 从缓存中查找
  if (positionDetails.value[positionId]) {
    return positionDetails.value[positionId].name
  }
  return `岗位 #${positionId}`
}

// 审核弹窗
const showAuditDialog = ref(false)
const auditLoading = ref(false)
const auditForm = ref({
  status: 'APPROVED' as 'APPROVED' | 'REJECTED',
  reason: '',
})

// 获取社团 ID
const getClubId = () => {
  return userStore.userInfo?.roles.find((r) => r.code === 'CLUB_ADMIN')?.club_id
}

// 获取招新场次列表
const fetchSessions = async () => {
  const clubId = getClubId()
  if (!clubId) return

  try {
    const res = await getRecruitmentSessions({ club_id: clubId })
    sessions.value = res

    // 如果 URL 有 session_id 参数，设置为选中状态
    const sessionId = route.query.session_id
    if (sessionId) {
      selectedSessionId.value = Number(sessionId)
    } else if (res.length > 0) {
      selectedSessionId.value = res[0].id
    }
  } catch (err) {
    console.error('获取招新场次失败', err)
  }
}

// 获取报名列表
const fetchApplications = async () => {
  if (!selectedSessionId.value) {
    applications.value = []
    total.value = 0
    return
  }

  try {
    loading.value = true
    error.value = ''

    const res = await getSignupApplications({
      recruitment_session_id: selectedSessionId.value,
      status: statusFilter.value || undefined,
      page: page.value,
      page_size: pageSize.value,
    })

    applications.value = res.items
    total.value = res.total
  } catch (err: any) {
    error.value = err.message || '获取报名列表失败'
  } finally {
    loading.value = false
  }
}

// 查看详情
const viewDetail = async (app: SignupApplication) => {
  try {
    const res = await getSignupApplicationDetail(app.id)
    currentApplication.value = res
    showDetailDialog.value = true
  } catch (err: any) {
    error.value = err.message || '获取详情失败'
  }
}

// 打开发送审核弹窗
const openAuditDialog = (app: SignupApplication, status: 'APPROVED' | 'REJECTED') => {
  currentApplication.value = app
  auditForm.value = {
    status,
    reason: status === 'REJECTED' ? '' : '',
  }
  showAuditDialog.value = true
}

// 提交审核
const handleAudit = async () => {
  if (!currentApplication.value) return

  if (auditForm.value.status === 'REJECTED' && !auditForm.value.reason.trim()) {
    error.value = '请输入拒绝理由'
    return
  }

  try {
    auditLoading.value = true
    error.value = ''

    await auditSignupApplication(currentApplication.value.id, auditForm.value)
    success.value = '审核完成'
    showAuditDialog.value = false
    await fetchApplications()
  } catch (err: any) {
    error.value = err.message || '审核失败'
  } finally {
    auditLoading.value = false
  }
}

// 状态文本
const statusText: Record<string, string> = {
  PENDING: '待审核',
  APPROVED: '已通过',
  REJECTED: '已拒绝',
}

// 状态样式
const getStatusBadge = (status: string) => {
  switch (status) {
    case 'APPROVED':
      return 'bg-green-100 text-green-800'
    case 'PENDING':
      return 'bg-yellow-100 text-yellow-800'
    case 'REJECTED':
      return 'bg-red-100 text-red-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

// 格式化日期
const formatDate = (dateStr: string) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString('zh-CN')
}

// 监听筛选条件变化
const onFilterChange = () => {
  page.value = 1
  fetchApplications()
}

// 监听路由变化
const onRouteChange = () => {
  const sessionId = route.query.session_id
  if (sessionId) {
    selectedSessionId.value = Number(sessionId)
    fetchApplications()
  }
}

onMounted(async () => {
  await fetchSessions()
  await fetchApplications()
})
</script>

<template>
  <div class="p-6">
    <div class="mb-6">
      <h1 class="text-2xl font-bold mb-4">报名审核</h1>

      <!-- 筛选器 -->
      <div class="flex gap-4 mb-4">
        <div class="w-64">
          <Select v-model="selectedSessionId" @update:model-value="fetchApplications">
            <SelectTrigger>
              <SelectValue placeholder="选择招新场次" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem v-for="session in sessions" :key="session.id" :value="session.id.toString()">
                {{ session.name }}
              </SelectItem>
            </SelectContent>
          </Select>
        </div>
        <div class="w-40">
          <Select v-model="statusFilter" @update:model-value="onFilterChange">
            <SelectTrigger>
              <SelectValue placeholder="全部状态" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="">全部状态</SelectItem>
              <SelectItem value="PENDING">待审核</SelectItem>
              <SelectItem value="APPROVED">已通过</SelectItem>
              <SelectItem value="REJECTED">已拒绝</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>
    </div>

    <!-- 错误提示 -->
    <div v-if="error" class="mb-4 p-3 text-sm text-red-600 bg-red-50 rounded-md">
      {{ error }}
    </div>

    <!-- 成功提示 -->
    <div v-if="success" class="mb-4 p-3 text-sm text-green-600 bg-green-50 rounded-md">
      {{ success }}
    </div>

    <!-- 报名列表 -->
    <div class="space-y-4">
      <Card v-for="app in applications" :key="app.id" class="border-0">
        <CardContent class="py-4">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <div class="flex items-center gap-3 mb-2">
                <span class="font-medium">报名人</span>
                <span :class="['px-2 py-0.5 text-xs rounded-full', getStatusBadge(app.status)]">
                  {{ statusText[app.status] }}
                </span>
              </div>
              <p class="text-sm text-muted-foreground mb-1">
                自我介绍：{{ app.self_intro || '暂无' }}
              </p>
              <p class="text-xs text-muted-foreground">
                报名时间：{{ formatDate(app.created_at) }}
              </p>
              <p v-if="app.audit_reason" class="text-xs text-red-500 mt-1">
                拒绝理由：{{ app.audit_reason }}
              </p>
            </div>
            <div class="flex gap-2">
              <Button variant="outline" size="sm" @click="viewDetail(app)">
                <Eye class="w-4 h-4 mr-1" />
                详情
              </Button>
              <Button
                v-if="app.status === 'PENDING'"
                variant="outline"
                size="sm"
                class="text-green-600"
                @click="openAuditDialog(app, 'APPROVED')"
              >
                <Check class="w-4 h-4 mr-1" />
                通过
              </Button>
              <Button
                v-if="app.status === 'PENDING'"
                variant="outline"
                size="sm"
                class="text-red-600"
                @click="openAuditDialog(app, 'REJECTED')"
              >
                <X class="w-4 h-4 mr-1" />
                拒绝
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      <!-- 空状态 -->
      <div v-if="applications.length === 0 && !loading" class="text-center py-12">
        <p class="text-muted-foreground">暂无报名记录</p>
      </div>

      <!-- 加载状态 -->
      <div v-if="loading" class="text-center py-12">
        <p class="text-muted-foreground">加载中...</p>
      </div>
    </div>

    <!-- 分页 -->
    <div v-if="total > pageSize" class="mt-4 flex justify-center gap-2">
      <Button
        variant="outline"
        size="sm"
        :disabled="page === 1"
        @click="page--; fetchApplications()"
      >
        上一页
      </Button>
      <span class="text-sm text-muted-foreground py-2">
        第 {{ page }} 页 / 共 {{ Math.ceil(total / pageSize) }} 页
      </span>
      <Button
        variant="outline"
        size="sm"
        :disabled="page >= Math.ceil(total / pageSize)"
        @click="page++; fetchApplications()"
      >
        下一页
      </Button>
    </div>

    <!-- 详情弹窗 -->
    <Dialog :open="showDetailDialog" @update:open="showDetailDialog = $event">
      <DialogContent class="max-w-lg">
        <DialogHeader>
          <DialogTitle>报名详情</DialogTitle>
          <DialogDescription>查看报名人信息及所选岗位</DialogDescription>
        </DialogHeader>
        <div v-if="currentApplication" class="space-y-4 py-4">
          <!-- 用户信息 -->
          <div class="space-y-2">
            <Label class="flex items-center gap-2">
              <User class="w-4 h-4" />
              报名人信息
            </Label>
            <div class="bg-gray-50 rounded-md p-3 space-y-2">
              <div class="flex justify-between text-sm">
                <span class="text-muted-foreground">用户ID</span>
                <span class="font-medium">{{ currentApplication.user_id }}</span>
              </div>
              <div v-if="currentApplication.user_name" class="flex justify-between text-sm">
                <span class="text-muted-foreground">姓名</span>
                <span class="font-medium">{{ currentApplication.user_name }}</span>
              </div>
              <div v-if="currentApplication.user_phone" class="flex justify-between text-sm">
                <span class="text-muted-foreground">电话</span>
                <span class="font-medium">{{ currentApplication.user_phone }}</span>
              </div>
              <div v-if="currentApplication.user_email" class="flex justify-between text-sm">
                <span class="text-muted-foreground">邮箱</span>
                <span class="font-medium">{{ currentApplication.user_email }}</span>
              </div>
            </div>
          </div>

          <!-- 状态 -->
          <div class="space-y-2">
            <Label>状态</Label>
            <div>
              <span :class="['px-2 py-1 text-xs rounded-full', getStatusBadge(currentApplication.status)]">
                {{ statusText[currentApplication.status] }}
              </span>
            </div>
          </div>

          <!-- 自我介绍 -->
          <div class="space-y-2">
            <Label>自我介绍</Label>
            <p class="text-sm bg-gray-50 rounded-md p-3">{{ currentApplication.self_intro || '暂无' }}</p>
          </div>

          <!-- 报名岗位 -->
          <div v-if="currentApplication.items && currentApplication.items.length > 0" class="space-y-2">
            <Label>报名岗位</Label>
            <div class="space-y-2">
              <div
                v-for="item in currentApplication.items"
                :key="item.id"
                class="flex items-center justify-between text-sm bg-gray-50 rounded p-3"
              >
                <div class="flex items-center gap-2">
                  <span class="font-medium">{{ getPositionName(item.position_id) }}</span>
                  <span class="text-xs text-muted-foreground">
                    部门: {{ item.department_id || '未指定' }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- 时间信息 -->
          <div class="space-y-2">
            <Label>时间信息</Label>
            <div class="bg-gray-50 rounded-md p-3 space-y-1 text-sm">
              <div class="flex justify-between">
                <span class="text-muted-foreground">报名时间</span>
                <span>{{ formatDate(currentApplication.created_at) }}</span>
              </div>
              <div v-if="currentApplication.audit_time" class="flex justify-between">
                <span class="text-muted-foreground">审核时间</span>
                <span>{{ formatDate(currentApplication.audit_time) }}</span>
              </div>
            </div>
          </div>

          <!-- 拒绝理由 -->
          <div v-if="currentApplication.audit_reason" class="space-y-2">
            <Label>拒绝理由</Label>
            <p class="text-sm text-red-600 bg-red-50 rounded-md p-3">{{ currentApplication.audit_reason }}</p>
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" @click="showDetailDialog = false">关闭</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>

    <!-- 审核弹窗 -->
    <Dialog :open="showAuditDialog" @update:open="showAuditDialog = $event">
      <DialogContent class="max-w-md">
        <DialogHeader>
          <DialogTitle>{{ auditForm.status === 'APPROVED' ? '通过报名' : '拒绝报名' }}</DialogTitle>
          <DialogDescription>
            {{ auditForm.status === 'APPROVED' ? '确认通过该报名申请' : '请输入拒绝理由' }}
          </DialogDescription>
        </DialogHeader>
        <div class="space-y-4 py-4">
          <div v-if="auditForm.status === 'REJECTED'" class="space-y-2">
            <Label for="reason">拒绝理由 *</Label>
            <Textarea
              id="reason"
              v-model="auditForm.reason"
              placeholder="请输入拒绝理由"
              rows="3"
            />
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" @click="showAuditDialog = false">取消</Button>
          <Button
            :variant="auditForm.status === 'APPROVED' ? 'default' : 'destructive'"
            @click="handleAudit"
            :disabled="auditLoading"
          >
            {{ auditLoading ? '处理中...' : '确认' }}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  </div>
</template>
