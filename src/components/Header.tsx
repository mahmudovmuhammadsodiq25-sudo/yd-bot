import Link from "next/link";

const links = [
  { href: "/", label: "Bosh sahifa" },
  { href: "/tours", label: "Manzillar" },
  { href: "/blog", label: "Blog" },
  { href: "/contact", label: "Aloqa" },
];

export default function Header() {
  return (
    <header className="sticky top-0 z-50 border-b border-black/10 bg-white/90 backdrop-blur dark:border-white/10 dark:bg-neutral-950/90">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
        <Link href="/" className="flex items-center gap-2 text-xl font-bold tracking-tight text-teal-700 dark:text-teal-400">
          <span aria-hidden>🧭</span>
          Anklavtour
        </Link>
        <nav className="flex items-center gap-6 text-sm font-medium">
          {links.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="text-neutral-700 transition-colors hover:text-teal-700 dark:text-neutral-300 dark:hover:text-teal-400"
            >
              {link.label}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  );
}
