import { useSyncExternalStore } from "react";
import { readJSON, writeJSON } from "./storage";

/**
 * Which exercises the student has passed. Stored locally — this is a practice
 * tool, not an assessment system, so there is no server to answer to.
 */
const KEY = "code-lab:progress";

export type Progress = Record<string, { completedAt: string }>;

let progress: Progress = readJSON<Progress>(KEY, {});

const listeners = new Set<() => void>();

function emit() {
  for (const listener of listeners) listener();
}

function subscribe(listener: () => void) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

export function markCompleted(exerciseId: string) {
  if (progress[exerciseId]) return;
  progress = { ...progress, [exerciseId]: { completedAt: new Date().toISOString() } };
  writeJSON(KEY, progress);
  emit();
}

export function resetProgress() {
  progress = {};
  writeJSON(KEY, progress);
  emit();
}

/** Subscribes a component to the progress store. */
export function useProgress(): Progress {
  return useSyncExternalStore(
    subscribe,
    () => progress,
    () => progress,
  );
}
