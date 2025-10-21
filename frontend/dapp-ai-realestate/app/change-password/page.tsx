"use client";
import { useState } from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

export default function ChangePasswordPage() {
  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [status, setStatus] = useState<string | null>(null);

  const apiUrl = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";
  const userDetails = typeof window !== "undefined" ? localStorage.getItem("userDetails") : null;
  const token = userDetails ? JSON.parse(userDetails).access : null;

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setStatus("Saving...");
    try {
      const res = await fetch(`${apiUrl}/core/api/change-password`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify({ old_password: oldPassword, new_password: newPassword }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data?.error || "Failed");
      setStatus("Password changed successfully");
      setOldPassword(""); setNewPassword("");
    } catch (err: any) {
      setStatus("Error: " + (err.message || err));
    }
  }

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Navbar />

      <main className="flex-grow flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="w-full max-w-md">
          <div className="bg-white shadow-lg rounded-2xl p-6 sm:p-8 border border-gray-100">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h1 className="text-2xl font-semibold text-gray-900">Change Password</h1>
                <p className="mt-1 text-sm text-gray-500">Update your account password. Use a strong, unique password.</p>
              </div>
              <div className="hidden sm:flex items-center justify-center w-12 h-12 bg-blue-50 rounded-full">
                <svg className="w-6 h-6 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 11c1.657 0 3-1.567 3-3.5S13.657 4 12 4 9 5.567 9 7.5 10.343 11 12 11zM4 20v-2a4 4 0 014-4h8a4 4 0 014 4v2" />
                </svg>
              </div>
            </div>

            <form onSubmit={handleSubmit} className="space-y-5">
              <div>
                <label htmlFor="oldPassword" className="block text-sm font-medium text-gray-700 mb-1">Current password</label>
                <input
                  id="oldPassword"
                  value={oldPassword}
                  onChange={e => setOldPassword(e.target.value)}
                  placeholder="Enter current password"
                  type="password"
                  className="block w-full rounded-xl border-gray-200 shadow-sm focus:ring-2 focus:ring-blue-400 focus:border-transparent px-4 py-2"
                  required
                />
              </div>

              <div>
                <label htmlFor="newPassword" className="block text-sm font-medium text-gray-700 mb-1">New password</label>
                <input
                  id="newPassword"
                  value={newPassword}
                  onChange={e => setNewPassword(e.target.value)}
                  placeholder="Enter new password"
                  type="password"
                  className="block w-full rounded-xl border-gray-200 shadow-sm focus:ring-2 focus:ring-blue-400 focus:border-transparent px-4 py-2"
                  required
                />
                <p className="mt-2 text-xs text-gray-400">Use at least 8 characters. Mix letters, numbers and symbols for better security.</p>
              </div>

              <div className="pt-2">
                <button
                  type="submit"
                  className="w-full inline-flex justify-center items-center rounded-xl bg-blue-600 hover:bg-blue-700 active:bg-blue-800 text-white font-medium px-4 py-2 shadow-sm transition"
                >
                  Save new password
                </button>
              </div>

              {status && (
                <div className={`mt-2 text-sm ${status.startsWith("Error") ? "text-red-600" : "text-green-600"}`}>
                  {status}
                </div>
              )}
            </form>
          </div>

          <div className="mt-6 text-center text-sm text-gray-500">
            <p>
              Trouble signing in? <a href="/reset-password" className="text-blue-600 hover:underline">Reset your password</a>
            </p>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
