// Copies the Pyodide runtime out of node_modules into public/ so Vite serves it
// as a static asset. Pyodide resolves pyodide.asm.wasm / python_stdlib.zip at
// runtime relative to indexURL, so it must not go through the bundler.
import { cp, mkdir, readFile, readdir, rm, writeFile } from "node:fs/promises";
import { createRequire } from "node:module";
import { dirname, join } from "node:path";
import { BASE_PATH } from "./base.mjs";

const require = createRequire(import.meta.url);

// `--prod` mirrors vite's `base` for a production build; dev serves from root.
const base = process.argv.includes("--prod") ? BASE_PATH : "/";
const src = dirname(require.resolve("pyodide/package.json"));
const dest = join(process.cwd(), "public", "pyodide");

// Source maps and the bundled REPL pages are dead weight in the served build.
const skip = /\.map$|\.d\.ts$|^console.*\.html$|^README\.md$|^package\.json$/;

await rm(dest, { recursive: true, force: true });
await mkdir(dest, { recursive: true });

const entries = await readdir(src);
let copied = 0;
for (const name of entries) {
  if (skip.test(name)) continue;
  await cp(join(src, name), join(dest, name), { recursive: true });
  copied++;
}
console.log(`copy-pyodide: ${copied} entries -> public/pyodide`);

// Generate the service worker with this Pyodide version baked into its cache
// name, so an upgrade invalidates the previously cached runtime.
const { version } = JSON.parse(await readFile(require.resolve("pyodide/package.json"), "utf8"));
const template = await readFile(join(process.cwd(), "scripts", "sw-template.js"), "utf8");
await writeFile(
  join(process.cwd(), "public", "sw.js"),
  template.replaceAll("__PYODIDE_VERSION__", version).replaceAll("__BASE__", base),
);
console.log(`copy-pyodide: public/sw.js generated for pyodide ${version} at base ${base}`);
