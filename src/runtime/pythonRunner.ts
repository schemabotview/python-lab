import type { OutputChunk, RunOutcome, WorkerRequest, WorkerResponse } from "./protocol";

export type RunnerStatus = "idle" | "booting" | "ready" | "running";

export type RunOptions = {
  onOutput?: (chunk: OutputChunk) => void;
  timeoutMs?: number;
  /** When present the run is graded against this test source. */
  tests?: string;
};

const DEFAULT_TIMEOUT_MS = 5_000;

/**
 * Main-thread handle on the Python worker.
 *
 * Pyodide blocks its thread while executing, so a runaway loop in student code
 * is only recoverable by killing the worker outright. Every run is therefore
 * raced against a timeout; on expiry we terminate and boot a replacement.
 */
export class PythonRunner {
  private worker: Worker | null = null;
  private nextId = 1;
  private pending: ((response: WorkerResponse) => void) | null = null;
  private bootPromise: Promise<string> | null = null;
  private active: { resolve: (outcome: RunOutcome) => void; timer: ReturnType<typeof setTimeout> } | null =
    null;

  status: RunnerStatus = "idle";
  onStatusChange?: (status: RunnerStatus) => void;

  private setStatus(status: RunnerStatus) {
    this.status = status;
    this.onStatusChange?.(status);
  }

  private spawn() {
    const worker = new Worker(new URL("./worker.ts", import.meta.url), { type: "module" });
    worker.onmessage = (event: MessageEvent<WorkerResponse>) => this.pending?.(event.data);
    this.worker = worker;
    return worker;
  }

  private send(request: WorkerRequest) {
    this.worker?.postMessage(request);
  }

  /** Boots the interpreter. Safe to call repeatedly; the first call wins. */
  boot(): Promise<string> {
    if (this.bootPromise) return this.bootPromise;

    this.setStatus("booting");
    this.bootPromise = new Promise<string>((resolve, reject) => {
      const worker = this.spawn();
      const id = this.nextId++;

      worker.onerror = (event) => reject(new Error(event.message || "Worker failed to start"));
      this.pending = (response) => {
        if (response.id !== id) return;
        this.pending = null;
        if (response.type === "ready") {
          this.setStatus("ready");
          resolve(response.pythonVersion);
        } else if (response.type === "error") {
          this.setStatus("idle");
          reject(new Error(response.message));
        }
      };

      this.send({ type: "init", id });
    });

    return this.bootPromise;
  }

  async run(code: string, options: RunOptions = {}): Promise<RunOutcome> {
    const { onOutput, timeoutMs = DEFAULT_TIMEOUT_MS, tests } = options;

    await this.boot();
    if (this.status === "running") {
      return { status: "error", message: "A program is already running." };
    }
    this.setStatus("running");

    const id = this.nextId++;

    const outcome = await new Promise<RunOutcome>((resolve) => {
      const timer = setTimeout(() => {
        this.abort({ status: "timeout", limitMs: timeoutMs });
      }, timeoutMs);

      this.active = { resolve, timer };

      this.pending = (response) => {
        if (response.id !== id) return;
        switch (response.type) {
          case "output":
            onOutput?.(response.chunk);
            return;
          case "result":
            this.settle({
              status: "ok",
              durationMs: response.durationMs,
              tests: response.tests,
            });
            return;
          case "error":
            this.settle({
              status: "error",
              message: response.message,
              traceback: response.traceback,
            });
            return;
        }
      };

      this.send({ type: "run", id, code, tests });
    });

    return outcome;
  }

  /** Resolves the awaiting caller without touching interpreter state. */
  private resolveActive(outcome: RunOutcome) {
    const active = this.active;
    if (!active) return false;
    this.active = null;
    this.pending = null;
    clearTimeout(active.timer);
    active.resolve(outcome);
    return true;
  }

  /** The run ended on its own; the interpreter is still healthy. */
  private settle(outcome: RunOutcome) {
    if (this.resolveActive(outcome)) this.setStatus("ready");
  }

  /**
   * The run has to be killed — a hung loop won't yield the thread, so the only
   * way out is terminating the worker and booting a replacement.
   */
  private abort(outcome: RunOutcome) {
    if (this.resolveActive(outcome)) void this.restart();
  }

  /** User-initiated cancel. No-op when nothing is running. */
  stop() {
    this.abort({ status: "stopped" });
  }

  /** Kills the current interpreter and boots a clean one. */
  restart(): Promise<string> {
    this.resolveActive({ status: "stopped" });
    this.worker?.terminate();
    this.worker = null;
    this.pending = null;
    this.bootPromise = null;
    this.setStatus("idle");
    return this.boot();
  }

  dispose() {
    this.resolveActive({ status: "stopped" });
    this.worker?.terminate();
    this.worker = null;
    this.pending = null;
    this.bootPromise = null;
    this.setStatus("idle");
  }
}
