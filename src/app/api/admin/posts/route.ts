import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { getAdminUsername } from "@/lib/auth";

export async function POST(req: NextRequest) {
  const username = await getAdminUsername();
  if (!username) return NextResponse.json({ error: "Ruxsat yo'q" }, { status: 401 });

  const body = await req.json().catch(() => null);
  if (!body) return NextResponse.json({ error: "Noto'g'ri so'rov" }, { status: 400 });

  const { title, slug, excerpt, content, imageUrl, published } = body;
  if (!title || !slug || !excerpt || !content) {
    return NextResponse.json({ error: "Barcha majburiy maydonlarni to'ldiring" }, { status: 400 });
  }

  const post = await prisma.post.create({
    data: {
      title,
      slug,
      excerpt,
      content,
      imageUrl: imageUrl || null,
      published: published === undefined ? true : Boolean(published),
    },
  });

  return NextResponse.json({ post }, { status: 201 });
}
