<script setup lang="ts">
import { RouterView } from 'vue-router'
import {
  LayoutDashboard,
  Users,
  Calendar,
  BarChart,
  Ticket,
  Settings2,
  LifeBuoy,
  Command,
  Plus,
  History,
  ClipboardCheck,
  Filter,
  Building,
} from 'lucide-vue-next'
import { useUserStore } from '@/stores/user'
import AppSidebar from '@/components/AppSidebar.vue'
import NavUserCustom from '@/components/NavUserCustom.vue'
import NavGroup from '@/components/NavGroup.vue'
import {
  SidebarInset,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarProvider,
} from '@/components/ui/sidebar'

const userStore = useUserStore()

const data = {
  user: {
    name: userStore.userInfo?.name || '用户',
    email: userStore.userInfo?.phone || '',
    avatar: '',
  },
  navMain: [
    {
      title: '数据看板',
      url: '/admin/dashboard',
      icon: LayoutDashboard,
    },
  ],
  navApplications: [
    {
      title: '发布报名',
      url: '/admin/applications/create',
      icon: Plus,
    },
    {
      title: '历史报名记录',
      url: '/admin/applications/history',
      icon: History,
    },
    {
      title: '报名审核',
      url: '/admin/applications/review',
      icon: ClipboardCheck,
    },
  ],
  navInterviews: [
    {
      title: '发布面试',
      url: '/admin/interviews/create',
      icon: Plus,
    },
    {
      title: '面试记录',
      url: '/admin/interviews/records',
      icon: History,
    },
    {
      title: '面试筛选',
      url: '/admin/interviews/filter',
      icon: Filter,
    },
  ],
  navClubs: [
    {
      title: '社团资料',
      url: '/admin/clubs/profile',
      icon: Building,
    },
    {
      title: '社团人员管理',
      url: '/admin/clubs/members',
      icon: Users,
    },
  ],
  navSystem: [
    {
      title: '系统设置',
      url: '/admin/settings',
      icon: Settings2,
    },
  ],
}
</script>

<template>
  <SidebarProvider>
    <AppSidebar variant="inset">
      <template #header>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton size="lg" as-child>
              <a href="#">
                <div class="flex aspect-square size-8 items-center justify-center rounded-lg bg-primary text-primary-foreground">
                  <Command class="size-4" />
                </div>
                <div class="grid flex-1 text-left text-sm leading-tight">
                  <span class="truncate font-medium">社团面试系统</span>
                  <span class="truncate text-xs">管理后台</span>
                </div>
              </a>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </template>
      <template #content>
        <NavGroup :items="data.navMain" />
        <NavGroup title="报名管理" :items="data.navApplications" />
        <NavGroup title="面试管理" :items="data.navInterviews" />
        <NavGroup title="社团管理" :items="data.navClubs" />
        <NavGroup title="系统" :items="data.navSystem" class="mt-auto" />
      </template>
      <template #footer>
        <NavUserCustom :user="data.user" />
      </template>
    </AppSidebar>

    <SidebarInset>
      <!-- 主内容区 -->
      <main class="flex-1 p-6 overflow-auto">
        <RouterView />
      </main>
    </SidebarInset>
  </SidebarProvider>
</template>
