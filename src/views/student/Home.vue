<script setup lang="ts">
import { computed } from 'vue'
import { useUserStore } from '@/stores/user'
import { School, MapPin } from 'lucide-vue-next'

const userStore = useUserStore()

const schoolName = computed(() => {
  return userStore.userInfo?.school_name || '未选择学校'
})
</script>

<template>
  <div class="pb-4">
    <!-- 顶部学校信息 -->
    <div class="flex items-center gap-2 mb-4">
      <School class="w-4 h-4 text-gray-500" />
      <span class="text-sm text-gray-600">{{ schoolName }}</span>
    </div>

    <!-- 占位内容 -->
    <div class="text-center text-gray-400 py-12">
      页面开发中...
    </div>
  </div>
</template>
