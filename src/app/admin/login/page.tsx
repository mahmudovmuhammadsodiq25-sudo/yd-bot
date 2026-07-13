import { redirect } from "next/navigation";
import { getAdminUsername } from "@/lib/auth";
import LoginForm from "@/components/LoginForm";

export default async function AdminLoginPage() {
  const username = await getAdminUsername();
  if (username) redirect("/admin");

  return (
    <div className="flex min-h-screen flex-col items-center justify-center px-4">
      <h1 className="mb-8 text-2xl font-bold text-teal-700 dark:text-teal-400">
        Anklavtour admin panel
      </h1>
      <LoginForm />
    </div>
  );
}
