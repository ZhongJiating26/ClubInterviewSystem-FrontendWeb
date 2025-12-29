<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { initAccount } from '@/api/modules/auth'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import SchoolSelect from '@/components/SchoolSelect.vue'

const router = useRouter()

// 表单数据
const password = ref('')
const confirmPassword = ref('')
const name = ref('')
const idCardNo = ref('')
const schoolId = ref<number | null>(null)
const schoolCode = ref<string | null>(null)
const major = ref('')
const studentNo = ref('')
const email = ref('')

// 状态
const loading = ref(false)
const error = ref('')

// 提交初始化
const handleInit = async () => {
  error.value = ''

  // 验证必填
  if (!password.value || !name.value || !idCardNo.value ||
      !schoolCode.value || !major.value || !studentNo.value) {
    error.value = '请填写所有必填项'
    return
  }

  // 身份证号格式验证（15-18位）
  if (idCardNo.value.length < 15) {
    error.value = '身份证号至少15位'
    return
  }

  if (password.value.length < 6) {
    error.value = '密码至少6位'
    return
  }

  if (password.value !== confirmPassword.value) {
    error.value = '两次密码不一致'
    return
  }

  loading.value = true

  try {
    const data = {
      password: password.value,
      name: name.value,
      id_card_no: idCardNo.value,
      school_code: schoolCode.value,
      major: major.value,
      student_no: studentNo.value
    }
    await initAccount(data)
    // 初始化成功，跳转到学生端首页
    router.push('/student/apply')
  } catch (err: any) {
    error.value = err.message || '初始化失败'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen w-full bg-white flex items-center justify-center p-6">
    <div class="w-full max-w-sm flex flex-col gap-6">
      <!-- 标题 -->
      <div class="flex flex-col items-center gap-2 text-center">
        <h1 class="text-2xl font-bold">完善个人信息</h1>
        <p class="text-muted-foreground text-sm">请填写以下信息完成注册</p>
      </div>

      <!-- 表单 -->
      <form @submit.prevent="handleInit" class="flex flex-col gap-4">
        <!-- 错误提示 -->
        <div v-if="error" class="p-3 text-sm text-red-600 bg-red-50 rounded-md">
          {{ error }}
        </div>

        <!-- 姓名 -->
        <div class="grid gap-2">
          <Label for="name">姓名</Label>
          <Input
            id="name"
            v-model="name"
            type="text"
            placeholder="请输入您的真实姓名"
            required
          />
        </div>

        <!-- 身份证号 -->
        <div class="grid gap-2">
          <Label for="id_card_no">身份证号</Label>
          <Input
            id="id_card_no"
            v-model="idCardNo"
            type="text"
            placeholder="请输入身份证号"
            required
          />
        </div>

        <!-- 学校选择 -->
        <SchoolSelect
          v-model="schoolId"
          v-model:modelCode="schoolCode"
          label="学校"
          placeholder="输入学校名称搜索"
          :required="true"
        />

        <!-- 专业 -->
        <div class="grid gap-2">
          <Label for="major">专业</Label>
          <Input
            id="major"
            v-model="major"
            type="text"
            placeholder="请输入专业"
            required
          />
        </div>

        <!-- 学号 -->
        <div class="grid gap-2">
          <Label for="student_no">学号</Label>
          <Input
            id="student_no"
            v-model="studentNo"
            type="text"
            placeholder="请输入学号"
            required
          />
        </div>

        <!-- 邮箱（可选） -->
        <div class="grid gap-2">
          <Label for="email">邮箱</Label>
          <Input
            id="email"
            v-model="email"
            type="email"
            placeholder="选填"
          />
        </div>

        <!-- 密码 -->
        <div class="grid gap-2">
          <Label for="password">密码</Label>
          <Input
            id="password"
            v-model="password"
            type="password"
            placeholder="至少6位"
            required
          />
        </div>

        <!-- 确认密码 -->
        <div class="grid gap-2">
          <Label for="confirm_password">确认密码</Label>
          <Input
            id="confirm_password"
            v-model="confirmPassword"
            type="password"
            placeholder="请再次输入密码"
            required
          />
        </div>

        <Button type="submit" class="w-full" :disabled="loading">
          <span v-if="loading">提交中...</span>
          <span v-else>提交</span>
        </Button>
      </form>
    </div>
  </div>
</template>
