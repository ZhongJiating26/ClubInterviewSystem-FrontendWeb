import path from 'node:path'
import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'
import vue from '@vitejs/plugin-vue'
import tsconfigPaths from 'vite-tsconfig-paths'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(), tailwindcss(), tsconfigPaths()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    host: '0.0.0.0', // 允许其他电脑访问
    proxy: {
      // API 代理（排除 /admin/ 和 /student/，因为它们与前端路由冲突）
      '^/auth/': { target: 'http://localhost:8000', changeOrigin: true },
      '^/schools/': { target: 'http://localhost:8000', changeOrigin: true },
      '^/clubs/': { target: 'http://localhost:8000', changeOrigin: true },
      '^/departments/': { target: 'http://localhost:8000', changeOrigin: true },
      '^/positions/': { target: 'http://localhost:8000', changeOrigin: true },
      '^/recruitment/': { target: 'http://localhost:8000', changeOrigin: true },
      '^/interview/': { target: 'http://localhost:8000', changeOrigin: true },
      '^/interviews/': { target: 'http://localhost:8000', changeOrigin: true },
      // 注意：/admin/ 和 /student/ 不在这里代理，因为它们会与前端路由冲突
    },
  },
})
