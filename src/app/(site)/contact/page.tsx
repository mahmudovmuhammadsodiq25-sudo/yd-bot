export const metadata = {
  title: "Aloqa — Sayyoh.uz",
};

export default function ContactPage() {
  return (
    <div className="mx-auto max-w-4xl px-4 py-16">
      <h1 className="text-3xl font-extrabold text-neutral-900 dark:text-white">
        Biz bilan bog&apos;laning
      </h1>
      <p className="mt-2 text-neutral-600 dark:text-neutral-400">
        Savollaringiz bormi? Quyidagi ma&apos;lumotlar orqali biz bilan
        bog&apos;laning, yoki tanlagan turingiz sahifasidagi band qilish
        formasidan foydalaning.
      </p>

      <div className="mt-10 grid gap-8 sm:grid-cols-3">
        <div className="rounded-2xl border border-black/10 p-6 dark:border-white/10">
          <p className="text-sm font-semibold text-teal-700 dark:text-teal-400">Telefon</p>
          <p className="mt-2 text-lg font-medium text-neutral-900 dark:text-white">
            +998 90 123 45 67
          </p>
        </div>
        <div className="rounded-2xl border border-black/10 p-6 dark:border-white/10">
          <p className="text-sm font-semibold text-teal-700 dark:text-teal-400">Email</p>
          <p className="mt-2 text-lg font-medium text-neutral-900 dark:text-white">
            info@sayyoh.uz
          </p>
        </div>
        <div className="rounded-2xl border border-black/10 p-6 dark:border-white/10">
          <p className="text-sm font-semibold text-teal-700 dark:text-teal-400">Manzil</p>
          <p className="mt-2 text-lg font-medium text-neutral-900 dark:text-white">
            Toshkent, O&apos;zbekiston
          </p>
        </div>
      </div>
    </div>
  );
}
