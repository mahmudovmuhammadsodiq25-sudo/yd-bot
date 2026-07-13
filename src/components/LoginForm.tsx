"use client";

import { useState, type FormEvent } from "react";
import { useRouter } from "next/navigation";

export default function LoginForm() {
  const router = useRouter();
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setLoading(true);
    setError("");

    const data = new FormData(e.currentTarget);

    const res = await fetch("/api/admin/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: data.get("username"),
        password: data.get("password"),
      }),
    });

    setLoading(false);

    if (!res.ok) {
      const body = await res.json().catch(() => ({}));
      setError(body.error || "Xatolik yuz berdi");
      return;
    }

    router.push("/admin");
    router.refresh();
  }

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-sm space-y-4">
      <div>
        <label className="mb-1 block text-sm font-medium text-neutral-700 dark:text-neutral-300">
          Login
        </label>
        <input
          name="username"
          required
          autoFocus
          className="w-full rounded-lg border border-black/15 bg-white px-3 py-2 text-sm outline-none focus:border-teal-600 dark:border-white/15 dark:bg-neutral-900"
        />
      </div>
      <div>
        <label className="mb-1 block text-sm font-medium text-neutral-700 dark:text-neutral-300">
          Parol
        </label>
        <input
          name="password"
          type="password"
          required
          className="w-full rounded-lg border border-black/15 bg-white px-3 py-2 text-sm outline-none focus:border-teal-600 dark:border-white/15 dark:bg-neutral-900"
        />
      </div>
      {error && <p className="text-sm text-red-600 dark:text-red-400">{error}</p>}
      <button
        type="submit"
        disabled={loading}
        className="w-full rounded-full bg-teal-700 px-6 py-3 font-semibold text-white transition hover:bg-teal-800 disabled:opacity-60"
      >
        {loading ? "Kirilmoqda..." : "Kirish"}
      </button>
    </form>
  );
}
