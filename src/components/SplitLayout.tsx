import { useCallback, useRef, useState, type ReactNode } from "react";
import { readJSON, writeJSON } from "../lib/storage";

/** "row" puts the panes side by side, "column" stacks them. */
type Direction = "row" | "column";

type SplitLayoutProps = {
  /** First pane: the left one in a row, the top one in a column. */
  left: ReactNode;
  /** Second pane: the right one in a row, the bottom one in a column. */
  right: ReactNode;
  /** Where the stored ratio lives, so the choice survives reloads. */
  storageKey: string;
  direction?: Direction;
  /** What the divider resizes, read out by screen readers. */
  label: string;
};

/** Travel limits and the reset position, per axis. */
const LIMITS: Record<Direction, { min: number; max: number; home: number }> = {
  row: { min: 0.22, max: 0.7, home: 0.38 },
  column: { min: 0.25, max: 0.8, home: 0.6 },
};

const STEP = 0.02;

/**
 * Two panes with a draggable divider between them.
 *
 * The ratio is published as a CSS custom property rather than an inline
 * grid-template — inline styles beat media queries, and the narrow-screen
 * layout needs to be able to stack these panes regardless of the ratio.
 */
export function SplitLayout({
  left,
  right,
  storageKey,
  direction = "row",
  label,
}: SplitLayoutProps) {
  const limits = LIMITS[direction];
  const container = useRef<HTMLDivElement>(null);

  const clamp = useCallback(
    (ratio: number) => Math.min(limits.max, Math.max(limits.min, ratio)),
    [limits],
  );

  const [ratio, setRatio] = useState(() => clamp(readJSON(storageKey, limits.home)));
  const [dragging, setDragging] = useState(false);

  const commit = useCallback(
    (next: number) => {
      const clamped = clamp(next);
      setRatio(clamped);
      writeJSON(storageKey, clamped);
    },
    [clamp, storageKey],
  );

  const ratioFromEvent = (clientX: number, clientY: number) => {
    const bounds = container.current?.getBoundingClientRect();
    if (!bounds) return null;
    if (direction === "row") {
      if (bounds.width === 0) return null;
      return (clientX - bounds.left) / bounds.width;
    }
    if (bounds.height === 0) return null;
    return (clientY - bounds.top) / bounds.height;
  };

  // The two arrow keys that move the divider along its own axis.
  const [shrink, grow] =
    direction === "row" ? ["ArrowLeft", "ArrowRight"] : ["ArrowUp", "ArrowDown"];

  return (
    <div
      className={`split split-${direction} ${dragging ? "split-dragging" : ""}`}
      ref={container}
      style={{ "--split": `${(ratio * 100).toFixed(2)}%` } as React.CSSProperties}
    >
      {left}

      <div
        className="split-handle"
        role="separator"
        aria-orientation={direction === "row" ? "vertical" : "horizontal"}
        aria-label={label}
        aria-valuenow={Math.round(ratio * 100)}
        aria-valuemin={Math.round(limits.min * 100)}
        aria-valuemax={Math.round(limits.max * 100)}
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
          const next = ratioFromEvent(event.clientX, event.clientY);
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
          if (event.key === shrink) commit(ratio - STEP);
          else if (event.key === grow) commit(ratio + STEP);
          else if (event.key === "Home") commit(limits.home);
          else return;
          event.preventDefault();
        }}
        onDoubleClick={() => commit(limits.home)}
      />

      {right}
    </div>
  );
}
