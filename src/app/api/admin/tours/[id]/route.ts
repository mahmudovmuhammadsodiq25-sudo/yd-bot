import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { getAdminUsername } from "@/lib/auth";

export async function PUT(req: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  const username = await getAdminUsername();
  if (!username) return NextResponse.json({ error: "Ruxsat yo'q" }, { status: 401 });

  const { id } = await params;
  const body = await req.json().catch(() => null);
  if (!body) return NextResponse.json({ error: "Noto'g'ri so'rov" }, { status: 400 });

  const { title, slug, location, description, price, days, imageUrl, featured } = body;

  const tour = await prisma.tour.update({
    where: { id },
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
