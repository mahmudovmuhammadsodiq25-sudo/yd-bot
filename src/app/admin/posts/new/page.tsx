import { redirect } from "next/navigation";
import { getAdminUsername } from "@/lib/auth";
import PostForm from "@/components/admin/PostForm";

export default async function NewPostPage() {
  const username = await getAdminUsername();
  if (!username) redirect("/admin/login");

  return (
    <div>
      <h1 className="text-2xl font-bold text-neutral-900 dark:text-white">Yangi maqola qo&apos;shish</h1>
      <div className="mt-6">
        <PostForm />
      </div>
    </div>
  );
}
