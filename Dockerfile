# 多阶段构建 - 构建阶段
FROM node:20-alpine AS builder

# 设置工作目录
WORKDIR /app

# 复制 package.json 和 package-lock.json
COPY package*.json ./

# 安装所有依赖（包括 devDependencies，因为需要构建）
RUN npm ci

# 复制所有源代码
COPY . .

# 构建项目
RUN npm run build

# 生产阶段 - 使用 Node.js serve 静态文件
FROM node:20-alpine

# 安装 serve 包用于服务静态文件
RUN npm install -g serve

# 设置工作目录
WORKDIR /app

# 从构建阶段复制构建产物
COPY --from=builder /app/dist ./dist

# 暴露 3000 端口
EXPOSE 3000

# 启动 serve 服务
CMD ["serve", "-s", "dist", "-l", "3000"]
