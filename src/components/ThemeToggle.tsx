// The theme control, for SiteHeader's `actions` slot. A PORT of ui-graphl's #theme button and the
// shell's ThemeToggle — same square icon, same glyphs, same "where you are AND what the press does"
// accessible name. Text glyphs rather than an icon library, exactly as the other two bars have them.

import type { ThemeKey } from "../lib/theme";

// The glyph shows where you ARE, not where the press goes — a toggle that previews its destination
// reads as already-switched at a glance.
const FACE: Record<ThemeKey, { glyph: string; label: string }> = {
  dark: { glyph: "☾", label: "Dark theme" },
  light: { glyph: "☀", label: "Light theme" },
};

export function ThemeToggle({ theme, onToggle }: { theme: ThemeKey; onToggle: () => void }) {
  const next: ThemeKey = theme === "dark" ? "light" : "dark";
  const label = `${FACE[theme].label}. Switch to ${FACE[next].label.toLowerCase()}.`;
  return (
    <button className="site__icon" type="button" onClick={onToggle} aria-label={label} title={label}>
      {FACE[theme].glyph}
    </button>
  );
}
