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

/**
 * Which track an exercise belongs to. These mirror the course arc of the
 * `python` concept app — every section a student can watch has one exercise
 * here — plus "algorithms" for the interview-style set, which teaches no
 * particular section.
 */
export type TopicId = "syntax" | "data" | "oop" | "idioms" | "stdlib" | "capstone" | "algorithms";

/** Track headings, in the order they appear on the index. */
export const TRACKS: { id: TopicId; label: string }[] = [
  { id: "syntax", label: "Core syntax" },
  { id: "data", label: "Data structures" },
  { id: "oop", label: "Objects & classes" },
  { id: "idioms", label: "Pythonic idioms" },
  { id: "stdlib", label: "Files, I/O & stdlib" },
  { id: "capstone", label: "Capstone" },
  { id: "algorithms", label: "Algorithms" },
];

export type ExerciseMeta = {
  title: string;
  difficulty: Difficulty;
  topic: TopicId;
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

/**
 * The index groups by track. A track with nothing in it is dropped rather than
 * rendered as an empty heading, and an exercise whose topic is not in TRACKS
 * still appears — under a heading of its own name, so a typo is visible on the
 * page instead of silently hiding the exercise.
 */
export const tracks = (() => {
  const known = new Set(TRACKS.map((track) => track.id));
  const extra = [...new Set(exercises.map((e) => e.topic).filter((id) => !known.has(id)))];
  return [...TRACKS, ...extra.map((id) => ({ id, label: id }))]
    .map((track) => ({ ...track, exercises: exercises.filter((e) => e.topic === track.id) }))
    .filter((track) => track.exercises.length > 0);
})();

const byId = new Map(exercises.map((exercise) => [exercise.id, exercise]));

export function getExercise(id: string | undefined): Exercise | undefined {
  return id ? byId.get(id) : undefined;
}
