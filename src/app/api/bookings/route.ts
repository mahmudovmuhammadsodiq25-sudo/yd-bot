import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { getAdminUsername } from "@/lib/auth";

export async function POST(req: NextRequest) {
  const body = await req.json().catch(() => null);

  if (!body) {
    return NextResponse.json({ error: "Noto'g'ri so'rov" }, { status: 400 });
  }

  const { tourId, fullName, phone, email, people, travelDate, message } = body;

  if (!tourId || !fullName || !phone || !travelDate) {
    return NextResponse.json(
      { error: "Barcha majburiy maydonlarni to'ldiring" },
      { status: 400 }
    );
  }

  const tour = await prisma.tour.findUnique({ where: { id: tourId } });
  if (!tour) {
    return NextResponse.json({ error: "Tur topilmadi" }, { status: 404 });
  }

  const parsedDate = new Date(travelDate);
  if (Number.isNaN(parsedDate.getTime())) {
    return NextResponse.json({ error: "Sana noto'g'ri" }, { status: 400 });
  }

  const booking = await prisma.booking.create({
    data: {
      tourId,
      fullName: String(fullName),
      phone: String(phone),
      email: email ? String(email) : null,
      people: Number(people) > 0 ? Number(people) : 1,
      travelDate: parsedDate,
      message: message ? String(message) : null,
    },
  });

  return NextResponse.json({ booking }, { status: 201 });
}

export async function GET() {
  const username = await getAdminUsername();
  if (!username) {
    return NextResponse.json({ error: "Ruxsat yo'q" }, { status: 401 });
  }

  const bookings = await prisma.booking.findMany({
    include: { tour: true },
    orderBy: { createdAt: "desc" },
  });

  return NextResponse.json({ bookings });
}
