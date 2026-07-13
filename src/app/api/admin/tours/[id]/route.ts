import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { getAdminUsername } from "@/lib/auth";
import { CATEGORIES } from "@/lib/categories";

const VALID_CATEGORIES = CATEGORIES.map((c) => c.value) as string[];

export async function PUT(req: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  const username = await getAdminUsername();
  if (!username) return NextResponse.json({ error: "Ruxsat yo'q" }, { status: 401 });

  const { id } = await params;
  const body = await req.json().catch(() => null);
  if (!body) return NextResponse.json({ error: "Noto'g'ri so'rov" }, { status: 400 });

  const {
    title,
    slug,
    category,
    country,
    location,
    description,
    price,
    days,
    imageUrl,
    latitude,
    longitude,
    featured,
    gallery,
  } = body;

  if (category && !VALID_CATEGORIES.includes(category)) {
    return NextResponse.json({ error: "Noto'g'ri kategoriya" }, { status: 400 });
  }

  const tour = await prisma.tour.update({
    where: { id },
    data: {
      title,
      slug,
      category: category || "tur",
      country,
      location,
      description,
      price: Number(price),
      days: Number(days),
      imageUrl: imageUrl || null,
      latitude: latitude !== null && latitude !== undefined && latitude !== "" ? Number(latitude) : null,
      longitude: longitude !== null && longitude !== undefined && longitude !== "" ? Number(longitude) : null,
      featured: Boolean(featured),
      images: Array.isArray(gallery)
        ? {
            deleteMany: {},
            create: gallery.map((url: string, order: number) => ({ url, order })),
          }
        : undefined,
    },
  });

  return NextResponse.json({ tour });
}

export async function DELETE(_req: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  const username = await getAdminUsername();
  if (!username) return NextResponse.json({ error: "Ruxsat yo'q" }, { status: 401 });

  const { id } = await params;
  await prisma.booking.deleteMany({ where: { tourId: id } });
  await prisma.tour.delete({ where: { id } });

  return NextResponse.json({ ok: true });
}
