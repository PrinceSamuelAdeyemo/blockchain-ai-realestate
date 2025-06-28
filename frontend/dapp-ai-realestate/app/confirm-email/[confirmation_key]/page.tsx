"use client";

import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export default function ConfirmPage() {
  const params = useParams();
  const router = useRouter();

  // Because useParams() can return string | string[] | undefined,
  // we coerce it down to a single string (or bail out).
  const rawParam = params.confirmation_key;
  const confirmationKey =
    Array.isArray(rawParam) ? rawParam[0] : rawParam;

  const [status, setStatus] = useState<"idle" | "success" | "error">("idle");
  const [message, setMessage] = useState<string>("");

  useEffect(() => {
    // Only proceed if we have a single string
    if (!confirmationKey) {
      console.warn("No confirmation key found in URL");
      return;
    }

    const confirmEmail = async () => {
      try {
        // Now TypeScript knows confirmationKey is string
        const decodedKey = decodeURIComponent(confirmationKey);
        console.log("Decoded confirmation key:", decodedKey);

        const res = await fetch(
          `${process.env.NEXT_PUBLIC_API_BASE_URL}/core/api/v1/users/confirm-email/`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ key: decodedKey }),
          }
        );
        const data = await res.json();

        if (res.ok) {
          setStatus("success");
          setMessage(data.message || "Email confirmed successfully.");
          setTimeout(() => router.push("/login"), 3000);
          router.push("/login");
        
        } else {
          setStatus("error");
          setMessage(data.error || "Invalid or expired confirmation key.");
        }
      } catch (err) {
        console.error(err);
        setStatus("error");
        setMessage("An error occurred. Please try again.");
      }
    };

    confirmEmail();
  }, [confirmationKey, router]);

  return (
    <main style={{ maxWidth: 400, margin: "4rem auto", textAlign: "center" }}>
      {status === "idle" && <p>Confirming your email…</p>}
      {status === "success" && (
        <p style={{ color: "green", fontWeight: "bold" }}>{message}</p>
      )}
      {status === "error" && (
        <p style={{ color: "red", fontWeight: "bold" }}>{message}</p>
      )}
    </main>
  );
}
