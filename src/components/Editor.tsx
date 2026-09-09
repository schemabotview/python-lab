import { useEffect, useRef } from "react";
import { basicSetup } from "codemirror";
import { EditorState, Prec } from "@codemirror/state";
import { EditorView, keymap } from "@codemirror/view";
import { indentWithTab } from "@codemirror/commands";
import { indentUnit } from "@codemirror/language";
import { python } from "@codemirror/lang-python";
import { oneDark } from "@codemirror/theme-one-dark";

type EditorProps = {
  value: string;
  onChange: (value: string) => void;
  onRun: () => void;
  onRunTests: () => void;
  /** Resets the document when it changes — e.g. switching exercise or "reset to starter". */
  documentKey?: string;
};

const theme = EditorView.theme({
  "&": { height: "100%", fontSize: "13.5px" },
  ".cm-scroller": {
    fontFamily: "ui-monospace, SFMono-Regular, Menlo, monospace",
    lineHeight: "1.6",
  },
  "&.cm-focused": { outline: "none" },
});

export function Editor({ value, onChange, onRun, onRunTests, documentKey }: EditorProps) {
  const host = useRef<HTMLDivElement>(null);
  const view = useRef<EditorView | null>(null);
  // Keep the latest callbacks reachable from the long-lived keymap/listener,
  // which are installed once and would otherwise close over stale props.
  const latest = useRef({ onChange, onRun, onRunTests });
  useEffect(() => {
    latest.current = { onChange, onRun, onRunTests };
  });

  useEffect(() => {
    if (!host.current) return;

    const instance = new EditorView({
      parent: host.current,
      state: EditorState.create({
        doc: value,
        extensions: [
          // Outrank basicSetup so Mod-Enter isn't swallowed by a default binding.
          Prec.highest(
            keymap.of([
              {
                key: "Mod-Enter",
                run: () => {
                  latest.current.onRun();
                  return true;
                },
              },
              {
                key: "Shift-Mod-Enter",
                run: () => {
                  latest.current.onRunTests();
                  return true;
                },
              },
            ]),
          ),
          basicSetup,
          keymap.of([indentWithTab]),
          python(),
          indentUnit.of("  "),
          oneDark,
          theme,
          EditorView.updateListener.of((update) => {
            if (update.docChanged) latest.current.onChange(update.state.doc.toString());
          }),
        ],
      }),
    });

    view.current = instance;
    return () => {
      instance.destroy();
      view.current = null;
    };
    // Mount once; document swaps are handled by the documentKey effect below.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    const instance = view.current;
    if (!instance) return;
    const current = instance.state.doc.toString();
    if (current === value) return;
    instance.dispatch({
      changes: { from: 0, to: current.length, insert: value },
    });
    // Only a deliberate document swap replaces the doc; ordinary typing flows
    // out through onChange and must not round-trip back in.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [documentKey]);

  return <div className="editor" ref={host} />;
}
