import { redirect } from "next/navigation";
import Link from "next/link";
import { getAdminUsername } from "@/lib/auth";
import { prisma } from "@/lib/prisma";

export default async function AdminDashboardPage() {
  const username = await getAdminUsername();
  if (!username) redirect("/admin/login");

  const [tourCount, postCount, bookingCount, pendingCount, recentBookings] = await Promise.all([
    prisma.tour.count(),
    prisma.post.count(),
    prisma.booking.count(),
    prisma.booking.count({ where: { status: "pending" } }),
    prisma.booking.findMany({
      include: { tour: true },
      orderBy: { createdAt: "desc" },
      take: 5,
    }),
  ]);

  const stats = [
    { label: "Turlar", value: tourCount, href: "/admin/tours" },
    { label: "Maqolalar", value: postCount, href: "/admin/posts" },
    { label: "Buyurtmalar", value: bookingCount, href: "/admin/bookings" },
    { label: "Kutilayotgan buyurtmalar", value: pendingCount, href: "/admin/bookings" },
  ];

  return (
    <div>
      <h1 className="text-2xl font-bold text-neutral-900 dark:text-white">Dashboard</h1>

      <div className="mt-6 grid gap-4 sm:grid-cols-4">
        {stats.map((stat) => (
          <Link
            key={stat.label}
            href={stat.href}
            className="rounded-2xl border border-black/10 bg-white p-5 shadow-sm transition hover:shadow-md dark:border-white/10 dark:bg-neutral-900"
          >
            <p className="text-sm text-neutral-500 dark:text-neutral-400">{stat.label}</p>
            <p className="mt-1 text-3xl font-bold text-neutral-900 dark:text-white">{stat.value}</p>
          </Link>
        ))}
      </div>

      <div className="mt-10">
        <h2 className="text-lg font-semibold text-neutral-900 dark:text-white">
          So&apos;nggi buyurtmalar
        </h2>
        <div className="mt-4 overflow-x-auto rounded-2xl border border-black/10 bg-white dark:border-white/10 dark:bg-neutral-900">
          <table className="w-full text-left text-sm">
            <thead className="border-b border-black/10 text-neutral-500 dark:border-white/10 dark:text-neutral-400">
              <tr>
                <th className="px-4 py-3">Mijoz</th>
                <th className="px-4 py-3">Tur</th>
                <th className="px-4 py-3">Sana</th>
                <th className="px-4 py-3">Holat</th>
              </tr>
            </thead>
            <tbody>
              {recentBookings.map((b) => (
                <tr key={b.id} className="border-b border-black/5 last:border-0 dark:border-white/5">
                  <td className="px-4 py-3">{b.fullName}</td>
                  <td className="px-4 py-3">{b.tour.title}</td>
                  <td className="px-4 py-3">{new Date(b.travelDate).toLocaleDateString("uz-UZ")}</td>
                  <td className="px-4 py-3 capitalize">{b.status}</td>
                </tr>
              ))}
              {recentBookings.length === 0 && (
                <tr>
                  <td colSpan={4} className="px-4 py-6 text-center text-neutral-500">
                    Hozircha buyurtmalar yo&apos;q.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
