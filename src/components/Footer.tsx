export default function Footer() {
  return (
    <footer className="mt-16 border-t border-black/10 bg-neutral-50 dark:border-white/10 dark:bg-neutral-900">
      <div className="mx-auto max-w-6xl px-4 py-10 text-sm text-neutral-600 dark:text-neutral-400">
        <div className="grid gap-8 sm:grid-cols-3">
          <div>
            <p className="text-base font-bold text-teal-700 dark:text-teal-400">Sayyoh.uz</p>
            <p className="mt-2">O&apos;zbekiston bo&apos;ylab unutilmas sayohatlar tashkilotchisi.</p>
          </div>
          <div>
            <p className="font-semibold text-neutral-900 dark:text-white">Aloqa</p>
            <p className="mt-2">Tel: +998 90 123 45 67</p>
            <p>Email: info@sayyoh.uz</p>
            <p>Toshkent, O&apos;zbekiston</p>
          </div>
          <div>
            <p className="font-semibold text-neutral-900 dark:text-white">Ish vaqti</p>
            <p className="mt-2">Dushanba - Shanba: 09:00 - 18:00</p>
            <p>Yakshanba: dam olish kuni</p>
          </div>
        </div>
        <p className="mt-8 border-t border-black/10 pt-6 text-xs dark:border-white/10">
          © {new Date().getFullYear()} Sayyoh.uz. Barcha huquqlar himoyalangan.
        </p>
      </div>
    </footer>
  );
}
