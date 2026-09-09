import { readJSON, writeJSON } from "./storage";

/**
 * Work in progress, kept per exercise so navigating away and back — or closing
 * the tab — doesn't discard what the student has typed.
 */
const KEY = "code-lab:drafts";

type DraftMap = Record<string, string>;

let drafts: DraftMap = readJSON<DraftMap>(KEY, {});

export function getDraft(exerciseId: string): string | undefined {
  return drafts[exerciseId];
}

export function saveDraft(exerciseId: string, code: string) {
  drafts = { ...drafts, [exerciseId]: code };
  writeJSON(KEY, drafts);
}

export function clearDraft(exerciseId: string) {
  const { [exerciseId]: _removed, ...rest } = drafts;
  drafts = rest;
  writeJSON(KEY, drafts);
}
