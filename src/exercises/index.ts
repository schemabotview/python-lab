/**
 * Content pipeline for the exercises in this folder.
 *
 * Each exercise is a directory holding meta.json, prompt.md, starter.py and
 * tests.py. Only the files globbed below reach the client bundle — solution.py
 * is deliberately absent, so reference solutions never ship. tests.py does
 * ship, because grading runs in the browser: a determined student can read the
 * assertions in devtools. That is an acceptable trade for a practice tool, and
 * the line to revisit if this ever needs to support real assessment.
 */

export type Difficulty = "easy" | "medium" | "hard";

export type ExerciseMeta = {
  title: string;
  difficulty: Difficulty;
  order: number;
  summary: string;
  tags: string[];
};

export type Exercise = ExerciseMeta & {
  id: string;
  prompt: string;
  starter: string;
  tests: string;
};

const metaFiles = import.meta.glob<ExerciseMeta>("./*/meta.json", {
  eager: true,
  import: "default",
});
const promptFiles = import.meta.glob<string>("./*/prompt.md", {
  eager: true,
  query: "?raw",
  import: "default",
});
const starterFiles = import.meta.glob<string>("./*/starter.py", {
  eager: true,
  query: "?raw",
  import: "default",
});
const testFiles = import.meta.glob<string>("./*/tests.py", {
  eager: true,
  query: "?raw",
  import: "default",
});

/** "./two-sum/meta.json" -> "two-sum" */
function idFromPath(path: string) {
  return path.split("/")[1];
}

function build(): Exercise[] {
  const exercises = Object.entries(metaFiles).map(([path, meta]) => {
    const id = idFromPath(path);
    const prompt = promptFiles[`./${id}/prompt.md`];
    const starter = starterFiles[`./${id}/starter.py`];
    const tests = testFiles[`./${id}/tests.py`];

    // Fail loudly at startup rather than rendering a half-empty exercise.
    if (prompt === undefined) throw new Error(`Exercise "${id}" is missing prompt.md`);
    if (starter === undefined) throw new Error(`Exercise "${id}" is missing starter.py`);
    if (tests === undefined) throw new Error(`Exercise "${id}" is missing tests.py`);

    return { ...meta, id, prompt, starter, tests };
  });

  return exercises.sort((a, b) => a.order - b.order || a.title.localeCompare(b.title));
}

export const exercises = build();

const byId = new Map(exercises.map((exercise) => [exercise.id, exercise]));

export function getExercise(id: string | undefined): Exercise | undefined {
  return id ? byId.get(id) : undefined;
}
