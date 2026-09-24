// The PLATFORM theme contract, shared with graphl.in and the concept apps. ui-graphl/theme.js is the
// original; @graphlearning/shell/src/useTheme.ts is the second implementation; this is the THIRD, and
// the same rule applies as to the site bar it sits in — one design, three implementations, change one
// and change all three.
//
//   key      localStorage['graphl:theme']
//   values   'light' | 'dark' | absent
//   switch   data-theme on <html>; absent means "nothing chosen yet"
//
// Every GraphL app is same-origin under graphl.in, so a reader who picks light on the catalog or in a
// concept app walks into the lab already light, with nothing passed between them.
//
// WHY THIS IS HAND-PORTED rather than imported: @graphlearning/shell peers @graphlearning/flow, which
// would drag the react-flow engine into a lab that has no scenes. The same reason SiteHeader is a
// hand-port here. It is 40 lines; the engine is 500kB.
//
// SIMPLER THAN THE SHELL'S, in two ways that matter: a lab has no DECK, so there is no authored
// theme to defer to — the default is simply dark; and a lab is never captured, so there is no
// capture pin. What is left is: stored choice, or dark.

import { useCallback, useEffect, useState } from "react";

const KEY = "graphl:theme";

export type ThemeKey = "dark" | "light";

// localStorage throws in some privacy modes. A broken toggle must never take the page with it, so
// every access is guarded and the fallback is the default.
export function readTheme(): ThemeKey {
  try {
    return localStorage.getItem(KEY) === "light" ? "light" : "dark";
  } catch {
    return "dark";
  }
}

function writeTheme(theme: ThemeKey) {
  try {
    localStorage.setItem(KEY, theme);
  } catch {
    /* the choice will not survive a reload; everything else still works */
  }
}

/** Owns the reader's choice and keeps <html data-theme> in step. Two states, dark <-> light. */
export function useTheme() {
  const [theme, setTheme] = useState<ThemeKey>(readTheme);

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    // color-scheme drives the form controls, the scrollbars and the editor's own caret colour, none
    // of which any stylesheet here reaches. index.html sets it before first paint; this keeps it in
    // step afterwards.
    document.documentElement.style.colorScheme = theme;
  }, [theme]);

  // Another GraphL app on the same origin changed the choice — follow it, so the platform does not
  // disagree with itself between two tabs.
  useEffect(() => {
    const onStorage = (e: StorageEvent) => {
      if (e.key === KEY || e.key === null) setTheme(readTheme());
    };
    window.addEventListener("storage", onStorage);
    return () => window.removeEventListener("storage", onStorage);
  }, []);

  // Swapping must look instantaneous. Several elements carry a colour transition for hover, and
  // without suppressing them the ground flips at once while everything else cross-fades behind it —
  // the switch reads as a smear rather than a change. Two nested rAFs: the first runs before the
  // paint that applies the new colours, the second after it. Ported from ui-graphl's theme.js.
  const toggle = useCallback(() => {
    const next: ThemeKey = theme === "dark" ? "light" : "dark";
    writeTheme(next);
    const root = document.documentElement;
    root.classList.add("theme-swap");
    setTheme(next);
    requestAnimationFrame(() => requestAnimationFrame(() => root.classList.remove("theme-swap")));
  }, [theme]);

  return { theme, toggle };
}
