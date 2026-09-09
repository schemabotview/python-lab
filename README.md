# python-lab

Python coding exercises that run entirely in the browser. No backend, no
install — the interpreter is real CPython compiled to WebAssembly.

The hands-on half of the Python track: where the [`python`](../python) concept
app teaches with narrated diagrams, python-lab has you write and run the code.
Serves at **https://graphl.in/python-lab/**.

## Running it

```bash
npm install
npm run dev      # http://localhost:5173
npm run build    # production build into dist/
npm run preview  # serve the production build
```

`predev` and `prebuild` run `scripts/copy-pyodide.mjs` automatically, so the
runtime is always in place before the app starts.

## How it works

**The interpreter.** Pyodide (CPython 3.14) runs inside a Web Worker. It has to
be a worker: Pyodide blocks its thread while executing, so a student's runaway
loop would freeze the tab with no way back. Every run is raced against a 5s
timeout, and on expiry — or when the student hits Stop — the worker is
terminated and a fresh one boots.

**The runtime files are self-hosted, not loaded from a CDN.**
`scripts/copy-pyodide.mjs` copies them out of `node_modules` into
`public/pyodide/`, which is gitignored and regenerated on every dev/build run.
Pyodide resolves its `.wasm` and stdlib at runtime relative to `indexURL`, so
these files must not go through the bundler.

**Tracebacks.** Student code is compiled under a fixed filename and registered
with `linecache`, so tracebacks show real source lines and caret anchors.
Frames belonging to the runner itself are trimmed, leaving only the student's
own code.

**Grading.** `tests.py` is split with `ast.parse` and executed one statement at
a time, so each assertion reports separately. For equality assertions both
sides are re-evaluated (with output suppressed) to report `got X, expected Y`.

**Caching.** A generated service worker (`scripts/sw-template.js` →
`public/sw.js`) caches the ~13 MB runtime. Its cache name carries the Pyodide
version, so upgrading the package invalidates the old files automatically. The
first visit downloads the runtime; every visit after that is served from cache.

## Adding an exercise

Create a directory under `src/exercises/`:

```
src/exercises/my-exercise/
  meta.json     title, difficulty, order, summary, tags
  prompt.md     the requirement, rendered in the left pane
  starter.py    what the editor is pre-filled with
  tests.py      assertions, one per behaviour, each with a message
  solution.py   reference answer — never bundled
```

The loader picks it up automatically. Write each assertion with a message: it
becomes the test's name in the UI.

Indent exercise Python with **2 spaces**, matching the editor's `indentUnit`
(`src/components/Editor.tsx`). A starter indented differently from what the
editor inserts is jarring to type into. Note this departs from PEP 8's 4
spaces — it is a deliberate choice for the narrow editor pane.

Verify solutions against their tests before committing:

```bash
python3 - <<'PY'
import pathlib
for d in sorted(p for p in pathlib.Path("src/exercises").iterdir() if p.is_dir()):
    ns = {}
    exec((d / "solution.py").read_text(), ns)
    exec((d / "tests.py").read_text(), ns)
    print("PASS", d.name)
PY
```

## Things to know

- **`solution.py` never ships.** Only files named in `import.meta.glob`
  (`src/exercises/index.ts`) enter the bundle, and solutions aren't among them.
- **`tests.py` does ship**, because grading runs client-side — a determined
  student can read the assertions in devtools. Fine for a practice tool; the
  point to revisit if this ever needs to support real assessment.
- **Deployment needs an SPA fallback.** Routes like `/exercise/two-sum` must
  rewrite to `index.html`, or a refresh 404s. `vite dev` and `vite preview`
  already do this.
- **`input()` doesn't work.** Pyodide has no synchronous stdin. Exercises are
  written as functions the tests call, which sidesteps it entirely.
