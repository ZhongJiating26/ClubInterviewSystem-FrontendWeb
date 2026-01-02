<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
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
      <AlertTitle>社团资料不完整</AlertTitle>
      <AlertDescription>
        您的社团资料还缺少以下信息：{{ getMissingFieldText(profileCheck.missing_fields) }}。
        请及时完善社团资料，以便正常运营。
      </AlertDescription>
    </Alert>

    <p>管理员仪表盘</p>
  </div>
</template>
