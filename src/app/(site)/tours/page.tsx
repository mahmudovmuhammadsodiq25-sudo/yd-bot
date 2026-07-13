import Link from "next/link";
import Image from "next/image";
import { prisma } from "@/lib/prisma";

export const metadata = {
  title: "Turlar — Sayyoh.uz",
};

export const dynamic = "force-dynamic";

export default async function ToursPage() {
  const tours = await prisma.tour.findMany({ orderBy: { createdAt: "desc" } });

  return (
    <div className="mx-auto max-w-6xl px-4 py-16">
      <h1 className="text-3xl font-extrabold text-neutral-900 dark:text-white">
        Barcha turlar
      </h1>
      <p className="mt-2 text-neutral-600 dark:text-neutral-400">
        O&apos;zbekistonning eng mashhur manzillariga sayohatlarni tanlang.
      </p>

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
            </div>
            <div className="p-5">
              <p className="text-xs font-semibold uppercase tracking-wide text-teal-700 dark:text-teal-400">
                {tour.location} · {tour.days} kun
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
          <p className="text-neutral-500">Hozircha turlar mavjud emas.</p>
        )}
      </div>
    </div>
  );
}
