import Image from "next/image";
import { notFound } from "next/navigation";
import { prisma } from "@/lib/prisma";

export const dynamic = "force-dynamic";

export default async function BlogPostPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const post = await prisma.post.findUnique({ where: { slug } });

  if (!post || !post.published) notFound();

  return (
    <article className="mx-auto max-w-3xl px-4 py-16">
      <div className="relative h-72 w-full overflow-hidden rounded-2xl bg-neutral-200 sm:h-96 dark:bg-neutral-800">
        {post.imageUrl && (
          <Image src={post.imageUrl} alt={post.title} fill priority className="object-cover" />
        )}
      </div>
      <h1 className="mt-8 text-3xl font-extrabold text-neutral-900 dark:text-white">
        {post.title}
      </h1>
      <p className="mt-2 text-sm text-neutral-500 dark:text-neutral-400">
        {new Date(post.createdAt).toLocaleDateString("uz-UZ")}
      </p>
      <div className="mt-8 whitespace-pre-line leading-relaxed text-neutral-700 dark:text-neutral-300">
        {post.content}
      </div>
    </article>
  );
}
