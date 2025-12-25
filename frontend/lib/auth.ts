import { api } from "./api";
import { cookies } from "next/headers";

export interface User {
  id: number;
  phone: string;
  name: string | null;
  status: number;
  is_initialized: boolean;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export async function login(phone: string, password: string): Promise<LoginResponse> {
  const response = await api.post<LoginResponse>("/auth/login", {
    phone,
    password,
  });
  
  if (typeof window !== "undefined") {
    localStorage.setItem("access_token", response.data.access_token);
  }
  
  return response.data;
}

export async function register(data: {
  phone: string;
  password: string;
  name?: string;
  school_id?: number;
}) {
  const response = await api.post("/auth/register", data);
  return response.data;
}

export async function getCurrentUser(): Promise<User | null> {
  try {
    if (typeof window !== "undefined") {
      const token = localStorage.getItem("access_token");
      if (!token) return null;
    }
    
    const response = await api.get<User>("/auth/me");
    return response.data;
  } catch (error) {
    return null;
  }
}

export function logout() {
  if (typeof window !== "undefined") {
    localStorage.removeItem("access_token");
    window.location.href = "/login";
  }
}

