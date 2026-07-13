"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";

const links = [
  { href: "/admin", label: "Dashboard" },
  { href: "/admin/tours", label: "Turlar" },
  { href: "/admin/posts", label: "Blog" },
  { href: "/admin/bookings", label: "Buyurtmalar" },
];

export default function AdminNav({ username }: { username: string }) {
  const router = useRouter();

  async function handleLogout() {
    await fetch("/api/admin/logout", { method: "POST" });
    router.push("/admin/login");
    router.refresh();
  }

  return (
    <header className="border-b border-black/10 bg-white dark:border-white/10 dark:bg-neutral-900">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
        <div className="flex items-center gap-8">
          <span className="text-lg font-bold text-teal-700 dark:text-teal-400">
            Sayyoh.uz admin
          </span>
          <nav className="flex gap-5 text-sm font-medium">
            {links.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="text-neutral-700 hover:text-teal-700 dark:text-neutral-300 dark:hover:text-teal-400"
              >
                {link.label}
              </Link>
            ))}
          </nav>
        </div>
        <div className="flex items-center gap-4 text-sm">
          <span className="text-neutral-500 dark:text-neutral-400">{username}</span>
          <button
            onClick={handleLogout}
            className="rounded-full border border-black/15 px-4 py-1.5 font-medium text-neutral-700 hover:bg-black/5 dark:border-white/15 dark:text-neutral-300 dark:hover:bg-white/5"
          >
            Chiqish
          </button>
        </div>
      </div>
    </header>
  );
}
