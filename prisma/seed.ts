import { PrismaClient } from "@prisma/client";
import bcrypt from "bcryptjs";

const prisma = new PrismaClient();

async function main() {
  const tours = [
    {
      title: "Samarqand: Amir Temur izidan",
      slug: "samarqand-amir-temur",
      category: "tur",
      country: "O'zbekiston",
      location: "Samarqand",
      description:
        "Registon maydoni, Gur-Amir maqbarasi va Shohi Zinda majmuasini ziyorat qiladigan 2 kunlik tur. Mahalliy gid va mehmonxona narxga kiritilgan.",
      price: 120,
      days: 2,
      imageUrl: "https://images.unsplash.com/photo-1596395871672-4e8c81e0b0c3?w=1200&q=80",
      latitude: 39.6270,
      longitude: 66.9750,
      featured: true,
      images: [
        "https://images.unsplash.com/photo-1596395871672-4e8c81e0b0c3?w=1200&q=80",
        "https://images.unsplash.com/photo-1583417319070-4a69db38a482?w=1200&q=80",
      ],
    },
    {
      title: "Buxoro: Qadimiy shahar sirlari",
      slug: "buxoro-qadimiy-shahar",
      category: "tur",
      country: "O'zbekiston",
      location: "Buxoro",
      description:
        "Ark qal'asi, Labi Hovuz va Poi Kalon majmuasi bo'ylab sayohat. Mahalliy hunarmandchilik ustaxonalariga tashrif bilan.",
      price: 100,
      days: 2,
      imageUrl: "https://images.unsplash.com/photo-1601074231000-79b8c9c9a1c1?w=1200&q=80",
      latitude: 39.7747,
      longitude: 64.4286,
      featured: true,
      images: [],
    },
    {
      title: "Xiva: Ichan Qal'a sayohati",
      slug: "xiva-ichan-qala",
      category: "tur",
      country: "O'zbekiston",
      location: "Xiva",
      description:
        "UNESCO ro'yxatidagi Ichan Qal'a devorlari ichida bir kunlik piyoda sayohat, kechqurun milliy taomlar bilan tanishtiruv.",
      price: 90,
      days: 1,
      imageUrl: "https://images.unsplash.com/photo-1590766940554-153faf87eaad?w=1200&q=80",
      latitude: 41.3783,
      longitude: 60.3639,
      featured: true,
      images: [],
    },
    {
      title: "Chimyon tog'lari: Faol dam olish",
      slug: "chimyon-toglari",
      category: "dam_olish",
      country: "O'zbekiston",
      location: "Toshkent viloyati, Chimyon",
      description:
        "Kanatli yo'l orqali tog' cho'qqisiga chiqish, piyoda sayr va tabiat qo'ynida piknik bilan bir kunlik tur.",
      price: 60,
      days: 1,
      imageUrl: "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1200&q=80",
      latitude: 41.5333,
      longitude: 70.0167,
      featured: false,
      images: [],
    },
    {
      title: "Shohimardon: ziyorat va tabiat qo'ynida",
      slug: "shohimardon-ziyorat",
      category: "ziyoratgoh",
      country: "O'zbekiston",
      location: "Farg'ona viloyati, Shohimardon",
      description:
        "Hazrat Ali avlodlaridan biriga nisbat beriladigan mozor majmuasi va uni o'rab turgan tog' manzaralari. Sershovqin soy bo'yida dam olish va ziyorat qilish imkoniyati bir joyda.",
      price: 70,
      days: 1,
      imageUrl: "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200&q=80",
      latitude: 39.9967,
      longitude: 71.7783,
      featured: true,
      images: [
        "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200&q=80",
        "https://images.unsplash.com/photo-1483728642387-6c3bdd6c93e5?w=1200&q=80",
      ],
    },
    {
      title: "So'x tumani: tog' va soy bo'yi manzaralari",
      slug: "sox-tumani-manzaralari",
      category: "dam_olish",
      country: "O'zbekiston",
      location: "Farg'ona vodiysi, So'x tumani",
      description:
        "Tog' etaklarida joylashgan tinch soy bo'ylari va yashil vodiylar. Piknik, baliq ovi va sayr uchun qulay hudud, kunduzi issiq, kechqurun salqin tog' havosi bilan.",
      price: 50,
      days: 1,
      imageUrl: "https://images.unsplash.com/photo-1500534623283-312aade485b7?w=1200&q=80",
      latitude: 39.9575,
      longitude: 71.1804,
      featured: false,
      images: [],
    },
    {
      title: "Qulfi Zanjirkisho ziyoratgohi",
      slug: "qulfi-zanjirkisho-ziyoratgohi",
      category: "ziyoratgoh",
      country: "O'zbekiston",
      location: "Farg'ona viloyati, So'x tumani, Xushyor MFY",
      description:
        "So'x tumanining Xushyor mahallasida joylashgan ziyoratgoh. 2003–2004-yillarda qurilgan bo'lib, hududi chegaralangan va obod saqlanadi. Hozirgi kunda mahalliy aholi va tashrif buyuruvchilar uchun ziyorat hamda dam olish maskani sifatida xizmat qilib kelmoqda. Davlat tomonidan diqqatga sazovor joy sifatida rasmiy hatlovdan o'tkazilgan.",
      price: 0,
      days: 1,
      imageUrl: "/images/sox/qulfi-zanjirkisho-1.jpg",
      latitude: 39.91802,
      longitude: 71.06814,
      featured: true,
      images: [
        "/images/sox/qulfi-zanjirkisho-1.jpg",
        "/images/sox/qulfi-zanjirkisho-2.jpg",
      ],
    },
    {
      title: "Quvi qal'asi",
      slug: "quvi-qalasi",
      category: "ziyoratgoh",
      country: "O'zbekiston",
      location: "Farg'ona viloyati, So'x tumani, Saribozorcha MFY",
      description:
        "So'x tumanining Saribozorcha mahallasida joylashgan qadimiy arxeologiya yodgorligi. Eramizdan avvalgi I asrlarda paydo bo'lganligi aniqlangan bo'lib, maydoni 0,80 sotixni tashkil etadi. Qadimiy qal'a xarobalari tepalik ko'rinishida saqlanib qolgan va davlat muhofazasidagi madaniy meros obyektlari ro'yxatiga kiritilgan.",
      price: 0,
      days: 1,
      imageUrl: "/images/sox/quvi-qalasi-1.jpg",
      latitude: 39.96033,
      longitude: 71.14342,
      featured: false,
      images: [
        "/images/sox/quvi-qalasi-1.jpg",
        "/images/sox/quvi-qalasi-2.jpg",
        "/images/sox/quvi-qalasi-3.jpg",
      ],
    },
    {
      title: "Quyi Mug'tepa qal'asi",
      slug: "quyi-mugtepa-qalasi",
      category: "ziyoratgoh",
      country: "O'zbekiston",
      location: "Farg'ona viloyati, So'x tumani, G'aznov MFY",
      description:
        "So'x tumanining G'aznov mahallasida joylashgan arxeologiya yodgorligi. Eramizdan avvalgi I asrlarga oid bo'lib, maydoni 0,50 sotixni tashkil etadi. Yodgorlik rang-barang qoyali tog' yonbag'irlari va bog'lar bilan o'ralgan bo'lib, atrofi betakror tabiiy manzaraga ega. Davlat muhofazasidagi madaniy meros obyekti hisoblanadi.",
      price: 0,
      days: 1,
      imageUrl: "/images/sox/quyi-mugtepa-1.jpg",
      latitude: 40.15045,
      longitude: 71.07811,
      featured: true,
      images: [
        "/images/sox/quyi-mugtepa-1.jpg",
        "/images/sox/quyi-mugtepa-2.jpg",
      ],
    },
    {
      title: "Nodir suratlar qal'asi",
      slug: "nodir-suratlar-qalasi",
      category: "ziyoratgoh",
      country: "O'zbekiston",
      location: "Farg'ona viloyati, So'x tumani, Tul MFY",
      description:
        "So'x tumanining Tul mahallasida joylashgan qadimiy arxeologiya yodgorligi. Paydo bo'lgan davri hozircha aniqlanmagan, maydoni 0,90 sotixni tashkil etadi. Qoyatosh cho'qqilari va So'x daryosi vodiysi manzarasi bag'rida joylashgan bo'lib, davlat muhofazasidagi madaniy meros obyektlari qatoriga kiritilgan.",
      price: 0,
      days: 1,
      imageUrl: "/images/sox/nodir-suratlar-1.jpg",
      latitude: 40.14523,
      longitude: 71.07907,
      featured: false,
      images: [
        "/images/sox/nodir-suratlar-1.jpg",
        "/images/sox/nodir-suratlar-2.jpg",
        "/images/sox/nodir-suratlar-3.jpg",
      ],
    },
    {
      title: "Issiqko'l: Qirg'iziston marvaridi",
      slug: "issiqkol-qirgiziston",
      category: "dam_olish",
      country: "Qirg'iziston",
      location: "Issiqko'l ko'li, Cholpon-Ota",
      description:
        "Dunyodagi eng katta tog' ko'llaridan biri bo'lgan Issiqko'l bo'yida dam olish. Toza havo, tog' manzarasi va qumli plyajlar bilan mashhur, ko'p kunlik dam olish uchun ideal.",
      price: 150,
      days: 3,
      imageUrl: "https://images.unsplash.com/photo-1506929562872-bb421503ef21?w=1200&q=80",
      latitude: 42.6474,
      longitude: 77.0857,
      featured: true,
      images: [],
    },
    {
      title: "Chortoq sanatoriysi: shifobaxsh suvlar maskani",
      slug: "chortoq-sanatoriyasi",
      category: "davolanish",
      country: "O'zbekiston",
      location: "Namangan viloyati, Chortoq",
      description:
        "Mineral issiq suvlari bilan mashhur davolanish maskani. Bo'g'im va asab kasalliklarini davolashda foydalaniladigan sanatoriy, tog' etagida joylashgan.",
      price: 80,
      days: 5,
      imageUrl: "https://images.unsplash.com/photo-1544161515-4ab6ce6db874?w=1200&q=80",
      latitude: 41.15,
      longitude: 71.4667,
      featured: false,
      images: [],
    },
  ];

  for (const { images, ...tour } of tours) {
    const created = await prisma.tour.upsert({
      where: { slug: tour.slug },
      update: tour,
      create: tour,
    });

    await prisma.tourImage.deleteMany({ where: { tourId: created.id } });
    if (images.length > 0) {
      await prisma.tourImage.createMany({
        data: images.map((url, order) => ({ tourId: created.id, url, order })),
      });
    }
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
