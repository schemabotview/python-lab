import { useCallback, useRef, useState, type ReactNode } from "react";
import { readJSON, writeJSON } from "../lib/storage";

type SplitLayoutProps = {
  left: ReactNode;
  right: ReactNode;
  /** Where the stored ratio lives, so the choice survives reloads. */
  storageKey: string;
};

const MIN = 0.22;
const MAX = 0.7;
const DEFAULT = 0.38;
const STEP = 0.02;

function clamp(ratio: number) {
  return Math.min(MAX, Math.max(MIN, ratio));
}

/**
 * Two panes with a draggable divider between them.
 *
 * The ratio is published as a CSS custom property rather than an inline
 * grid-template — inline styles beat media queries, and the narrow-screen
 * layout needs to be able to stack these panes regardless of the ratio.
 */
export function SplitLayout({ left, right, storageKey }: SplitLayoutProps) {
  const container = useRef<HTMLDivElement>(null);
  const [ratio, setRatio] = useState(() => clamp(readJSON(storageKey, DEFAULT)));
  const [dragging, setDragging] = useState(false);

  const commit = useCallback(
    (next: number) => {
      const clamped = clamp(next);
      setRatio(clamped);
      writeJSON(storageKey, clamped);
    },
    [storageKey],
  );

  const ratioFromEvent = (clientX: number) => {
    const bounds = container.current?.getBoundingClientRect();
    if (!bounds || bounds.width === 0) return null;
    return (clientX - bounds.left) / bounds.width;
  };

  return (
    <div
      className={`split ${dragging ? "split-dragging" : ""}`}
      ref={container}
      style={{ "--split": `${(ratio * 100).toFixed(2)}%` } as React.CSSProperties}
    >
      {left}

      <div
        className="split-handle"
        role="separator"
        aria-orientation="vertical"
        aria-label="Resize the requirement pane"
        aria-valuenow={Math.round(ratio * 100)}
        aria-valuemin={Math.round(MIN * 100)}
        aria-valuemax={Math.round(MAX * 100)}
        tabIndex={0}
        onPointerDown={(event) => {
          // Pointer capture keeps the drag alive when the cursor outruns the
          // handle. Not every pointer can be captured, and the drag still works
          // without it, so a failure here must not abort the gesture.
          try {
            event.currentTarget.setPointerCapture(event.pointerId);
          } catch {
            // no capture available; dragging continues while over the handle
          }
          setDragging(true);
        }}
        onPointerMove={(event) => {
          if (!dragging) return;
          // A release can go missing — the pointer is cancelled, the window
          // loses focus, or the button comes up outside the document. Without
          // this the handle stays armed and resizes on plain hover, so trust
          // the button state over our own flag.
          if (event.buttons === 0) {
            setDragging(false);
            return;
          }
          const next = ratioFromEvent(event.clientX);
          if (next !== null) commit(next);
        }}
        onPointerUp={(event) => {
          try {
            event.currentTarget.releasePointerCapture(event.pointerId);
          } catch {
            // nothing was captured
          }
          setDragging(false);
        }}
        onPointerCancel={() => setDragging(false)}
        onLostPointerCapture={() => setDragging(false)}
        onKeyDown={(event) => {
          if (event.key === "ArrowLeft") commit(ratio - STEP);
          else if (event.key === "ArrowRight") commit(ratio + STEP);
          else if (event.key === "Home") commit(DEFAULT);
          else return;
          event.preventDefault();
        }}
        onDoubleClick={() => commit(DEFAULT)}
      />

      {right}
    </div>
  );
}
