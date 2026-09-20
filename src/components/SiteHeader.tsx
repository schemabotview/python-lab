import type { ReactNode } from "react";

/**
 * Platform chrome — the bar that sits above every GraphL page: the root catalog at graphl.in, the
 * seven concept apps, and this lab. Brand on the left, section nav on the right. The point is that
 * it renders identically everywhere, so a reader crossing from the catalog into the lab never
 * feels they have left the site.
 *
 * THIS IS THE THIRD COPY. ui-graphl/index.html is the original (buildless vanilla),
 * @graphlearning/shell exports the second (SiteHeader.tsx + the .site* rules in its styles.css),
 * and this is the third. The lab cannot use the shell's: the shell would drag in the react-flow
 * engine as a peer for a lab that has no scenes, and its stylesheet re-declares .idx, .idx-card
 * and five more names this repo already owns with different markup — importing it would break the
 * exercise list. So: one design, three implementations. Change one, change all three.
 *
 * Where it renders is a rule, not a preference: the exercise LIST only. ExerciseView is the
 * working surface (its own full-height chrome, its own back link), the same way a concept app's
 * section view is a video frame and never carries this bar.
 */

// The nav, mirroring catalog.json's `kinds` at graphl.in. Duplicated rather than fetched — the
// catalog is a different origin at dev time and this list has been three items all year.
const KINDS = [
  { id: "courses", label: "Courses" },
  { id: "labs", label: "Labs" },
  { id: "coach", label: "Coach" },
];

// The mark, inlined rather than referenced as /icon.svg: this app builds with `base` set to its own
// subpath, so a relative src resolves somewhere else and an absolute one breaks `npm run dev`.
// 335 bytes of SVG has neither problem, and nothing to flash in.
function Mark() {
  return (
    <svg className="site__logo" width="28" height="28" viewBox="0 0 512 512" aria-hidden="true">
      <rect width="512" height="512" rx="80" fill="#e8804f" />
      <g fill="none" stroke="#ffffff" strokeWidth="58" strokeLinecap="butt" strokeLinejoin="miter">
        <path d="M 373 200 A 130 130 0 1 0 373 312" />
        <path d="M 283 312 L 373 312 L 373 410" />
      </g>
    </svg>
  );
}

export function SiteHeader({
  // Which nav item is "you are here" — a catalog.json `kind` id. This repo is listed there as
  // kind "labs", so that is the default and nothing passes it.
  kind = "labs",
  nav = KINDS,
  // Where the brand points: the root catalog. Absolute, because every GraphL app is served from a
  // subpath of the same origin.
  home = "/",
  // Right-hand slot — the theme toggle and the account control when they exist.
  actions,
}: {
  kind?: string;
  nav?: { id: string; label: string }[];
  home?: string;
  actions?: ReactNode;
}) {
  return (
    <header className="site">
      <div className="site__inner">
        <a className="site__brand" href={home}>
          <Mark />
          <span className="site__name">GraphL</span>
        </a>
        {/* Plain anchors, not react-router Links: these leave the app for another origin path, so
            routing them client-side would be wrong. Middle-click and copy-link come free. */}
        <nav className="site__nav" aria-label="Sections">
          {nav.map((k) => (
            <a
              key={k.id}
              className="site__link"
              href={`${home}#${k.id}`}
              {...(k.id === kind ? { "aria-current": "page" as const } : {})}
            >
              {k.label}
            </a>
          ))}
        </nav>
        <div className="site__actions">{actions}</div>
      </div>
    </header>
  );
}
