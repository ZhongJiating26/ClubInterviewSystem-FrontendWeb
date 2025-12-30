<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { Button } from '@/components/ui/button'
import { Home, ArrowLeft } from 'lucide-vue-next'
</script>

<template>
  <div class="min-h-screen w-full bg-white flex items-center justify-center p-6">
    <div class="w-full max-w-sm flex flex-col gap-6">
      <!-- 标题 -->
      <div class="flex flex-col items-center gap-2 text-center">
        <h1 class="text-[8rem] md:text-[20rem] font-bold text-gray-300 leading-none">404</h1>
        <p class="text-2xl font-semibold">页面未找到</p>
        <p class="text-muted-foreground text-sm">您访问的页面不存在或已被移除</p>
      </div>

      <!-- 操作按钮 -->
      <div class="flex flex-col gap-3">
        <RouterLink to="/">
          <Button variant="outline" class="w-full">
            <Home class="w-4 h-4 mr-2" />
            返回首页
          </Button>
        </RouterLink>
      </div>
    </div>
  </div>
</template>
