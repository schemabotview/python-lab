/// <reference lib="webworker" />
import type { PyodideAPI, loadPyodide as LoadPyodide } from "pyodide";
import type { TestResult, WorkerRequest, WorkerResponse } from "./protocol";

// Pyodide is served from public/pyodide (see scripts/copy-pyodide.mjs). It must
// be loaded at runtime, not bundled, so it can resolve its .wasm and stdlib
// relative to indexURL.
//
// BASE_URL — not a leading-slash literal — because the app deploys under
// graphl.in/python-lab/. Vite inlines this at build time, in worker bundles too.
// It always ends in "/".
const PYODIDE_BASE = `${import.meta.env.BASE_URL}pyodide/`;

/**
 * Executes student code, and optionally grades it against a test file.
 *
 * Tests are split into individual top-level statements so each assertion can be
 * reported separately — one red line the student can act on, rather than a
 * whole file that either passed or didn't.
 */
const BOOTSTRAP = `
import ast, contextlib, io, json, linecache, sys, traceback

USER_FILE = "<exercise>"
TESTS_FILE = "<tests>"

def _register(filename, source):
    # Without this, traceback can't resolve a synthetic filename and prints
    # frames with no source line or caret anchors.
    linecache.cache[filename] = (
        len(source),
        None,
        source.splitlines(keepends=True),
        filename,
    )

def _trimmed_traceback(*files):
    etype, value, tb = sys.exc_info()
    # Walk past our own frames so the first line the student sees is their code.
    while tb is not None and tb.tb_frame.f_code.co_filename not in files:
        tb = tb.tb_next
    return "".join(traceback.format_exception(etype, value, tb))

def _exec_user(source):
    """Run the student's code. Returns (namespace, traceback or None)."""
    namespace = {"__name__": "__main__", "__file__": USER_FILE}
    _register(USER_FILE, source)
    try:
        compiled = compile(source, USER_FILE, "exec")
    except SyntaxError:
        return namespace, _trimmed_traceback(USER_FILE)
    try:
        exec(compiled, namespace)
    except SystemExit:
        pass
    except BaseException:
        return namespace, _trimmed_traceback(USER_FILE)
    finally:
        sys.stdout.flush()
        sys.stderr.flush()
    return namespace, None

def _run_user_code(source):
    return _exec_user(source)[1]

def _describe(node, source):
    segment = (ast.get_source_segment(source, node) or "").strip()
    # A message on the assert reads better than its expression, so prefer it.
    if (
        isinstance(node, ast.Assert)
        and isinstance(node.msg, ast.Constant)
        and isinstance(node.msg.value, str)
    ):
        return node.msg.value, segment
    return segment, segment

def _brief(value):
    text = repr(value)
    return text if len(text) <= 200 else text[:197] + "..."

def _comparison_detail(node, namespace):
    """For an equality assert, report what the code actually produced.

    Plain asserts only say that something was false, which leaves a beginner
    guessing. Re-evaluating both sides costs one extra call and turns that into
    "got X, expected Y". Output is swallowed so the re-run can't duplicate the
    student's prints, and any failure here just means no extra detail.
    """
    test = node.test if isinstance(node, ast.Assert) else None
    if not isinstance(test, ast.Compare) or len(test.ops) != 1:
        return None
    if not isinstance(test.ops[0], (ast.Eq, ast.Is)):
        return None
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            actual = eval(compile(ast.Expression(test.left), TESTS_FILE, "eval"), namespace)
            expected = eval(
                compile(ast.Expression(test.comparators[0]), TESTS_FILE, "eval"), namespace
            )
    except BaseException:
        return None
    return "got {}, expected {}".format(_brief(actual), _brief(expected))

def _run_tests(user_source, tests_source):
    namespace, failure = _exec_user(user_source)
    if failure is not None:
        return json.dumps({"error": failure})

    _register(TESTS_FILE, tests_source)
    try:
        tree = ast.parse(tests_source, TESTS_FILE)
    except SyntaxError:
        return json.dumps({"error": _trimmed_traceback(TESTS_FILE)})

    results = []
    for node in tree.body:
        name, segment = _describe(node, tests_source)
        # Compiling one node at a time keeps the original line numbers, so a
        # traceback still points into the real test file.
        module = ast.Module(body=[node], type_ignores=[])
        try:
            exec(compile(module, TESTS_FILE, "exec"), namespace)
        except AssertionError as exc:
            detail = _comparison_detail(node, namespace)
            if detail is None:
                # The assert's own message is already the headline; only keep it
                # here when it says something the headline doesn't.
                message = str(exc)
                detail = message if message and message != name else None
            entry = {"status": "fail", "name": name, "source": segment}
            if detail:
                entry["detail"] = detail
            results.append(entry)
        except BaseException:
            results.append({
                "status": "error",
                "name": name,
                "source": segment,
                "detail": _trimmed_traceback(USER_FILE, TESTS_FILE),
            })
        else:
            # Non-assert statements are setup, not assertions worth reporting.
            if isinstance(node, ast.Assert):
                results.append({"status": "pass", "name": name, "source": segment})
        finally:
            sys.stdout.flush()
            sys.stderr.flush()

    return json.dumps({"results": results})
`;

let pyodide: PyodideAPI | null = null;
let runUserCode: ((source: string) => string | null) | null = null;
let runTests: ((source: string, tests: string) => string) | null = null;

function post(message: WorkerResponse) {
  self.postMessage(message);
}

async function init(id: number) {
  const { loadPyodide } = (await import(
    /* @vite-ignore */ `${PYODIDE_BASE}pyodide.mjs`
  )) as { loadPyodide: typeof LoadPyodide };

  pyodide = await loadPyodide({ indexURL: PYODIDE_BASE });
  pyodide.runPython(BOOTSTRAP);
  runUserCode = pyodide.globals.get("_run_user_code");
  runTests = pyodide.globals.get("_run_tests");

  post({
    type: "ready",
    id,
    pythonVersion: pyodide.runPython("__import__('sys').version.split()[0]"),
  });
}

function run(id: number, code: string, tests?: string) {
  if (!pyodide || !runUserCode || !runTests) {
    post({ type: "error", id, message: "Python runtime is not ready yet." });
    return;
  }

  // Rebind per run: the callbacks close over this run's id so late output from
  // a terminated run can never be attributed to the next one.
  pyodide.setStdout({
    batched: (text) => post({ type: "output", id, chunk: { stream: "stdout", text } }),
  });
  pyodide.setStderr({
    batched: (text) => post({ type: "output", id, chunk: { stream: "stderr", text } }),
  });

  const startedAt = performance.now();
  let traceback: string | null = null;
  let results: TestResult[] | undefined;

  try {
    if (tests === undefined) {
      traceback = runUserCode(code);
    } else {
      const outcome = JSON.parse(runTests(code, tests)) as {
        error?: string;
        results?: TestResult[];
      };
      traceback = outcome.error ?? null;
      results = outcome.results;
    }
  } catch (err) {
    // A failure here is the runtime itself breaking, not the student's code.
    post({ type: "error", id, message: err instanceof Error ? err.message : String(err) });
    return;
  }

  const durationMs = performance.now() - startedAt;

  if (traceback) {
    post({
      type: "error",
      id,
      message: traceback.trimEnd().split("\n").at(-1) ?? "Error",
      traceback,
    });
    return;
  }
  post({ type: "result", id, durationMs, tests: results });
}

self.onmessage = async (event: MessageEvent<WorkerRequest>) => {
  const request = event.data;
  try {
    if (request.type === "init") await init(request.id);
    else if (request.type === "run") run(request.id, request.code, request.tests);
  } catch (err) {
    post({
      type: "error",
      id: request.id,
      message: err instanceof Error ? err.message : String(err),
    });
  }
};
