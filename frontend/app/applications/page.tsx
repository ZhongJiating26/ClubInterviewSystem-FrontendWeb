"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { format } from "date-fns";

interface Application {
  id: number;
  recruitment_id: number;
  recruitment_title?: string;
  user_id: number;
  motivation: string | null;
  experience: string | null;
  skills: string | null;
  status: number;
  reviewed_by: number | null;
  reviewed_at: string | null;
  review_comment: string | null;
  created_at: string;
}

export default function ApplicationsPage() {
  const [applications, setApplications] = useState<Application[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchApplications() {
      try {
        // 获取当前用户的申请列表
        const response = await api.get<Application[]>("/recruitments/applications/my");
        setApplications(response.data);
      } catch (error) {
        console.error("获取申请列表失败:", error);
        // 如果接口不存在，显示空列表
        setApplications([]);
      } finally {
        setLoading(false);
      }
    }
    fetchApplications();
  }, []);

  const getStatusText = (status: number) => {
    const statusMap: Record<number, { text: string; color: string }> = {
      0: { text: "待审核", color: "bg-yellow-100 text-yellow-800" },
      1: { text: "已通过", color: "bg-green-100 text-green-800" },
      2: { text: "已拒绝", color: "bg-red-100 text-red-800" },
      3: { text: "已取消", color: "bg-gray-100 text-gray-800" },
    };
    return statusMap[status] || { text: "未知", color: "bg-gray-100 text-gray-800" };
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div>加载中...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-6">
          <Link href="/dashboard" className="text-blue-600 hover:underline">
            ← 返回首页
          </Link>
        </div>
        <h1 className="text-2xl font-bold mb-6">我的申请</h1>

        {applications.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-12 text-center">
            <p className="text-gray-500 mb-4">暂无申请记录</p>
            <Link href="/recruitments">
              <Button>查看招新活动</Button>
            </Link>
          </div>
        ) : (
          <div className="space-y-4">
            {applications.map((application) => {
              const status = getStatusText(application.status);
              return (
                <div
                  key={application.id}
                  className="bg-white rounded-lg shadow hover:shadow-md transition-shadow p-6"
                >
                  <div className="flex justify-between items-start mb-4">
                    <div className="flex-1">
                      <h2 className="text-lg font-semibold mb-2">
                        {application.recruitment_title || `招新活动 #${application.recruitment_id}`}
                      </h2>
                      <div className="text-sm text-gray-600 space-y-1">
                        <p>
                          <span className="font-medium">申请时间：</span>
                          {format(new Date(application.created_at), "yyyy-MM-dd HH:mm")}
                        </p>
                        {application.motivation && (
                          <p>
                            <span className="font-medium">申请动机：</span>
                            {application.motivation}
                          </p>
                        )}
                        {application.review_comment && (
                          <p>
                            <span className="font-medium">审核意见：</span>
                            {application.review_comment}
                          </p>
                        )}
                        {application.reviewed_at && (
                          <p>
                            <span className="font-medium">审核时间：</span>
                            {format(new Date(application.reviewed_at), "yyyy-MM-dd HH:mm")}
                          </p>
                        )}
                      </div>
                    </div>
                    <div className="ml-4">
                      <span
                        className={`px-3 py-1 rounded-full text-sm ${status.color}`}
                      >
                        {status.text}
                      </span>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <Link href={`/recruitments/${application.recruitment_id}`}>
                      <Button variant="outline" size="sm">
                        查看详情
                      </Button>
                    </Link>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}

