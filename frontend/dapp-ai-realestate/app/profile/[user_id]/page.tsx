"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { apiUrl } from "@/utils/env";

interface UserProfile {
  id: number;
  username: string;
  email: string;
  first_name?: string;
  last_name?: string;
  wallet_address?: string;
  kyc_status?: string;
  investments?: Array<{
    property_title: string;
    amount: number;
    date: string;
  }>;
}

export default function ProfilePage() {
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const { user_id } = useParams<{ user_id: string }>();

  useEffect(() => {
    // You may want to use a token from localStorage/cookies for auth
    async function fetchProfile() {
      setLoading(true);
      try {
        const res = await fetch(`${apiUrl}/core/api/v1/users/${user_id}`//, {
          //credentials: "include", // if using session auth/cookies
          //headers: {
            // "Authorization": `Bearer ${token}`, // if using JWT
//},
        );
        if (!res.ok) throw new Error("Failed to fetch profile");
        const data = await res.json();
        setProfile(data);
      } catch (err) {
        setProfile(null);
      }
      setLoading(false);
    }
    fetchProfile();
  }, []);

  return (
    <div>
      <Navbar />
      <div className="max-w-2xl mx-auto mt-10 p-6 min-h-[85vh] bg-white rounded-lg shadow">
        <h1 className="text-2xl font-bold mb-4">My Profile</h1>
        {loading ? (
          <p>Loading...</p>
        ) : profile ? (
          <div>
            <div className="flex items-center gap-4 mb-6">
              <img
                src="/icons/profile_1107841.png"
                alt="Profile"
                width={64}
                height={64}
                className="rounded-full border"
              />
              <div>
                <div className="text-lg font-semibold">{profile.username}</div>
                <div className="text-gray-500">{profile.email}</div>
              </div>
            </div>
            <div className="mb-4">
              <strong>Full Name:</strong>{" "}
              {profile.first_name || ""} {profile.last_name || ""}
            </div>
            <div className="mb-4">
              <strong>Wallet Address:</strong>{" "}
              <span className="font-mono">{profile.wallet_address || "Not linked"}</span>
            </div>
            <div className="mb-4">
              <strong>KYC Status:</strong>{" "}
              <span
                className={
                  profile.kyc_status === "verified"
                    ? "text-green-600"
                    : "text-yellow-600"
                }
              >
                {profile.kyc_status || "Pending"}
              </span>
            </div>
            <div className="mb-4">
              <strong>My Investments:</strong>
              {profile.investments && profile.investments.length > 0 ? (
                <ul className="list-disc ml-6">
                  {profile.investments.map((inv, idx) => (
                    <li key={idx}>
                      <span className="font-semibold">{inv.property_title}</span>
                      {": "}
                      {inv.amount} ETH on {new Date(inv.date).toLocaleDateString()}
                    </li>
                  ))}
                </ul>
              ) : (
                <div className="text-gray-500">No investments yet.</div>
              )}
            </div>
          </div>
        ) : (
          <div className="text-red-600">Could not load profile.</div>
        )}
      </div>
      <Footer />
    </div>
  );
}