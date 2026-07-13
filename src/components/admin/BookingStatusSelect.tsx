"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

export default function BookingStatusSelect({
  bookingId,
  status,
}: {
  bookingId: string;
  status: string;
}) {
  const router = useRouter();
  const [loading, setLoading] = useState(false);

  async function handleChange(e: React.ChangeEvent<HTMLSelectElement>) {
    setLoading(true);
    await fetch(`/api/admin/bookings/${bookingId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status: e.target.value }),
    });
    setLoading(false);
    router.refresh();
  }

  return (
    <select
      defaultValue={status}
      onChange={handleChange}
      disabled={loading}
      className="rounded-lg border border-black/15 bg-white px-2 py-1 text-sm dark:border-white/15 dark:bg-neutral-900"
    >
      <option value="pending">Kutilmoqda</option>
      <option value="confirmed">Tasdiqlangan</option>
      <option value="cancelled">Bekor qilingan</option>
    </select>
  );
}
