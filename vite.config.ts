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
      // 只代理 API 路径，排除 /admin/* (由前端 SPA 处理)
      '^/auth': { target: 'http://localhost:8000', changeOrigin: true },
      '^/applications': { target: 'http://localhost:8000', changeOrigin: true },
      '^/interviews': { target: 'http://localhost:8000', changeOrigin: true },
      '^/notifications': { target: 'http://localhost:8000', changeOrigin: true },
      '^/tickets': { target: 'http://localhost:8000', changeOrigin: true },
      '^/statistics': { target: 'http://localhost:8000', changeOrigin: true },
      '^/score': { target: 'http://localhost:8000', changeOrigin: true },
      '^/schools': { target: 'http://localhost:8000', changeOrigin: true },
      '^/clubs': { target: 'http://localhost:8000', changeOrigin: true },
      '^/recruitment': { target: 'http://localhost:8000', changeOrigin: true },
      '^/student': { target: 'http://localhost:8000', changeOrigin: true },
    },
    appType: 'spa', // SPA 模式，自动处理 SPA 路由
  },
})
