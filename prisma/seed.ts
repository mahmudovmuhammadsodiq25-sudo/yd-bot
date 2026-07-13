import { PrismaClient } from "@prisma/client";
import bcrypt from "bcryptjs";

const prisma = new PrismaClient();

async function main() {
  const tours = [
    {
      title: "Samarqand: Amir Temur izidan",
      slug: "samarqand-amir-temur",
      location: "Samarqand",
      description:
        "Registon maydoni, Gur-Amir maqbarasi va Shohi Zinda majmuasini ziyorat qiladigan 2 kunlik tur. Mahalliy gid va mehmonxona narxga kiritilgan.",
      price: 120,
      days: 2,
      imageUrl: "https://images.unsplash.com/photo-1596395871672-4e8c81e0b0c3?w=1200&q=80",
      featured: true,
    },
    {
      title: "Buxoro: Qadimiy shahar sirlari",
      slug: "buxoro-qadimiy-shahar",
      location: "Buxoro",
      description:
        "Ark qal'asi, Labi Hovuz va Poi Kalon majmuasi bo'ylab sayohat. Mahalliy hunarmandchilik ustaxonalariga tashrif bilan.",
      price: 100,
      days: 2,
      imageUrl: "https://images.unsplash.com/photo-1601074231000-79b8c9c9a1c1?w=1200&q=80",
      featured: true,
    },
    {
      title: "Xiva: Ichan Qal'a sayohati",
      slug: "xiva-ichan-qala",
      location: "Xiva",
      description:
        "UNESCO ro'yxatidagi Ichan Qal'a devorlari ichida bir kunlik piyoda sayohat, kechqurun milliy taomlar bilan tanishtiruv.",
      price: 90,
      days: 1,
      imageUrl: "https://images.unsplash.com/photo-1590766940554-153faf87eaad?w=1200&q=80",
      featured: true,
    },
    {
      title: "Chimyon tog'lari: Faol dam olish",
      slug: "chimyon-toglari",
      location: "Chimyon",
      description:
        "Kanatli yo'l orqali tog' cho'qqisiga chiqish, piyoda sayr va tabiat qo'ynida piknik bilan bir kunlik tur.",
      price: 60,
      days: 1,
      imageUrl: "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1200&q=80",
      featured: false,
    },
  ];

  for (const tour of tours) {
    await prisma.tour.upsert({
      where: { slug: tour.slug },
      update: tour,
      create: tour,
    });
  }

  const posts = [
    {
      title: "O'zbekistonga sayohat qilishning 5 sababi",
      slug: "ozbekistonga-sayohat-5-sabab",
      excerpt: "Buyuk Ipak yo'li shaharlaridan tortib mehmondo'stlikkacha — nega aynan O'zbekiston keyingi manzilingiz bo'lishi kerak.",
      content:
        "O'zbekiston Markaziy Osiyoning yuragi bo'lib, ming yillik tarix, betakror me'morchilik va samimiy mehmondo'stlik bilan mashhur. Samarqand, Buxoro va Xiva kabi shaharlar sayyohlarni o'zining ko'k gumbazli masjidlari, bozorlari va an'anaviy taomlari bilan sehrlaydi.",
      imageUrl: "https://images.unsplash.com/photo-1518998053901-5348d3961a04?w=1200&q=80",
      published: true,
    },
    {
      title: "Samarqandda qayerga borish kerak?",
      slug: "samarqandda-qayerga-borish-kerak",
      excerpt: "Registon, Shohi Zinda va boshqa albatta ko'rish kerak bo'lgan joylar ro'yxati.",
      content:
        "Samarqand — Buyuk Ipak yo'lining marvaridi. Registon maydoni, Shohi Zinda maqbaralar majmuasi va Ulug'bek observatoriyasi shahar bo'ylab sayohatingizda albatta ko'rilishi kerak bo'lgan joylar hisoblanadi.",
      imageUrl: "https://images.unsplash.com/photo-1583417319070-4a69db38a482?w=1200&q=80",
      published: true,
    },
  ];

  for (const post of posts) {
    await prisma.post.upsert({
      where: { slug: post.slug },
      update: post,
      create: post,
    });
  }

  const adminUsername = process.env.SEED_ADMIN_USERNAME || "admin";
  const adminPassword = process.env.SEED_ADMIN_PASSWORD || "admin123";
  const passwordHash = await bcrypt.hash(adminPassword, 10);
  await prisma.adminUser.upsert({
    where: { username: adminUsername },
    update: { passwordHash },
    create: { username: adminUsername, passwordHash },
  });

  console.log("Seed complete.");
  console.log(`Admin login -> username: ${adminUsername}, password: ${adminPassword}`);
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
