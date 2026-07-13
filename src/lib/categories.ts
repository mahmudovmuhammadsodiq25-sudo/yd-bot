export const CATEGORIES = [
  { value: "tur", label: "Sayohat turi", emoji: "🧳" },
  { value: "ziyoratgoh", label: "Ziyoratgoh", emoji: "🕌" },
  { value: "dam_olish", label: "Dam olish hududi", emoji: "🏞️" },
  { value: "davolanish", label: "Davolanish maskani", emoji: "💧" },
] as const;

export type CategoryValue = (typeof CATEGORIES)[number]["value"];

export function categoryLabel(value: string): string {
  return CATEGORIES.find((c) => c.value === value)?.label ?? value;
}

export function categoryEmoji(value: string): string {
  return CATEGORIES.find((c) => c.value === value)?.emoji ?? "📍";
}
