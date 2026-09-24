import { useEffect } from "react";
import { Link } from "react-router-dom";
import { SiteHeader } from "../components/SiteHeader";
import { ThemeToggle } from "../components/ThemeToggle";
import { useTheme } from "../lib/theme";
import { exercises, tracks } from "../exercises";
import { prewarmPython } from "../hooks/usePythonRunner";
import { resetProgress, useProgress } from "../lib/progress";

export function ExerciseList() {
  const { theme, toggle } = useTheme();
  const progress = useProgress();
  const completedCount = exercises.filter((exercise) => progress[exercise.id]).length;

  // Start the interpreter while the student is choosing, so Run is instant.
  useEffect(() => prewarmPython(), []);

  return (
    // The bar is a SIBLING of .idx, not a child: it is full-bleed (its rule spans the viewport)
    // while .idx is a 940px centred column. Both use the same width and gutters, so the brand
    // lines up with the cards below it.
    <>
      <SiteHeader actions={<ThemeToggle theme={theme} onToggle={toggle} />} />
      <div className="idx">
        {/* Same shape as a concept app's index: the GraphL wordmark used to be an eyebrow here and
            is in the bar above now; what stays is this repo's subject. Kept identical so the
            catalog, the courses and the labs read as one system. */}
        <header className="idx__head">
          <h1 className="idx__subject">Python Lab</h1>
          <p className="idx__progress">
            <span>
              {completedCount} of {exercises.length} completed
            </span>
            {completedCount > 0 && (
              <button className="link" onClick={resetProgress}>
                Reset progress
              </button>
            )}
          </p>
        </header>

        {tracks.map((track) => (
          <section key={track.id} className="idx__track">
            <h2 className="idx__track-label">{track.label}</h2>
            <ol className="idx__grid">
              {track.exercises.map((exercise) => (
                <li key={exercise.id} className="idx-card">
                  <Link className="idx-card__link" to={`/exercise/${exercise.id}`}>
                    {/* Numbered by position in the whole lab, not within the track, so the
                        number is a stable name for an exercise however the tracks are cut. */}
                    <span className="idx-card__num">
                      {String(exercises.indexOf(exercise) + 1).padStart(2, "0")}
                    </span>
                    <span className="idx-card__body">
                      <span className="idx-card__row">
                        <span className="idx-card__title">{exercise.title}</span>
                        <span className={`pill pill-${exercise.difficulty}`}>
                          {exercise.difficulty}
                        </span>
                        {progress[exercise.id] && <span className="card-done">✓ completed</span>}
                      </span>
                      <span className="idx-card__summary">{exercise.summary}</span>
                      <span className="card-tags">
                        {exercise.tags.map((tag) => (
                          <span key={tag} className="tag">
                            {tag}
                          </span>
                        ))}
                      </span>
                    </span>
                    <span className="idx-card__arrow" aria-hidden="true">
                      →
                    </span>
                  </Link>
                </li>
              ))}
            </ol>
          </section>
        ))}
      </div>
    </>
  );
}
