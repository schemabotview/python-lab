import { useCallback, useEffect, useRef, useState } from "react";
import { PythonRunner, type RunnerStatus } from "../runtime/pythonRunner";
import type { OutputChunk, RunOutcome } from "../runtime/protocol";

/** Beyond this the DOM cost outweighs any value in keeping older lines. */
const MAX_LINES = 2000;

// One interpreter per page session, outside React so StrictMode's dev remount
// doesn't tear down a 13 MB runtime and boot it again.
const runner = new PythonRunner();

/**
 * Starts the interpreter before anyone needs it — called from the exercise
 * list, so the 13 MB runtime is warm by the time a student opens an exercise
 * and reaches for Run.
 */
export function prewarmPython() {
  // Errors are surfaced by usePythonRunner once a component actually mounts.
  void runner.boot().catch(() => {});
}

export type PythonRunnerState = {
  status: RunnerStatus;
  version: string | null;
  lines: OutputChunk[];
  droppedLines: number;
  outcome: RunOutcome | null;
  bootError: string | null;
  run: (code: string, tests?: string) => Promise<RunOutcome>;
  stop: () => void;
  restart: () => void;
  clear: () => void;
};

export function usePythonRunner(): PythonRunnerState {
  const [status, setStatus] = useState<RunnerStatus>(runner.status);
  const [version, setVersion] = useState<string | null>(null);
  const [lines, setLines] = useState<OutputChunk[]>([]);
  const [droppedLines, setDroppedLines] = useState(0);
  const [outcome, setOutcome] = useState<RunOutcome | null>(null);
  const [bootError, setBootError] = useState<string | null>(null);

  // Output arrives one print() at a time. Rendering each one would put a tight
  // loop's worth of re-renders on the main thread, so coalesce per frame.
  const buffer = useRef<OutputChunk[]>([]);
  const frame = useRef<number | null>(null);
  const retained = useRef(0);
  const dropped = useRef(0);

  const flush = useCallback(() => {
    if (frame.current !== null) {
      cancelAnimationFrame(frame.current);
      frame.current = null;
    }
    if (buffer.current.length === 0) return;

    const incoming = buffer.current;
    buffer.current = [];

    // Work out the overflow here rather than inside the updater: React may
    // defer or re-run an updater, so it has to stay free of side effects.
    const overflow = Math.max(0, retained.current + incoming.length - MAX_LINES);
    retained.current = retained.current + incoming.length - overflow;
    if (overflow > 0) {
      dropped.current += overflow;
      setDroppedLines(dropped.current);
    }

    setLines((prev) => {
      const next = prev.concat(incoming);
      return overflow > 0 ? next.slice(overflow) : next;
    });
  }, []);

  const push = useCallback(
    (chunk: OutputChunk) => {
      buffer.current.push(chunk);
      if (frame.current === null) frame.current = requestAnimationFrame(flush);
    },
    [flush],
  );

  useEffect(() => {
    runner.onStatusChange = setStatus;
    runner.boot().then(setVersion, (err: Error) => setBootError(err.message));
    return () => {
      runner.onStatusChange = undefined;
    };
  }, []);

  const clear = useCallback(() => {
    buffer.current = [];
    retained.current = 0;
    dropped.current = 0;
    setLines([]);
    setDroppedLines(0);
    setOutcome(null);
  }, []);

  const run = useCallback(
    async (code: string, tests?: string) => {
      clear();
      const result = await runner.run(code, { onOutput: push, tests });
      // Drain anything still buffered so the final lines land before the
      // outcome banner that follows them.
      flush();
      setOutcome(result);
      return result;
    },
    [clear, flush, push],
  );

  const stop = useCallback(() => runner.stop(), []);

  const restart = useCallback(() => {
    clear();
    setBootError(null);
    runner.restart().then(setVersion, (err: Error) => setBootError(err.message));
  }, [clear]);

  return {
    status,
    version,
    lines,
    droppedLines,
    outcome,
    bootError,
    run,
    stop,
    restart,
    clear,
  };
}
