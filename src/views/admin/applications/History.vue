<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import {
  getSignupApplications,
  getSignupApplicationDetail,
  type SignupApplication,
  type SignupStatus,
} from '@/api/modules/application'
import {
  getRecruitmentSessions,
  type RecruitmentSession,
} from '@/api/modules/recruitment'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Label } from '@/components/ui/label'
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
import { Calendar, Filter, Eye, User } from 'lucide-vue-next'

const userStore = useUserStore()

// 报名列表
const applications = ref<SignupApplication[]>([])
const total = ref(0)
const loading = ref(false)
const error = ref('')

// 招新场次列表
const sessions = ref<RecruitmentSession[]>([])
const selectedSessionId = ref<number | null>(null)

// 详情弹窗
const showDetailDialog = ref(false)
const currentApplication = ref<SignupApplication | null>(null)
const detailLoading = ref(false)

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
    if (res.length > 0) {
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
      page: 1,
      page_size: 100, // 显示更多历史记录
    })

    applications.value = res.items
    total.value = res.total
  } catch (err: any) {
    error.value = err.message || '获取报名列表失败'
  } finally {
    loading.value = false
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

// 查看详情
const viewDetail = async (app: SignupApplication) => {
  try {
    detailLoading.value = true
    const res = await getSignupApplicationDetail(app.id)
    currentApplication.value = res
    showDetailDialog.value = true
  } catch (err: any) {
    error.value = err.message || '获取详情失败'
  } finally {
    detailLoading.value = false
  }
}

// 格式化日期
const formatDate = (dateStr: string) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString('zh-CN')
}

onMounted(async () => {
  await fetchSessions()
  await fetchApplications()
})
</script>

<template>
  <div class="p-6">
    <div class="mb-6">
      <h1 class="text-2xl font-bold mb-4">历史报名记录</h1>

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
      </div>
    </div>

    <!-- 错误提示 -->
    <div v-if="error" class="mb-4 p-3 text-sm text-red-600 bg-red-50 rounded-md">
      {{ error }}
    </div>

    <!-- 报名统计 -->
    <div class="mb-4 flex gap-4 text-sm">
      <span class="text-muted-foreground">总计: {{ total }} 条报名记录</span>
    </div>

    <!-- 报名列表 -->
    <div class="space-y-3">
      <Card v-for="app in applications" :key="app.id" class="border-0">
        <CardContent class="py-3">
          <div class="flex items-center justify-between">
            <div class="flex-1">
              <div class="flex items-center gap-3">
                <span class="font-medium">报名人 #{{ app.user_id }}</span>
                <span :class="['px-2 py-0.5 text-xs rounded-full', getStatusBadge(app.status)]">
                  {{ statusText[app.status] }}
                </span>
              </div>
              <p class="text-sm text-muted-foreground mt-1">
                {{ app.self_intro || '暂无自我介绍' }}
              </p>
            </div>
            <div class="flex items-center gap-2">
              <Button variant="outline" size="sm" @click="viewDetail(app)">
                <Eye class="w-4 h-4 mr-1" />
                详情
              </Button>
              <div class="text-right text-sm text-muted-foreground">
                <p>{{ formatDate(app.created_at) }}</p>
                <p v-if="app.audit_time" class="text-xs">
                  审核: {{ formatDate(app.audit_time) }}
                </p>
              </div>
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
                class="text-sm bg-gray-50 rounded p-3"
              >
                <div class="font-medium">岗位 #{{ item.position_id }}</div>
                <div v-if="item.department_id" class="text-xs text-muted-foreground mt-1">
                  部门: {{ item.department_id }}
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
  </div>
</template>
