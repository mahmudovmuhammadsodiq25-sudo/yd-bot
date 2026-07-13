import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { getAdminUsername } from "@/lib/auth";
import { CATEGORIES } from "@/lib/categories";

const VALID_CATEGORIES = CATEGORIES.map((c) => c.value) as string[];

export async function POST(req: NextRequest) {
  const username = await getAdminUsername();
  if (!username) return NextResponse.json({ error: "Ruxsat yo'q" }, { status: 401 });

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

  if (!title || !slug || !country || !location || !description || !price || !days) {
    return NextResponse.json({ error: "Barcha majburiy maydonlarni to'ldiring" }, { status: 400 });
  }

  if (category && !VALID_CATEGORIES.includes(category)) {
    return NextResponse.json({ error: "Noto'g'ri kategoriya" }, { status: 400 });
  }

  const tour = await prisma.tour.create({
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
        ? { create: gallery.map((url: string, order: number) => ({ url, order })) }
        : undefined,
    },
  });

  return NextResponse.json({ tour }, { status: 201 });
}
