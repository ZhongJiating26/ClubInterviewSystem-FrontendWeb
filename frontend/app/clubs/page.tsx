"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import Link from "next/link";

interface Club {
  id: number;
  name: string;
  description: string | null;
  school_id: number;
  president_id: number;
  status: number;
  member_count: number;
}

export default function ClubsPage() {
  const [clubs, setClubs] = useState<Club[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchClubs() {
      try {
        const response = await api.get<Club[]>("/clubs");
        setClubs(response.data);
      } catch (error) {
        console.error("获取社团列表失败:", error);
      } finally {
        setLoading(false);
      }
    }
    fetchClubs();
  }, []);

  if (loading) {
    return <div className="p-8">加载中...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold">社团列表</h1>
          <Link href="/clubs/create">
            <Button>创建社团</Button>
          </Link>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {clubs.map((club) => (
            <Link key={club.id} href={`/clubs/${club.id}`}>
              <div className="bg-white p-6 rounded-lg shadow hover:shadow-md transition-shadow cursor-pointer">
                <h2 className="text-lg font-semibold mb-2">{club.name}</h2>
                <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                  {club.description || "暂无描述"}
                </p>
                <div className="flex justify-between text-sm text-gray-500">
                  <span>成员: {club.member_count}</span>
                  <span>状态: {club.status === 1 ? "正常" : "禁用"}</span>
                </div>
              </div>
            </Link>
          ))}
        </div>
        {clubs.length === 0 && (
          <div className="text-center py-12 text-gray-500">
            暂无社团，创建第一个社团吧！
          </div>
        )}
      </div>
    </div>
  );
}

