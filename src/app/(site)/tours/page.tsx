import Link from "next/link";
import Image from "next/image";
import { prisma } from "@/lib/prisma";
import { CATEGORIES, categoryEmoji, categoryLabel } from "@/lib/categories";

export const metadata = {
  title: "Manzillar — Anklavtour",
};

export const dynamic = "force-dynamic";

export default async function ToursPage({
  searchParams,
}: {
  searchParams: Promise<{ category?: string }>;
}) {
  const { category } = await searchParams;
  const validCategory = CATEGORIES.some((c) => c.value === category) ? category : undefined;

  const tours = await prisma.tour.findMany({
    where: validCategory ? { category: validCategory } : undefined,
    orderBy: { createdAt: "desc" },
  });

  return (
    <div className="mx-auto max-w-6xl px-4 py-16">
      <h1 className="text-3xl font-extrabold text-neutral-900 dark:text-white">
        Barcha manzillar
      </h1>
      <p className="mt-2 text-neutral-600 dark:text-neutral-400">
        Sayohat turlari, ziyoratgohlar, dam olish hududlari va davolanish maskanlari — barchasi bir joyda.
      </p>

      <div className="mt-6 flex flex-wrap gap-2">
        <Link
          href="/tours"
          className={`rounded-full px-4 py-2 text-sm font-medium transition ${
            !validCategory
              ? "bg-teal-700 text-white"
              : "border border-black/10 text-neutral-700 hover:bg-black/5 dark:border-white/10 dark:text-neutral-300 dark:hover:bg-white/5"
          }`}
        >
          Barchasi
        </Link>
        {CATEGORIES.map((c) => (
          <Link
            key={c.value}
            href={`/tours?category=${c.value}`}
            className={`rounded-full px-4 py-2 text-sm font-medium transition ${
              validCategory === c.value
                ? "bg-teal-700 text-white"
                : "border border-black/10 text-neutral-700 hover:bg-black/5 dark:border-white/10 dark:text-neutral-300 dark:hover:bg-white/5"
            }`}
          >
            {c.emoji} {c.label}
          </Link>
        ))}
      </div>

      <div className="mt-10 grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
        {tours.map((tour) => (
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
              <span className="absolute left-3 top-3 rounded-full bg-black/60 px-3 py-1 text-xs font-semibold text-white">
                {categoryEmoji(tour.category)} {categoryLabel(tour.category)}
              </span>
            </div>
            <div className="p-5">
              <p className="text-xs font-semibold uppercase tracking-wide text-teal-700 dark:text-teal-400">
                {tour.country} · {tour.location} · {tour.days} kun
              </p>
              <h3 className="mt-2 text-lg font-bold text-neutral-900 dark:text-white">
                {tour.title}
              </h3>
              <p className="mt-3 text-sm text-neutral-600 line-clamp-2 dark:text-neutral-400">
                {tour.description}
              </p>
              <p className="mt-3 font-semibold text-neutral-700 dark:text-neutral-300">
                ${tour.price} dan boshlab
              </p>
            </div>
          </Link>
        ))}
        {tours.length === 0 && (
          <p className="text-neutral-500">Bu kategoriyada hozircha manzillar mavjud emas.</p>
        )}
      </div>
    </div>
  );
}
