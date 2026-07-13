import { Geist, Geist_Mono } from "next/font/google";
import "../globals.css";
import AdminNav from "@/components/AdminNav";
import { getAdminUsername } from "@/lib/auth";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata = {
  title: "Admin panel — Sayyoh.uz",
};

export default async function AdminLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const username = await getAdminUsername();

  return (
    <html lang="uz" className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}>
      <body className="min-h-full bg-neutral-100 dark:bg-neutral-950">
        {username && <AdminNav username={username} />}
        <main className={username ? "mx-auto max-w-6xl px-4 py-8" : ""}>{children}</main>
      </body>
    </html>
  );
}
