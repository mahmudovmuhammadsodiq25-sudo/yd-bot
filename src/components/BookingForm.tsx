"use client";

import { useState, type FormEvent } from "react";

export default function BookingForm({ tourId }: { tourId: string }) {
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");
  const [errorMessage, setErrorMessage] = useState("");

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setStatus("loading");
    setErrorMessage("");

    const form = e.currentTarget;
    const data = new FormData(form);

    try {
      const res = await fetch("/api/bookings", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          tourId,
          fullName: data.get("fullName"),
          phone: data.get("phone"),
          email: data.get("email"),
          people: Number(data.get("people")),
          travelDate: data.get("travelDate"),
          message: data.get("message"),
        }),
      });

      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body.error || "Xatolik yuz berdi");
      }

      setStatus("success");
      form.reset();
    } catch (err) {
      setStatus("error");
      setErrorMessage(err instanceof Error ? err.message : "Xatolik yuz berdi");
    }
  }

  if (status === "success") {
    return (
      <div className="rounded-xl border border-teal-200 bg-teal-50 p-6 text-teal-800 dark:border-teal-900 dark:bg-teal-950 dark:text-teal-200">
        <p className="font-semibold">Buyurtmangiz qabul qilindi!</p>
        <p className="mt-1 text-sm">
          Tez orada operatorlarimiz siz bilan bog&apos;lanadi.
        </p>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="mb-1 block text-sm font-medium text-neutral-700 dark:text-neutral-300">
          To&apos;liq ism
        </label>
        <input
          name="fullName"
          required
          className="w-full rounded-lg border border-black/15 bg-white px-3 py-2 text-sm outline-none focus:border-teal-600 dark:border-white/15 dark:bg-neutral-900"
        />
      </div>
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="mb-1 block text-sm font-medium text-neutral-700 dark:text-neutral-300">
            Telefon raqami
          </label>
          <input
            name="phone"
            required
            placeholder="+998 90 123 45 67"
            className="w-full rounded-lg border border-black/15 bg-white px-3 py-2 text-sm outline-none focus:border-teal-600 dark:border-white/15 dark:bg-neutral-900"
          />
        </div>
        <div>
          <label className="mb-1 block text-sm font-medium text-neutral-700 dark:text-neutral-300">
            Email (ixtiyoriy)
          </label>
          <input
            name="email"
            type="email"
            className="w-full rounded-lg border border-black/15 bg-white px-3 py-2 text-sm outline-none focus:border-teal-600 dark:border-white/15 dark:bg-neutral-900"
          />
        </div>
      </div>
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="mb-1 block text-sm font-medium text-neutral-700 dark:text-neutral-300">
            Kishilar soni
          </label>
          <input
            name="people"
            type="number"
            min={1}
            defaultValue={1}
            required
            className="w-full rounded-lg border border-black/15 bg-white px-3 py-2 text-sm outline-none focus:border-teal-600 dark:border-white/15 dark:bg-neutral-900"
          />
        </div>
        <div>
          <label className="mb-1 block text-sm font-medium text-neutral-700 dark:text-neutral-300">
            Sayohat sanasi
          </label>
          <input
            name="travelDate"
            type="date"
            required
            className="w-full rounded-lg border border-black/15 bg-white px-3 py-2 text-sm outline-none focus:border-teal-600 dark:border-white/15 dark:bg-neutral-900"
          />
        </div>
      </div>
      <div>
        <label className="mb-1 block text-sm font-medium text-neutral-700 dark:text-neutral-300">
          Qo&apos;shimcha izoh (ixtiyoriy)
        </label>
        <textarea
          name="message"
          rows={3}
          className="w-full rounded-lg border border-black/15 bg-white px-3 py-2 text-sm outline-none focus:border-teal-600 dark:border-white/15 dark:bg-neutral-900"
        />
      </div>

      {status === "error" && (
        <p className="text-sm text-red-600 dark:text-red-400">{errorMessage}</p>
      )}

      <button
        type="submit"
        disabled={status === "loading"}
        className="w-full rounded-full bg-teal-700 px-6 py-3 font-semibold text-white transition hover:bg-teal-800 disabled:opacity-60"
      >
        {status === "loading" ? "Yuborilmoqda..." : "Bandlashni tasdiqlash"}
      </button>
    </form>
  );
}
