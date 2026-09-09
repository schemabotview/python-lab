import { useEffect, useRef, useState } from "react";
import type { OutputChunk, RunOutcome, TestResult } from "../runtime/protocol";
import type { RunnerStatus } from "../runtime/pythonRunner";

type OutputPanelProps = {
  lines: OutputChunk[];
  droppedLines: number;
  outcome: RunOutcome | null;
  status: RunnerStatus;
  onClear: () => void;
};

type Tab = "output" | "tests";

function summary(outcome: RunOutcome | null, status: RunnerStatus) {
  if (status === "running") return { text: "Running…", tone: "muted" as const };
  if (!outcome) return null;
  switch (outcome.status) {
    case "ok":
      return { text: `Finished in ${outcome.durationMs.toFixed(0)} ms`, tone: "ok" as const };
    case "error":
      return { text: outcome.message, tone: "error" as const };
    case "timeout":
      return { text: `Stopped after ${outcome.limitMs / 1000}s`, tone: "error" as const };
    case "stopped":
      return { text: "Stopped", tone: "muted" as const };
  }
}

const MARKS: Record<TestResult["status"], string> = {
  pass: "✓",
  fail: "✗",
  error: "!",
};

function TestList({ results }: { results: TestResult[] }) {
  const passed = results.filter((result) => result.status === "pass").length;
  const allPassed = passed === results.length;

  return (
    <div className="tests">
      <p className={`tests-headline ${allPassed ? "tests-pass" : "tests-fail"}`}>
        {allPassed
          ? `All ${results.length} tests passed — nice work.`
          : `${passed} of ${results.length} tests passing`}
      </p>

      <ul className="test-list">
        {results.map((result, index) => (
          <li key={index} className={`test test-${result.status}`}>
            <span className="test-mark" aria-hidden="true">
              {MARKS[result.status]}
            </span>
            <span className="test-body">
              <span className="test-name">{result.name}</span>
              {result.detail && <span className="test-detail">{result.detail}</span>}
              <code className="test-source">{result.source}</code>
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}

export function OutputPanel({
  lines,
  droppedLines,
  outcome,
  status,
  onClear,
}: OutputPanelProps) {
  const body = useRef<HTMLDivElement>(null);
  const pinned = useRef(true);
  const [tab, setTab] = useState<Tab>("output");
  const [shownOutcome, setShownOutcome] = useState(outcome);

  const results = outcome?.status === "ok" ? outcome.tests : undefined;

  // Show the student what they just asked for: grading results after a graded
  // run, console output after a plain one. Adjusting during render rather than
  // in an effect — the switch is caused by a finished run, and this way the
  // panel never paints on the wrong tab first. A manual tab choice afterwards
  // survives, because this only fires when a new outcome arrives.
  if (outcome !== shownOutcome) {
    setShownOutcome(outcome);
    if (outcome) setTab(results ? "tests" : "output");
  }

  // Follow the tail while the user is at the bottom, but don't yank the view
  // away if they've scrolled up to read something.
  useEffect(() => {
    const element = body.current;
    if (element && pinned.current && tab === "output") {
      element.scrollTop = element.scrollHeight;
    }
  }, [lines, outcome, tab]);

  const status_ = summary(outcome, status);
  const isEmpty = lines.length === 0 && !outcome && status !== "running";

  return (
    <section className="panel output-panel">
      <header className="panel-head">
        <div className="tabs" role="tablist">
          <button
            role="tab"
            aria-selected={tab === "output"}
            className={`tab ${tab === "output" ? "tab-active" : ""}`}
            onClick={() => setTab("output")}
          >
            Output
          </button>
          <button
            role="tab"
            aria-selected={tab === "tests"}
            className={`tab ${tab === "tests" ? "tab-active" : ""}`}
            onClick={() => setTab("tests")}
          >
            Tests
            {results && (
              <span className="tab-count">
                {results.filter((r) => r.status === "pass").length}/{results.length}
              </span>
            )}
          </button>
        </div>

        {status_ && <span className={`summary summary-${status_.tone}`}>{status_.text}</span>}
        <button className="link" onClick={onClear} disabled={isEmpty}>
          Clear
        </button>
      </header>

      <div
        className="panel-body console"
        ref={body}
        onScroll={(event) => {
          const el = event.currentTarget;
          pinned.current = el.scrollHeight - el.scrollTop - el.clientHeight < 24;
        }}
      >
        {tab === "tests" ? (
          results ? (
            <TestList results={results} />
          ) : (
            <p className="placeholder">
              Run the tests to check your solution against the requirement.
            </p>
          )
        ) : (
          <>
            {isEmpty && <p className="placeholder">Run your code to see its output here.</p>}

            {droppedLines > 0 && (
              <div className="notice">…{droppedLines} earlier lines hidden</div>
            )}

            {lines.map((line, index) => (
              <div key={index} className={`line line-${line.stream}`}>
                {line.text || " "}
              </div>
            ))}

            {outcome?.status === "error" && (
              <pre className="traceback">{outcome.traceback ?? outcome.message}</pre>
            )}

            {outcome?.status === "timeout" && (
              <div className="notice notice-error">
                Your program ran longer than {outcome.limitMs / 1000} seconds and was stopped.
                Check for a loop that never ends. The Python runtime has been restarted.
              </div>
            )}

            {outcome?.status === "stopped" && (
              <div className="notice">Run cancelled. The Python runtime has been restarted.</div>
            )}
          </>
        )}
      </div>
    </section>
  );
}
