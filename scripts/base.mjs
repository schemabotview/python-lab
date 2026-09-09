/**
 * Where the app is served in production.
 *
 * The GraphL catalog (graphl.in) links each site at `/<slug>/`, and the slug is
 * the repo name — so this must match `schemabotview/python-lab`. Dev stays at "/".
 *
 * Read by vite.config.ts (asset URLs) and scripts/copy-pyodide.mjs (the service
 * worker's runtime path). One definition, so the two can never disagree.
 */
export const BASE_PATH = "/python-lab/";
