import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * 从 API 错误响应中提取错误消息
 * 处理 FastAPI 422 验证错误的格式
 */
export function extractErrorMessage(error: any): string {
  if (!error?.response?.data) {
    return error?.message || "操作失败，请重试";
  }

  const data = error.response.data;
  
  // 如果是字符串，直接返回
  if (typeof data.detail === "string") {
    return data.detail;
  }
  
  // 如果是数组（FastAPI 422 验证错误）
  if (Array.isArray(data.detail)) {
    const messages = data.detail.map((item: any) => {
      const field = item.loc?.join(".") || "字段";
      return `${field}: ${item.msg || "验证失败"}`;
    });
    return messages.join("; ");
  }
  
  // 如果是对象
  if (typeof data.detail === "object") {
    return data.detail.msg || data.detail.message || "操作失败，请重试";
  }
  
  return "操作失败，请重试";
}

