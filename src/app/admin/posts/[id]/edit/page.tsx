import { redirect, notFound } from "next/navigation";
import { getAdminUsername } from "@/lib/auth";
import { prisma } from "@/lib/prisma";
import PostForm from "@/components/admin/PostForm";

export default async function EditPostPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const username = await getAdminUsername();
  if (!username) redirect("/admin/login");

  const { id } = await params;
  const post = await prisma.post.findUnique({ where: { id } });
  if (!post) notFound();

  return (
    <div>
      <h1 className="text-2xl font-bold text-neutral-900 dark:text-white">Maqolani tahrirlash</h1>
      <div className="mt-6">
        <PostForm post={post} />
      </div>
    </div>
  );
}
