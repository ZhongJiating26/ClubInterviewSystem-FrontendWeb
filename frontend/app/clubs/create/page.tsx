"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { extractErrorMessage } from "@/lib/utils";
import Link from "next/link";

export default function CreateClubPage() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    school_id: "",
    logo_url: "",
    cover_url: "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const payload: any = {
        name: formData.name,
      };
      
      if (formData.description && formData.description.trim()) {
        payload.description = formData.description.trim();
      }
      
      if (formData.school_id && formData.school_id.trim()) {
        const schoolId = parseInt(formData.school_id);
        if (!isNaN(schoolId)) {
          payload.school_id = schoolId;
        }
      }
      
      if (formData.logo_url && formData.logo_url.trim()) {
        payload.logo_url = formData.logo_url.trim();
      }
      
      if (formData.cover_url && formData.cover_url.trim()) {
        payload.cover_url = formData.cover_url.trim();
      }
      
      await api.post("/clubs", payload);
      router.push("/clubs");
    } catch (err: any) {
      setError(extractErrorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-6">
          <Link href="/clubs" className="text-blue-600 hover:underline">
            ← 返回社团列表
          </Link>
        </div>
        <div className="bg-white rounded-lg shadow-md p-6">
          <h1 className="text-2xl font-bold mb-6">创建社团</h1>
          
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
                社团名称 *
              </label>
              <input
                id="name"
                type="text"
                required
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary"
                placeholder="请输入社团名称"
              />
            </div>

            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
                社团描述
              </label>
              <textarea
                id="description"
                rows={4}
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary"
                placeholder="请输入社团描述"
              />
            </div>

            <div>
              <label htmlFor="school_id" className="block text-sm font-medium text-gray-700 mb-1">
                学校ID
              </label>
              <input
                id="school_id"
                type="number"
                value={formData.school_id}
                onChange={(e) => setFormData({ ...formData, school_id: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary"
                placeholder="请输入学校ID（可选）"
              />
            </div>

            <div>
              <label htmlFor="logo_url" className="block text-sm font-medium text-gray-700 mb-1">
                Logo URL
              </label>
              <input
                id="logo_url"
                type="url"
                value={formData.logo_url}
                onChange={(e) => setFormData({ ...formData, logo_url: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary"
                placeholder="请输入Logo图片URL（可选）"
              />
            </div>

            <div>
              <label htmlFor="cover_url" className="block text-sm font-medium text-gray-700 mb-1">
                封面图 URL
              </label>
              <input
                id="cover_url"
                type="url"
                value={formData.cover_url}
                onChange={(e) => setFormData({ ...formData, cover_url: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary"
                placeholder="请输入封面图URL（可选）"
              />
            </div>

            <div className="flex gap-4 pt-4">
              <Button
                type="submit"
                className="flex-1"
                disabled={loading}
              >
                {loading ? "创建中..." : "创建社团"}
              </Button>
              <Link href="/clubs">
                <Button type="button" variant="outline">
                  取消
                </Button>
              </Link>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

