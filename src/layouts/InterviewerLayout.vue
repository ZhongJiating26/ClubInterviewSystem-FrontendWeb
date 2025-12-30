<script setup lang="ts">
import { RouterView, RouterLink, useRoute, useRouter } from 'vue-router'
import { ClipboardList, LogOut } from 'lucide-vue-next'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const menuItems = [
  { path: '/interviewer/tasks', name: '面试任务', icon: ClipboardList }
]

const handleLogout = () => {
  userStore.logout()
}
</script>

<template>
  <div class="min-h-screen bg-gray-100 flex">
    <!-- 侧边栏 -->
    <aside class="w-64 bg-white border-r flex flex-col">
      <div class="p-6 border-b">
        <h1 class="text-xl font-bold">社团面试系统</h1>
        <p class="text-sm text-gray-500 mt-1">面试官端</p>
      </div>

      <nav class="flex-1 p-4 space-y-1">
        <RouterLink
          v-for="item in menuItems"
          :key="item.path"
          :to="item.path"
          class="flex items-center gap-3 px-4 py-3 rounded-lg text-gray-700 hover:bg-gray-100 transition-colors"
          :class="{ 'bg-primary text-white hover:bg-primary/90': route.path === item.path }"
        >
          <component :is="item.icon" class="w-5 h-5" />
          {{ item.name }}
        </RouterLink>
      </nav>

      <div class="p-4 border-t">
        <button
          @click="handleLogout"
          class="flex items-center gap-3 w-full px-4 py-3 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
        >
          <LogOut class="w-5 h-5" />
          退出登录
        </button>
      </div>
    </aside>

    <!-- 主内容区 -->
    <main class="flex-1 p-8 overflow-auto">
      <RouterView />
    </main>
  </div>
</template>
