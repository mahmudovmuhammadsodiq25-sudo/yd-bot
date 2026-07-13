import { redirect } from "next/navigation";
import { getAdminUsername } from "@/lib/auth";
import TourForm from "@/components/admin/TourForm";

export default async function NewTourPage() {
  const username = await getAdminUsername();
  if (!username) redirect("/admin/login");

  return (
    <div>
      <h1 className="text-2xl font-bold text-neutral-900 dark:text-white">Yangi tur qo&apos;shish</h1>
      <div className="mt-6">
        <TourForm />
      </div>
    </div>
  );
}
