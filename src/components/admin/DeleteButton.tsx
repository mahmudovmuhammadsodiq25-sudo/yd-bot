"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

export default function DeleteButton({ url, confirmText }: { url: string; confirmText: string }) {
  const router = useRouter();
  const [loading, setLoading] = useState(false);

  async function handleClick() {
    if (!confirm(confirmText)) return;
    setLoading(true);
    await fetch(url, { method: "DELETE" });
    setLoading(false);
    router.refresh();
  }

  return (
    <button
      onClick={handleClick}
      disabled={loading}
      className="text-sm font-medium text-red-600 hover:underline disabled:opacity-60 dark:text-red-400"
    >
      {loading ? "O'chirilmoqda..." : "O'chirish"}
    </button>
  );
}
