import { useState } from "react";
import { Link, useParams } from "react-router-dom";
import { Editor } from "../components/Editor";
import { OutputPanel } from "../components/OutputPanel";
import { Prompt } from "../components/Prompt";
import { SplitLayout } from "../components/SplitLayout";
import { getExercise } from "../exercises";
import { clearDraft, getDraft, saveDraft } from "../lib/drafts";
import { markCompleted, useProgress } from "../lib/progress";
import { usePythonRunner } from "../hooks/usePythonRunner";

export function ExerciseView() {
  const { id } = useParams();
  const exercise = getExercise(id);
  const py = usePythonRunner();
  const progress = useProgress();

  const [code, setCode] = useState(() =>
    exercise ? (getDraft(exercise.id) ?? exercise.starter) : "",
  );
  // Bumped on reset so the editor knows to replace its document; ordinary
  // typing must not trigger that path.
  const [resetNonce, setResetNonce] = useState(0);

  if (!exercise) {
    return (
      <div className="page">
        <p className="empty">
          No exercise called “{id}”. <Link to="/">Back to the list</Link>.
        </p>
      </div>
    );
  }

  const updateCode = (next: string) => {
    setCode(next);
    saveDraft(exercise.id, next);
  };

  const reset = () => {
    clearDraft(exercise.id);
    setCode(exercise.starter);
    setResetNonce((n) => n + 1);
  };

  const handleRun = () => void py.run(code);

  const handleRunTests = async () => {
    const outcome = await py.run(code, exercise.tests);
    const results = outcome.status === "ok" ? outcome.tests : undefined;
    if (results?.length && results.every((result) => result.status === "pass")) {
      markCompleted(exercise.id);
    }
  };

  const busy = py.status === "running";
  const booting = py.status === "booting" || py.status === "idle";
  const completed = Boolean(progress[exercise.id]);

  return (
    <div className="app">
      <SplitLayout
        storageKey="python-lab:split"
        left={
          <section className="panel prompt-panel">
            <header className="panel-head">
              <Link className="back" to="/">
                ← Exercises
              </Link>
              <div className="head-right">
                <span className={`pill pill-${exercise.difficulty}`}>
                  {exercise.difficulty}
                </span>
                {completed && <span className="pill pill-done">✓ completed</span>}
              </div>
            </header>
            <div className="panel-body">
              <Prompt markdown={exercise.prompt} />
            </div>
          </section>
        }
        right={
          <div className="workspace">
            <section className="panel editor-panel">
              <header className="panel-head">
                <h2>solution.py</h2>
              </header>
              <div className="panel-body">
                <Editor
                  value={code}
                  onChange={updateCode}
                  onRun={handleRun}
                  onRunTests={() => void handleRunTests()}
                  documentKey={`${exercise.id}:${resetNonce}`}
                />
              </div>

              <footer className="panel-foot">
                {/* The status sits beside the buttons it explains: while the
                    runtime boots, Run is disabled and this says why. */}
                <span className={`badge badge-${py.status}`}>
                  {py.bootError
                    ? "Runtime failed to load"
                    : booting
                      ? "Starting Python…"
                      : busy
                        ? "Running"
                        : `Python ${py.version ?? ""}`}
                </span>

                <div className="toolbar">
                  <button className="link" onClick={reset} disabled={code === exercise.starter}>
                    Reset
                  </button>
                  {busy ? (
                    <button className="danger" onClick={py.stop}>
                      Stop
                    </button>
                  ) : (
                    <>
                      <button className="secondary" onClick={handleRun} disabled={booting}>
                        Run <kbd>⌘↵</kbd>
                      </button>
                      <button onClick={() => void handleRunTests()} disabled={booting}>
                        Run tests <kbd>⇧⌘↵</kbd>
                      </button>
                    </>
                  )}
                </div>
              </footer>
            </section>

            <OutputPanel
              lines={py.lines}
              droppedLines={py.droppedLines}
              outcome={py.outcome}
              status={py.status}
              onClear={py.clear}
            />
          </div>
        }
      />

      {py.bootError && (
        <p className="boot-error">Could not start the Python runtime: {py.bootError}</p>
      )}
    </div>
  );
}
