import Link from "next/link";
import Image from "next/image";
import { prisma } from "@/lib/prisma";

export const dynamic = "force-dynamic";

export default async function HomePage() {
  const featuredTours = await prisma.tour.findMany({
    where: { featured: true },
    orderBy: { createdAt: "desc" },
    take: 3,
  });

  const latestPosts = await prisma.post.findMany({
    where: { published: true },
    orderBy: { createdAt: "desc" },
    take: 2,
  });

  return (
    <div>
      <section className="relative overflow-hidden bg-gradient-to-br from-teal-700 to-emerald-800 text-white">
        <div className="mx-auto max-w-6xl px-4 py-24 sm:py-32">
          <p className="text-sm font-semibold uppercase tracking-widest text-teal-200">
            Buyuk Ipak Yo&apos;li bo&apos;ylab
          </p>
          <h1 className="mt-4 max-w-2xl text-4xl font-extrabold leading-tight sm:text-5xl">
            O&apos;zbekistonning eng go&apos;zal manzillarini biz bilan kashf eting
          </h1>
          <p className="mt-6 max-w-xl text-lg text-teal-50">
            Samarqand, Buxoro, Xiva va boshqa tarixiy shaharlarga tashkil qilingan
            turlar. Tajribali gidlar, qulay narxlar va unutilmas xotiralar.
          </p>
          <div className="mt-8 flex gap-4">
            <Link
              href="/tours"
              className="rounded-full bg-white px-6 py-3 font-semibold text-teal-800 shadow-lg transition hover:bg-teal-50"
            >
              Turlarni ko&apos;rish
            </Link>
            <Link
              href="/contact"
              className="rounded-full border border-white/60 px-6 py-3 font-semibold text-white transition hover:bg-white/10"
            >
              Biz bilan bog&apos;lanish
            </Link>
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-4 py-16">
        <div className="flex items-end justify-between">
          <h2 className="text-2xl font-bold text-neutral-900 dark:text-white">
            Ommabop turlar
          </h2>
          <Link href="/tours" className="text-sm font-medium text-teal-700 hover:underline dark:text-teal-400">
            Barchasini ko&apos;rish →
          </Link>
        </div>
        <div className="mt-8 grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
          {featuredTours.map((tour) => (
            <Link
              key={tour.id}
              href={`/tours/${tour.slug}`}
              className="group overflow-hidden rounded-2xl border border-black/10 bg-white shadow-sm transition hover:shadow-lg dark:border-white/10 dark:bg-neutral-900"
            >
              <div className="relative h-48 w-full overflow-hidden bg-neutral-200 dark:bg-neutral-800">
                {tour.imageUrl && (
                  <Image
                    src={tour.imageUrl}
                    alt={tour.title}
                    fill
                    className="object-cover transition duration-300 group-hover:scale-105"
                  />
                )}
              </div>
              <div className="p-5">
                <p className="text-xs font-semibold uppercase tracking-wide text-teal-700 dark:text-teal-400">
                  {tour.location} · {tour.days} kun
                </p>
                <h3 className="mt-2 text-lg font-bold text-neutral-900 dark:text-white">
                  {tour.title}
                </h3>
                <p className="mt-3 font-semibold text-neutral-700 dark:text-neutral-300">
                  ${tour.price} dan boshlab
                </p>
              </div>
            </Link>
          ))}
        </div>
      </section>

      <section className="bg-neutral-50 py-16 dark:bg-neutral-900">
        <div className="mx-auto max-w-6xl px-4">
          <div className="flex items-end justify-between">
            <h2 className="text-2xl font-bold text-neutral-900 dark:text-white">
              So&apos;nggi maqolalar
            </h2>
            <Link href="/blog" className="text-sm font-medium text-teal-700 hover:underline dark:text-teal-400">
              Blogga o&apos;tish →
            </Link>
          </div>
          <div className="mt-8 grid gap-8 sm:grid-cols-2">
            {latestPosts.map((post) => (
              <Link
                key={post.id}
                href={`/blog/${post.slug}`}
                className="group flex gap-5 rounded-2xl border border-black/10 bg-white p-4 shadow-sm transition hover:shadow-lg dark:border-white/10 dark:bg-neutral-950"
              >
                <div className="relative h-24 w-32 shrink-0 overflow-hidden rounded-xl bg-neutral-200 dark:bg-neutral-800">
                  {post.imageUrl && (
                    <Image src={post.imageUrl} alt={post.title} fill className="object-cover" />
                  )}
                </div>
                <div>
                  <h3 className="font-bold text-neutral-900 group-hover:text-teal-700 dark:text-white dark:group-hover:text-teal-400">
                    {post.title}
                  </h3>
                  <p className="mt-2 text-sm text-neutral-600 dark:text-neutral-400 line-clamp-2">
                    {post.excerpt}
                  </p>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
