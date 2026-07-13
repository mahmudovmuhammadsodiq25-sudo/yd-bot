import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { getAdminUsername } from "@/lib/auth";

export async function POST(req: NextRequest) {
  const username = await getAdminUsername();
  if (!username) return NextResponse.json({ error: "Ruxsat yo'q" }, { status: 401 });

  const body = await req.json().catch(() => null);
  if (!body) return NextResponse.json({ error: "Noto'g'ri so'rov" }, { status: 400 });

  const { title, slug, location, description, price, days, imageUrl, featured } = body;
  if (!title || !slug || !location || !description || !price || !days) {
    return NextResponse.json({ error: "Barcha majburiy maydonlarni to'ldiring" }, { status: 400 });
  }

  const tour = await prisma.tour.create({
    data: {
      title,
      slug,
      location,
      description,
      price: Number(price),
      days: Number(days),
      imageUrl: imageUrl || null,
      featured: Boolean(featured),
    },
  });

  return NextResponse.json({ tour }, { status: 201 });
}
