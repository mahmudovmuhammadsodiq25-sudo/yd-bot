# Sayyoh.uz — Turizm sayti

O'zbekiston bo'ylab sayohat turlarini taqdim etuvchi, onlayn band qilish, sayohat blogi va admin panelga ega to'liq veb-sayt. Next.js (App Router, TypeScript, Tailwind CSS) va Prisma + SQLite asosida qurilgan.

## Imkoniyatlar

- **Ommaviy sayt** — bosh sahifa, turlar ro'yxati va tur sahifalari, blog, aloqa sahifasi.
- **Onlayn band qilish** — har bir tur sahifasida ism, telefon, sana va kishilar sonini o'z ichiga olgan booking formasi.
- **Admin panel** (`/admin`) — login bilan himoyalangan, turlar va blog maqolalarini qo'shish/tahrirlash/o'chirish, buyurtmalar holatini boshqarish.

## Ishga tushirish

```bash
npm install
npm run db:migrate   # SQLite bazasini yaratadi (prisma/dev.db)
npm run db:seed      # namunaviy turlar, maqolalar va admin foydalanuvchi qo'shadi
npm run dev
```

Sayt http://localhost:3000 da ochiladi.

### Admin panelga kirish

Standart login ma'lumotlari (`prisma/seed.ts` da o'zgartirish mumkin, yoki `SEED_ADMIN_USERNAME` / `SEED_ADMIN_PASSWORD` environment o'zgaruvchilari orqali):

- URL: `/admin/login`
- Login: `admin`
- Parol: `admin123`

**Production muhitida albatta admin parolini o'zgartiring.**

## Muhit o'zgaruvchilari

`.env` faylida (namuna uchun repo ichidagi `.env` ga qarang):

```
DATABASE_URL="file:./dev.db"
ADMIN_SESSION_SECRET="ishlab-chiqarish-uchun-tasodifiy-uzun-matn"
```

`ADMIN_SESSION_SECRET` production muhitida albatta o'zgartirilishi kerak (admin sessiya cookie'sini imzolash uchun ishlatiladi).

## Texnologiyalar

- Next.js 16 (App Router, Server Components)
- TypeScript
- Tailwind CSS v4
- Prisma ORM + SQLite
- bcryptjs (parollarni xeshlash)

## Loyihaning tuzilishi

```
src/
  app/
    (site)/        # ommaviy sahifalar (bosh sahifa, turlar, blog, aloqa)
    admin/         # admin panel sahifalari
    api/           # API route'lar (bookings, admin CRUD, auth)
  components/      # umumiy va admin uchun UI komponentlar
  lib/             # prisma client, auth yordamchi funksiyalari
prisma/
  schema.prisma    # ma'lumotlar bazasi sxemasi
  seed.ts          # namunaviy ma'lumotlar
```

## Deploy qilish

Loyiha istalgan Node.js hosting xizmatida (Vercel, Railway, Render va h.k.) ishlaydi. Production uchun SQLite o'rniga PostgreSQL kabi to'liq boshqariladigan bazadan foydalanish tavsiya etiladi — buning uchun `prisma/schema.prisma` dagi `datasource` provayderini o'zgartiring va `DATABASE_URL` ni yangilang.
