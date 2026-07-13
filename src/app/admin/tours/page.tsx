import { redirect } from "next/navigation";
import Link from "next/link";
import { getAdminUsername } from "@/lib/auth";
import { prisma } from "@/lib/prisma";
import DeleteButton from "@/components/admin/DeleteButton";

export default async function AdminToursPage() {
  const username = await getAdminUsername();
  if (!username) redirect("/admin/login");

  const tours = await prisma.tour.findMany({ orderBy: { createdAt: "desc" } });

  return (
    <div>
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-neutral-900 dark:text-white">Turlar</h1>
        <Link
          href="/admin/tours/new"
          className="rounded-full bg-teal-700 px-5 py-2 text-sm font-semibold text-white hover:bg-teal-800"
        >
          + Yangi tur
        </Link>
      </div>

      <div className="mt-6 overflow-x-auto rounded-2xl border border-black/10 bg-white dark:border-white/10 dark:bg-neutral-900">
        <table className="w-full text-left text-sm">
          <thead className="border-b border-black/10 text-neutral-500 dark:border-white/10 dark:text-neutral-400">
            <tr>
              <th className="px-4 py-3">Sarlavha</th>
              <th className="px-4 py-3">Manzil</th>
              <th className="px-4 py-3">Narx</th>
              <th className="px-4 py-3">Ommabop</th>
              <th className="px-4 py-3 text-right">Amallar</th>
            </tr>
          </thead>
          <tbody>
            {tours.map((tour) => (
              <tr key={tour.id} className="border-b border-black/5 last:border-0 dark:border-white/5">
                <td className="px-4 py-3 font-medium text-neutral-900 dark:text-white">{tour.title}</td>
                <td className="px-4 py-3">{tour.location}</td>
                <td className="px-4 py-3">${tour.price}</td>
                <td className="px-4 py-3">{tour.featured ? "Ha" : "Yo'q"}</td>
                <td className="px-4 py-3">
                  <div className="flex justify-end gap-4">
                    <Link
                      href={`/admin/tours/${tour.id}/edit`}
                      className="text-sm font-medium text-teal-700 hover:underline dark:text-teal-400"
                    >
                      Tahrirlash
                    </Link>
                    <DeleteButton
                      url={`/api/admin/tours/${tour.id}`}
                      confirmText={`"${tour.title}" turini o'chirishga ishonchingiz komilmi?`}
                    />
                  </div>
                </td>
              </tr>
            ))}
            {tours.length === 0 && (
              <tr>
                <td colSpan={5} className="px-4 py-6 text-center text-neutral-500">
                  Hozircha turlar yo&apos;q.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
