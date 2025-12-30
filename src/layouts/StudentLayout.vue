<script setup lang="ts">
import { ref } from 'vue'
import { RouterView, RouterLink, useRoute, useRouter } from 'vue-router'
import { User, Bell, Ticket, LogOut } from 'lucide-vue-next'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const menuItems = [
  { path: '/apply', name: '社团报名', icon: User },
  { path: '/notifications', name: '通知中心', icon: Bell },
  { path: '/student/tickets', name: '我的工单', icon: Ticket }
]

const handleLogout = () => {
  userStore.logout()
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 顶部栏 -->
    <header class="bg-white shadow-sm sticky top-0 z-10">
      <div class="px-4 py-3 flex items-center justify-between">
        <h1 class="text-lg font-bold">社团面试系统</h1>
        <button @click="handleLogout" class="p-2 text-gray-600">
          <LogOut class="w-5 h-5" />
        </button>
      </div>
    </header>

    <!-- 主内容区 -->
    <main class="p-4 pb-20">
      <RouterView />
    </main>

    <!-- 底部导航栏 -->
    <nav class="fixed bottom-0 left-0 right-0 bg-white border-t flex justify-around py-2">
      <RouterLink
        v-for="item in menuItems"
        :key="item.path"
        :to="item.path"
        class="flex flex-col items-center py-2 px-4 text-xs"
        :class="{ 'text-primary': route.path === item.path, 'text-gray-500': route.path !== item.path }"
      >
        <component :is="item.icon" class="w-6 h-6 mb-1" />
        {{ item.name }}
      </RouterLink>
    </nav>
  </div>
</template>
