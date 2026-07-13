import Image from "next/image";
import { notFound } from "next/navigation";
import { prisma } from "@/lib/prisma";
import BookingForm from "@/components/BookingForm";

export const dynamic = "force-dynamic";

export default async function TourDetailPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const tour = await prisma.tour.findUnique({ where: { slug } });

  if (!tour) notFound();

  return (
    <div className="mx-auto max-w-6xl px-4 py-16">
      <div className="grid gap-12 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <div className="relative h-72 w-full overflow-hidden rounded-2xl bg-neutral-200 sm:h-96 dark:bg-neutral-800">
            {tour.imageUrl && (
              <Image src={tour.imageUrl} alt={tour.title} fill priority className="object-cover" />
            )}
          </div>

          <p className="mt-6 text-sm font-semibold uppercase tracking-wide text-teal-700 dark:text-teal-400">
            {tour.location} · {tour.days} kunlik tur
          </p>
          <h1 className="mt-2 text-3xl font-extrabold text-neutral-900 dark:text-white">
            {tour.title}
          </h1>
          <p className="mt-6 whitespace-pre-line leading-relaxed text-neutral-700 dark:text-neutral-300">
            {tour.description}
          </p>
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
