"use client";
import { useState } from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

export default function ResetPasswordConfirmPage() {
  const [uid, setUid] = useState("");
  const [token, setToken] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [status, setStatus] = useState<string | null>(null);
  const apiUrl = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setStatus("Submitting...");
    try {
      const res = await fetch(`${apiUrl}/core/api/reset-password/confirm`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ uid, token, new_password: newPassword }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data?.error || "Failed");
      setStatus("Password reset successful. You can now login.");
      setUid(""); setToken(""); setNewPassword("");
    } catch (err: any) {
      setStatus("Error: " + (err.message || err));
    }
  }

  const isSubmitting = status === "Submitting...";

  return (
    <div className="min-h-screen flex flex-col bg-slate-50">
      <Navbar />

      <main className="flex-grow flex items-center justify-center px-4 py-12">
        <div className="w-full max-w-lg">
          <div className="bg-white/95 backdrop-blur-sm border border-gray-200 rounded-2xl shadow-lg p-8">
            <div className="text-center mb-6">
              <h1 className="text-2xl font-semibold text-gray-900">Set a new password</h1>
              <p className="mt-2 text-sm text-gray-500">
                Paste the UID and token from the email and choose a strong new password.
              </p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="text-sm font-medium text-gray-700">UID</label>
                <input
                  value={uid}
                  onChange={e => setUid(e.target.value)}
                  placeholder="UID (from email)"
                  required
                  className="mt-1 block w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                />
              </div>

              <div>
                <label className="text-sm font-medium text-gray-700">Token</label>
                <input
                  value={token}
                  onChange={e => setToken(e.target.value)}
                  placeholder="Token (from email)"
                  required
                  className="mt-1 block w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                />
              </div>

              <div>
                <label className="text-sm font-medium text-gray-700">New password</label>
                <input
                  value={newPassword}
                  onChange={e => setNewPassword(e.target.value)}
                  placeholder="New password"
                  type="password"
                  required
                  className="mt-1 block w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                />
                <p className="mt-2 text-xs text-gray-400">Use a strong password (min 8 characters, mix of letters & numbers).</p>
              </div>

              <button
                type="submit"
                className={`w-full inline-flex items-center justify-center gap-2 rounded-lg px-4 py-2 text-sm font-medium text-white transition ${
                  isSubmitting
                    ? "bg-emerald-400 cursor-wait"
                    : "bg-gradient-to-r from-emerald-600 to-emerald-500 hover:from-emerald-700 hover:to-emerald-600"
                }`}
                aria-busy={isSubmitting}
                disabled={isSubmitting}
              >
                {isSubmitting ? (
                  <>
                    <svg
                      className="animate-spin -ml-1 mr-2 h-4 w-4 text-white"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                    >
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
                    </svg>
                    Setting...
                  </>
                ) : (
                  "Set new password"
                )}
              </button>
            </form>

            {status && (
              <div
                role="status"
                className={`mt-5 px-4 py-3 rounded-md text-sm ${
                  status.startsWith("Error:")
                    ? "bg-red-50 text-red-800 border border-red-100"
                    : "bg-green-50 text-green-800 border border-green-100"
                }`}
              >
                {status}
              </div>
            )}

            <div className="mt-6 text-center">
              <a href="/signin" className="text-sm text-emerald-600 hover:underline">Back to sign in</a>
            </div>
          </div>

          <div className="mt-6 text-center text-xs text-gray-400">
            <p>Don't share your password. If you didn't request this, ignore the email and secure your account.</p>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
