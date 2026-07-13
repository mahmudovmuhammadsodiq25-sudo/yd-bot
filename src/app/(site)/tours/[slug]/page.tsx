import Image from "next/image";
import { notFound } from "next/navigation";
import { prisma } from "@/lib/prisma";
import BookingForm from "@/components/BookingForm";
import { categoryEmoji, categoryLabel } from "@/lib/categories";

export const dynamic = "force-dynamic";

export default async function TourDetailPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const tour = await prisma.tour.findUnique({
    where: { slug },
    include: { images: { orderBy: { order: "asc" } } },
  });

  if (!tour) notFound();

  const mapUrl =
    tour.latitude !== null && tour.longitude !== null
      ? `https://www.google.com/maps?q=${tour.latitude},${tour.longitude}`
      : `https://www.google.com/maps/search/${encodeURIComponent(`${tour.location}, ${tour.country}`)}`;

  return (
    <div className="mx-auto max-w-6xl px-4 py-16">
      <div className="grid gap-12 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <div className="relative h-72 w-full overflow-hidden rounded-2xl bg-neutral-200 sm:h-96 dark:bg-neutral-800">
            {tour.imageUrl && (
              <Image src={tour.imageUrl} alt={tour.title} fill priority className="object-cover" />
            )}
            <span className="absolute left-4 top-4 rounded-full bg-black/60 px-3 py-1 text-xs font-semibold text-white">
              {categoryEmoji(tour.category)} {categoryLabel(tour.category)}
            </span>
          </div>

          {tour.images.length > 0 && (
            <div className="mt-3 grid grid-cols-4 gap-3">
              {tour.images.map((img) => (
                <div
                  key={img.id}
                  className="relative h-20 overflow-hidden rounded-lg bg-neutral-200 dark:bg-neutral-800"
                >
                  <Image src={img.url} alt={tour.title} fill className="object-cover" />
                </div>
              ))}
            </div>
          )}

          <p className="mt-6 text-sm font-semibold uppercase tracking-wide text-teal-700 dark:text-teal-400">
            {tour.country} · {tour.location} · {tour.days} kun
          </p>
          <h1 className="mt-2 text-3xl font-extrabold text-neutral-900 dark:text-white">
            {tour.title}
          </h1>
          <p className="mt-6 whitespace-pre-line leading-relaxed text-neutral-700 dark:text-neutral-300">
            {tour.description}
          </p>

          <a
            href={mapUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="mt-6 inline-flex items-center gap-2 text-sm font-medium text-teal-700 hover:underline dark:text-teal-400"
          >
            📍 Xaritada ko&apos;rish
          </a>
        </div>

        <div>
          <div className="sticky top-24 rounded-2xl border border-black/10 bg-white p-6 shadow-sm dark:border-white/10 dark:bg-neutral-900">
            <p className="text-sm text-neutral-500 dark:text-neutral-400">1 kishi uchun narx</p>
            <p className="text-3xl font-extrabold text-neutral-900 dark:text-white">
              ${tour.price}
            </p>
            <div className="my-6 h-px bg-black/10 dark:bg-white/10" />
            <h2 className="mb-4 font-semibold text-neutral-900 dark:text-white">
              Onlayn band qilish
            </h2>
            <BookingForm tourId={tour.id} />
          </div>
        </div>
      </div>
    </div>
  );
}
