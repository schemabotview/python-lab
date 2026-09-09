/**
 * Thin localStorage wrapper. Storage can be unavailable or full (Safari private
 * browsing throws on write), and losing a draft is never worth crashing the app
 * over, so every access degrades to a no-op.
 */
export function readJSON<T>(key: string, fallback: T): T {
  try {
    const raw = localStorage.getItem(key);
    return raw === null ? fallback : (JSON.parse(raw) as T);
  } catch {
    return fallback;
  }
}

export function writeJSON(key: string, value: unknown) {
  try {
    localStorage.setItem(key, JSON.stringify(value));
  } catch {
    // Nothing useful to do — the session simply won't survive a reload.
  }
}
