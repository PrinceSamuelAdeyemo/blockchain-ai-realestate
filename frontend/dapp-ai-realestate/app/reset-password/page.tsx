// ...existing code...
"use client";
import { useState } from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

export default function ResetPasswordRequestPage() {
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState<string | null>(null);
  const apiUrl = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setStatus("Submitting...");
    try {
      const res = await fetch(`${apiUrl}/core/api/reset-password`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data?.error || "Failed");
      // In DEBUG backend returns uid/token; otherwise just message
      setStatus(data?.message || "If that email exists, instructions were sent.");
    } catch (err: any) {
      setStatus("Error: " + (err.message || err));
    }
  }

  const isSubmitting = status === "Submitting...";
  const statusType =
    status && status.startsWith("Error:")
      ? "error"
      : status && /sent|instructions|success|If that email exists/i.test(status)
      ? "success"
      : "info";

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Navbar />

      <main className="flex-grow flex items-center justify-center px-4 py-12">
        <div className="w-full max-w-md">
          <div className="bg-white/95 backdrop-blur-sm border border-gray-200 rounded-2xl shadow-lg p-8">
            <div className="mb-6 text-center">
              <h1 className="text-2xl font-semibold text-gray-900">
                Reset your password
              </h1>
              <p className="mt-2 text-sm text-gray-500">
                Enter the email associated with your account and we'll send instructions to reset your password.
              </p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              <label className="block">
                <span className="text-sm font-medium text-gray-700 mb-1 inline-block">Email</span>
                <input
                  value={email}
                  onChange={e => setEmail(e.target.value)}
                  placeholder="you@example.com"
                  type="email"
                  required
                  className="w-full rounded-md border border-gray-300 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </label>

              <button
                type="submit"
                className={`w-full inline-flex items-center justify-center gap-2 rounded-md px-4 py-2 text-sm font-medium text-white transition ${
                  isSubmitting
                    ? "bg-blue-400 cursor-wait"
                    : "bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-700 hover:to-blue-600"
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
                    Sending...
                  </>
                ) : (
                  "Send reset email"
                )}
              </button>
            </form>

            {status && (
              <div
                role="status"
                className={`mt-5 px-4 py-3 rounded-md text-sm ${
                  statusType === "error"
                    ? "bg-red-50 text-red-800 border border-red-100"
                    : statusType === "success"
                    ? "bg-green-50 text-green-800 border border-green-100"
                    : "bg-blue-50 text-blue-800 border border-blue-100"
                }`}
              >
                {status}
              </div>
            )}

            <div className="mt-6 text-center">
              <a href="/signin" className="text-sm text-blue-600 hover:underline">
                Back to sign in
              </a>
            </div>
          </div>

          <div className="mt-6 text-center text-xs text-gray-400">
            <p>We won't share your email. Check spam if you don't see the message.</p>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
// ...existing code...