import { redirect, notFound } from "next/navigation";
import { getAdminUsername } from "@/lib/auth";
import { prisma } from "@/lib/prisma";
import TourForm from "@/components/admin/TourForm";

export default async function EditTourPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const username = await getAdminUsername();
  if (!username) redirect("/admin/login");

  const { id } = await params;
  const tour = await prisma.tour.findUnique({ where: { id } });
  if (!tour) notFound();

  return (
    <div>
      <h1 className="text-2xl font-bold text-neutral-900 dark:text-white">Turni tahrirlash</h1>
      <div className="mt-6">
        <TourForm tour={tour} />
      </div>
    </div>
  );
}
