import { redirect } from "next/navigation";
import { getAdminUsername } from "@/lib/auth";
import { prisma } from "@/lib/prisma";
import BookingStatusSelect from "@/components/admin/BookingStatusSelect";
import DeleteButton from "@/components/admin/DeleteButton";

export default async function AdminBookingsPage() {
  const username = await getAdminUsername();
  if (!username) redirect("/admin/login");

  const bookings = await prisma.booking.findMany({
    include: { tour: true },
    orderBy: { createdAt: "desc" },
  });

  return (
    <div>
      <h1 className="text-2xl font-bold text-neutral-900 dark:text-white">Buyurtmalar</h1>

      <div className="mt-6 overflow-x-auto rounded-2xl border border-black/10 bg-white dark:border-white/10 dark:bg-neutral-900">
        <table className="w-full text-left text-sm">
          <thead className="border-b border-black/10 text-neutral-500 dark:border-white/10 dark:text-neutral-400">
            <tr>
              <th className="px-4 py-3">Mijoz</th>
              <th className="px-4 py-3">Tur</th>
              <th className="px-4 py-3">Telefon</th>
              <th className="px-4 py-3">Kishilar</th>
              <th className="px-4 py-3">Sana</th>
              <th className="px-4 py-3">Holat</th>
              <th className="px-4 py-3 text-right">Amallar</th>
            </tr>
          </thead>
          <tbody>
            {bookings.map((b) => (
              <tr key={b.id} className="border-b border-black/5 last:border-0 dark:border-white/5">
                <td className="px-4 py-3 font-medium text-neutral-900 dark:text-white">{b.fullName}</td>
                <td className="px-4 py-3">{b.tour.title}</td>
                <td className="px-4 py-3">{b.phone}</td>
                <td className="px-4 py-3">{b.people}</td>
                <td className="px-4 py-3">{new Date(b.travelDate).toLocaleDateString("uz-UZ")}</td>
                <td className="px-4 py-3">
                  <BookingStatusSelect bookingId={b.id} status={b.status} />
                </td>
                <td className="px-4 py-3 text-right">
                  <DeleteButton
                    url={`/api/admin/bookings/${b.id}`}
                    confirmText={`${b.fullName} buyurtmasini o'chirishga ishonchingiz komilmi?`}
                  />
                </td>
              </tr>
            ))}
            {bookings.length === 0 && (
              <tr>
                <td colSpan={7} className="px-4 py-6 text-center text-neutral-500">
                  Hozircha buyurtmalar yo&apos;q.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
