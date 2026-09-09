import { useEffect } from "react";
import { Link } from "react-router-dom";
import { exercises } from "../exercises";
import { prewarmPython } from "../hooks/usePythonRunner";
import { resetProgress, useProgress } from "../lib/progress";

export function ExerciseList() {
  const progress = useProgress();
  const completedCount = exercises.filter((exercise) => progress[exercise.id]).length;

  // Start the interpreter while the student is choosing, so Run is instant.
  useEffect(() => prewarmPython(), []);

  return (
    <div className="page">
      <header className="page-head">
        <h1>Python Lab</h1>
        <p className="lede">
          Python exercises that run entirely in your browser — nothing to install.
        </p>
        <p className="progress-line">
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

      <ul className="exercise-list">
        {exercises.map((exercise) => (
          <li key={exercise.id}>
            <Link className="exercise-card" to={`/exercise/${exercise.id}`}>
              <span className="card-top">
                <span className="card-title">{exercise.title}</span>
                <span className={`pill pill-${exercise.difficulty}`}>
                  {exercise.difficulty}
                </span>
                {progress[exercise.id] && <span className="card-done">✓ completed</span>}
              </span>
              <span className="card-summary">{exercise.summary}</span>
              <span className="card-tags">
                {exercise.tags.map((tag) => (
                  <span key={tag} className="tag">
                    {tag}
                  </span>
                ))}
              </span>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
