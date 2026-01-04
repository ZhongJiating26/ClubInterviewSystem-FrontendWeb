<script setup lang="ts">
import { computed } from 'vue'
import { RouterView, useRoute, useRouter } from 'vue-router'
import { User, Bell, Ticket, Home, Calendar, UserCircle, School } from 'lucide-vue-next'
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

// 判断是否是详情页（隐藏顶部和底部导航）
const isDetailPage = computed(() => route.path.startsWith('/student/club') || route.path.startsWith('/student/apply'))
</script>

<template>
  <div class="min-h-screen" style="background-color: #F8F8F8">
    <!-- 顶部栏 - 详情页不显示 -->
    <header v-if="!isDetailPage" class="bg-white shadow-sm sticky top-0 z-10">
      <div class="px-4 py-3 flex items-center gap-2 min-h-14">
        <School class="w-4 h-4 text-gray-500" />
        <span class="text-base font-medium text-gray-600 leading-none">{{ userStore.userInfo?.school_name || '学校' }}</span>
      </div>
    </header>

    <!-- 主内容区 - 详情页不需要底部留白 -->
    <main :class="isDetailPage ? 'p-0' : 'p-4 pb-20'">
      <RouterView />
    </main>

    <!-- 底部导航栏 - 详情页不显示 -->
    <div v-if="!isDetailPage" class="fixed bottom-0 left-0 right-0 bg-white border-t z-20">
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
