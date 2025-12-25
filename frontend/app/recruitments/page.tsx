"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { format } from "date-fns";

interface Recruitment {
  id: number;
  club_id: number;
  title: string;
  description: string | null;
  start_time: string;
  end_time: string;
  status: number;
  application_count: number;
}

export default function RecruitmentsPage() {
  const [recruitments, setRecruitments] = useState<Recruitment[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchRecruitments() {
      try {
        const response = await api.get<Recruitment[]>("/recruitments");
        setRecruitments(response.data);
      } catch (error) {
        console.error("获取招新列表失败:", error);
      } finally {
        setLoading(false);
      }
    }
    fetchRecruitments();
  }, []);

  const getStatusText = (status: number) => {
    const statusMap: Record<number, string> = {
      0: "待发布",
      1: "进行中",
      2: "已结束",
      3: "已取消",
    };
    return statusMap[status] || "未知";
  };

  if (loading) {
    return <div className="p-8">加载中...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold">招新活动</h1>
        </div>
        <div className="space-y-4">
          {recruitments.map((recruitment) => (
            <Link key={recruitment.id} href={`/recruitments/${recruitment.id}`}>
              <div className="bg-white p-6 rounded-lg shadow hover:shadow-md transition-shadow cursor-pointer">
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <h2 className="text-lg font-semibold mb-2">
                      {recruitment.title}
                    </h2>
                    <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                      {recruitment.description || "暂无描述"}
                    </p>
                    <div className="flex gap-4 text-sm text-gray-500">
                      <span>
                        开始: {format(new Date(recruitment.start_time), "yyyy-MM-dd")}
                      </span>
                      <span>
                        结束: {format(new Date(recruitment.end_time), "yyyy-MM-dd")}
                      </span>
                      <span>报名: {recruitment.application_count} 人</span>
                    </div>
                  </div>
                  <div className="ml-4">
                    <span
                      className={`px-3 py-1 rounded-full text-sm ${
                        recruitment.status === 1
                          ? "bg-green-100 text-green-800"
                          : recruitment.status === 2
                          ? "bg-gray-100 text-gray-800"
                          : "bg-yellow-100 text-yellow-800"
                      }`}
                    >
                      {getStatusText(recruitment.status)}
                    </span>
                  </div>
                </div>
              </div>
            </Link>
          ))}
        </div>
        {recruitments.length === 0 && (
          <div className="text-center py-12 text-gray-500">
            暂无招新活动
          </div>
        )}
      </div>
    </div>
  );
}

