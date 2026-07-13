import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { getAdminUsername } from "@/lib/auth";

export async function PUT(req: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  const username = await getAdminUsername();
  if (!username) return NextResponse.json({ error: "Ruxsat yo'q" }, { status: 401 });

  const { id } = await params;
  const body = await req.json().catch(() => null);
  if (!body) return NextResponse.json({ error: "Noto'g'ri so'rov" }, { status: 400 });

  const { title, slug, excerpt, content, imageUrl, published } = body;

  const post = await prisma.post.update({
    where: { id },
    data: {
      title,
      slug,
      excerpt,
      content,
      imageUrl: imageUrl || null,
      published: Boolean(published),
    },
  });

  return NextResponse.json({ post });
}

export async function DELETE(_req: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  const username = await getAdminUsername();
  if (!username) return NextResponse.json({ error: "Ruxsat yo'q" }, { status: 401 });

  const { id } = await params;
  await prisma.post.delete({ where: { id } });

  return NextResponse.json({ ok: true });
}
