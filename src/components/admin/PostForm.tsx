"use client";

import { useState, type FormEvent } from "react";
import { useRouter } from "next/navigation";

type Post = {
  id: string;
  title: string;
  slug: string;
  excerpt: string;
  content: string;
  imageUrl: string | null;
  published: boolean;
};

export default function PostForm({ post }: { post?: Post }) {
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
      excerpt: data.get("excerpt"),
      content: data.get("content"),
      imageUrl: data.get("imageUrl"),
      published: data.get("published") === "on",
    };

    const res = await fetch(post ? `/api/admin/posts/${post.id}` : "/api/admin/posts", {
      method: post ? "PUT" : "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    setLoading(false);

    if (!res.ok) {
      const body = await res.json().catch(() => ({}));
      setError(body.error || "Xatolik yuz berdi");
      return;
    }

    router.push("/admin/posts");
    router.refresh();
  }

  return (
    <form onSubmit={handleSubmit} className="max-w-2xl space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <Field label="Sarlavha">
          <input name="title" required defaultValue={post?.title} className={inputClass} />
        </Field>
        <Field label="Slug (URL)">
          <input name="slug" required defaultValue={post?.slug} className={inputClass} />
        </Field>
      </div>
      <Field label="Rasm URL manzili">
        <input name="imageUrl" defaultValue={post?.imageUrl ?? ""} className={inputClass} />
      </Field>
      <Field label="Qisqacha tavsif">
        <textarea name="excerpt" rows={2} required defaultValue={post?.excerpt} className={inputClass} />
      </Field>
      <Field label="To'liq matn">
        <textarea name="content" rows={8} required defaultValue={post?.content} className={inputClass} />
      </Field>
      <label className="flex items-center gap-2 text-sm text-neutral-700 dark:text-neutral-300">
        <input type="checkbox" name="published" defaultChecked={post?.published ?? true} />
        Chop etilsin (saytda ko&apos;rinsin)
      </label>

      {error && <p className="text-sm text-red-600 dark:text-red-400">{error}</p>}

      <button
        type="submit"
        disabled={loading}
        className="rounded-full bg-teal-700 px-6 py-2.5 font-semibold text-white transition hover:bg-teal-800 disabled:opacity-60"
      >
        {loading ? "Saqlanmoqda..." : post ? "Saqlash" : "Yaratish"}
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
