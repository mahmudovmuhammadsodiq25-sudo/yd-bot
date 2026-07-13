import Link from "next/link";
import Image from "next/image";
import { prisma } from "@/lib/prisma";

export const metadata = {
  title: "Blog — Anklavtour",
};

export const dynamic = "force-dynamic";

export default async function BlogPage() {
  const posts = await prisma.post.findMany({
    where: { published: true },
    orderBy: { createdAt: "desc" },
  });

  return (
    <div className="mx-auto max-w-6xl px-4 py-16">
      <h1 className="text-3xl font-extrabold text-neutral-900 dark:text-white">
        Sayohat blogi
      </h1>
      <p className="mt-2 text-neutral-600 dark:text-neutral-400">
        Manzillar, maslahatlar va sayohat hikoyalari.
      </p>

      <div className="mt-10 grid gap-8 sm:grid-cols-2">
        {posts.map((post) => (
          <Link
            key={post.id}
            href={`/blog/${post.slug}`}
            className="group overflow-hidden rounded-2xl border border-black/10 bg-white shadow-sm transition hover:shadow-lg dark:border-white/10 dark:bg-neutral-900"
          >
            <div className="relative h-48 w-full overflow-hidden bg-neutral-200 dark:bg-neutral-800">
              {post.imageUrl && (
                <Image
                  src={post.imageUrl}
                  alt={post.title}
                  fill
                  className="object-cover transition duration-300 group-hover:scale-105"
                />
              )}
            </div>
            <div className="p-5">
              <h2 className="text-lg font-bold text-neutral-900 dark:text-white">
                {post.title}
              </h2>
              <p className="mt-2 text-sm text-neutral-600 line-clamp-3 dark:text-neutral-400">
                {post.excerpt}
              </p>
            </div>
          </Link>
        ))}
        {posts.length === 0 && (
          <p className="text-neutral-500">Hozircha maqolalar mavjud emas.</p>
        )}
      </div>
    </div>
  );
}
