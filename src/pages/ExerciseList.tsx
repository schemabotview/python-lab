import { useEffect } from "react";
import { Link } from "react-router-dom";
import { exercises, tracks } from "../exercises";
import { prewarmPython } from "../hooks/usePythonRunner";
import { resetProgress, useProgress } from "../lib/progress";

export function ExerciseList() {
  const progress = useProgress();
  const completedCount = exercises.filter((exercise) => progress[exercise.id]).length;

  // Start the interpreter while the student is choosing, so Run is instant.
  useEffect(() => prewarmPython(), []);

  return (
    <div className="idx">
      {/* Same shape as a concept app's index: the GraphL eyebrow is the link back to the root
          catalog, then this repo's subject. Kept identical so the catalog, the courses and the
          labs read as one system. */}
      <header className="idx__head">
        <a className="idx__brand" href="/">
          GraphL
        </a>
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
  );
}
