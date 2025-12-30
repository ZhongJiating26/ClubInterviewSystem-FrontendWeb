<script setup lang="ts">
import { ref } from 'vue'
import { RouterView, RouterLink, useRoute, useRouter } from 'vue-router'
import { User, Bell, Ticket, LogOut, Home, Calendar, UserCircle } from 'lucide-vue-next'
import { useUserStore } from '@/stores/user'
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const menuItems = [
  { path: '/student/home', name: '首页', icon: Home },
  { path: '/student/interviews', name: '面试', icon: Calendar },
  { path: '/student/profile', name: '我的', icon: UserCircle }
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
    <div class="fixed bottom-0 left-0 right-0 bg-white border-t z-20">
      <Tabs :model-value="route.path" class="w-full">
        <TabsList class="grid grid-cols-3 gap-1 h-auto p-2 bg-transparent w-full">
          <TabsTrigger
            v-for="item in menuItems"
            :key="item.path"
            :value="item.path"
            class="flex flex-col items-center gap-1 py-1 rounded-xl transition-all data-[state=active]:bg-primary/10 data-[state=active]:text-primary"
            :class="{ 'text-primary': route.path.startsWith(item.path), 'text-gray-500': !route.path.startsWith(item.path) }"
            @click="router.push(item.path)"
          >
            <component :is="item.icon" class="w-5 h-5" />
            <span class="text-xs">{{ item.name }}</span>
          </TabsTrigger>
        </TabsList>
      </Tabs>
    </div>
  </div>
</template>
