"use client";

import { useState, type FormEvent } from "react";
import { useRouter } from "next/navigation";

type Tour = {
  id: string;
  title: string;
  slug: string;
  location: string;
  description: string;
  price: number;
  days: number;
  imageUrl: string | null;
  featured: boolean;
};

export default function TourForm({ tour }: { tour?: Tour }) {
  const router = useRouter();
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setLoading(true);
    setError("");

    const data = new FormData(e.currentTarget);
    const payload = {
      title: data.get("title"),
      slug: data.get("slug"),
      location: data.get("location"),
      description: data.get("description"),
      price: data.get("price"),
      days: data.get("days"),
      imageUrl: data.get("imageUrl"),
      featured: data.get("featured") === "on",
    };

    const res = await fetch(tour ? `/api/admin/tours/${tour.id}` : "/api/admin/tours", {
      method: tour ? "PUT" : "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    setLoading(false);

    if (!res.ok) {
      const body = await res.json().catch(() => ({}));
      setError(body.error || "Xatolik yuz berdi");
      return;
    }

    router.push("/admin/tours");
    router.refresh();
  }

  return (
    <form onSubmit={handleSubmit} className="max-w-2xl space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <Field label="Sarlavha">
          <input name="title" required defaultValue={tour?.title} className={inputClass} />
        </Field>
        <Field label="Slug (URL)">
          <input name="slug" required defaultValue={tour?.slug} className={inputClass} />
        </Field>
      </div>
      <div className="grid grid-cols-3 gap-4">
        <Field label="Manzil">
          <input name="location" required defaultValue={tour?.location} className={inputClass} />
        </Field>
        <Field label="Narx ($)">
          <input name="price" type="number" required defaultValue={tour?.price} className={inputClass} />
        </Field>
        <Field label="Kunlar soni">
          <input name="days" type="number" required defaultValue={tour?.days} className={inputClass} />
        </Field>
      </div>
      <Field label="Rasm URL manzili">
        <input name="imageUrl" defaultValue={tour?.imageUrl ?? ""} className={inputClass} />
      </Field>
      <Field label="Tavsif">
        <textarea name="description" rows={5} required defaultValue={tour?.description} className={inputClass} />
      </Field>
      <label className="flex items-center gap-2 text-sm text-neutral-700 dark:text-neutral-300">
        <input type="checkbox" name="featured" defaultChecked={tour?.featured} />
        Bosh sahifada ko&apos;rsatilsin (ommabop)
      </label>

      {error && <p className="text-sm text-red-600 dark:text-red-400">{error}</p>}

      <button
        type="submit"
        disabled={loading}
        className="rounded-full bg-teal-700 px-6 py-2.5 font-semibold text-white transition hover:bg-teal-800 disabled:opacity-60"
      >
        {loading ? "Saqlanmoqda..." : tour ? "Saqlash" : "Yaratish"}
      </button>
    </form>
  );
}

const inputClass =
  "w-full rounded-lg border border-black/15 bg-white px-3 py-2 text-sm outline-none focus:border-teal-600 dark:border-white/15 dark:bg-neutral-900";

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div>
      <label className="mb-1 block text-sm font-medium text-neutral-700 dark:text-neutral-300">
        {label}
      </label>
      {children}
    </div>
  );
}
