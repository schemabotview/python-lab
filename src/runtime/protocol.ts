/** Messages exchanged between the main thread and the Python worker. */

export type OutputChunk = {
  stream: "stdout" | "stderr";
  text: string;
};

export type TestStatus = "pass" | "fail" | "error";

export type TestResult = {
  /** The assertion's message when it has one, otherwise its source. */
  name: string;
  source: string;
  status: TestStatus;
  detail?: string;
};

/** Main thread -> worker. */
export type WorkerRequest =
  | { type: "init"; id: number }
  /** `tests` turns the run into a graded one. */
  | { type: "run"; id: number; code: string; tests?: string };

/** Worker -> main thread. */
export type WorkerResponse =
  | { type: "ready"; id: number; pythonVersion: string }
  | { type: "output"; id: number; chunk: OutputChunk }
  | { type: "result"; id: number; durationMs: number; tests?: TestResult[] }
  | { type: "error"; id: number; message: string; traceback?: string };

export type RunOutcome =
  | { status: "ok"; durationMs: number; tests?: TestResult[] }
  | { status: "error"; message: string; traceback?: string }
  | { status: "timeout"; limitMs: number }
  | { status: "stopped" };
