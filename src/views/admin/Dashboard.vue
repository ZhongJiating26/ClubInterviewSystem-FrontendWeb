<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { checkClubProfile } from '@/api/modules/clubs'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { AlertCircle } from 'lucide-vue-next'

interface ProfileCheck {
  club_id: number
  is_complete: boolean
  missing_fields: string[]
}

const userStore = useUserStore()
const profileCheck = ref<ProfileCheck | null>(null)
const checked = ref(false)
const noClub = ref(false)

// 获取社团资料检查状态
const fetchProfileCheck = async () => {
  // 如果已经检查过且资料完整，不再重复请求
  if (checked.value && profileCheck.value?.is_complete) {
    return
  }

  const clubAdminRole = userStore.userInfo?.roles.find(r => r.code === 'CLUB_ADMIN')
  const clubId = clubAdminRole?.club_id

  if (!clubId) {
    noClub.value = true
    return
  }

  noClub.value = false

  try {
    const res = await checkClubProfile(clubId)
    profileCheck.value = res
    checked.value = true
  } catch (error) {
    console.error('获取社团资料检查状态失败:', error)
  }
}

// 缺失字段中文映射
const missingFieldLabels: Record<string, string> = {
  school_code: '学校代码',
  name: '社团名称',
  category: '社团分类',
  description: '社团简介',
  cert_file_url: '证书文件'
}

const getMissingFieldText = (fields: string[]) => {
  return fields.map(f => missingFieldLabels[f] || f).join('、')
}

onMounted(() => {
  fetchProfileCheck()
})
</script>

<template>
  <div>
    <h1 class="text-2xl font-bold mb-4">仪表盘</h1>

    <!-- 还未创建社团提示 -->
    <Alert v-if="noClub" variant="warning" class="mb-6">
      <AlertCircle class="h-4 w-4" />
      <AlertTitle>还未创建社团</AlertTitle>
      <AlertDescription>
        您还没有创建社团，请先创建社团后再进行管理。
      </AlertDescription>
    </Alert>

    <!-- 社团资料不完整提示 -->
    <Alert v-else-if="profileCheck && !profileCheck.is_complete" variant="warning" class="mb-6">
      <AlertCircle class="h-4 w-4" />
      <div class="grid grid-cols-[1fr_auto] gap-2 items-center">
        <div>
          <AlertTitle>社团资料不完整</AlertTitle>
          <AlertDescription>
            您的社团资料还缺少以下信息：{{ getMissingFieldText(profileCheck.missing_fields) }}。
          </AlertDescription>
        </div>
        <RouterLink to="/admin/clubs/profile" class="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 border border-black bg-gray-200 hover:bg-gray-300 text-black h-9 px-4 py-2">
          立即完善
        </RouterLink>
      </div>
    </Alert>

    <p>管理员仪表盘</p>
  </div>
</template>
