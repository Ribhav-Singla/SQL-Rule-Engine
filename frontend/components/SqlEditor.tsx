"use client";

import { useCallback, useMemo } from "react";
import CodeMirror from "@uiw/react-codemirror";
import { sql, PostgreSQL } from "@codemirror/lang-sql";
import { EditorView, keymap } from "@codemirror/view";
import { HighlightStyle, syntaxHighlighting } from "@codemirror/language";
import { tags as t } from "@lezer/highlight";
import { format } from "sql-formatter";
import styles from "./SqlEditor.module.css";

interface SqlEditorProps {
  value: string;
  onChange: (value: string) => void;
  onRun: () => void;
  loading?: boolean;
  disabled?: boolean;
}

/* ── Custom orange theme for CodeMirror ── */
const editorTheme = EditorView.theme(
  {
    "&": {
      fontSize: "14px",
      backgroundColor: "#FFFFFF",
    },
    ".cm-content": {
      caretColor: "#F97316",
      fontFamily:
        "'JetBrains Mono', 'Fira Code', 'Cascadia Code', 'Consolas', monospace",
      padding: "12px 0",
      lineHeight: "1.7",
    },
    ".cm-cursor, .cm-dropCursor": {
      borderLeftColor: "#F97316",
      borderLeftWidth: "2px",
    },
    "&.cm-focused .cm-selectionBackground, .cm-selectionBackground":
      {
        backgroundColor: "#FED7AA !important",
      },
    ".cm-activeLine": {
      backgroundColor: "rgba(255, 247, 237, 0.6)",
    },
    ".cm-gutters": {
      backgroundColor: "#FAFAFA",
      borderRight: "1px solid #F3F4F6",
      color: "#9CA3AF",
      fontFamily:
        "'JetBrains Mono', monospace",
      fontSize: "12px",
      minWidth: "48px",
    },
    ".cm-activeLineGutter": {
      backgroundColor: "#FFEDD5",
      color: "#F97316",
    },
    ".cm-foldGutter": {
      color: "#D4D4D8",
    },
    ".cm-matchingBracket": {
      backgroundColor: "#FED7AA",
      color: "#F97316 !important",
      outline: "1px solid #FDBA74",
    },
    ".cm-searchMatch": {
      backgroundColor: "#FEF3C7",
      outline: "1px solid #FDE68A",
    },
    ".cm-tooltip": {
      backgroundColor: "#FFFFFF",
      border: "1px solid #E5E7EB",
      borderRadius: "8px",
      boxShadow:
        "0 4px 12px rgba(0,0,0,0.08)",
    },
    ".cm-tooltip-autocomplete": {
      "& > ul > li": {
        padding: "4px 8px",
        fontFamily: "'JetBrains Mono', monospace",
        fontSize: "13px",
      },
      "& > ul > li[aria-selected]": {
        backgroundColor: "#FFF7ED",
        color: "#F97316",
      },
    },
    ".cm-panels": {
      backgroundColor: "#FAFAFA",
      borderTop: "1px solid #E5E7EB",
    },
  },
  { dark: false }
);

/* ── Syntax highlighting ── */
const orangeHighlight = HighlightStyle.define([
  { tag: t.keyword, color: "#F97316", fontWeight: "600" },
  { tag: t.operatorKeyword, color: "#EA580C", fontWeight: "600" },
  { tag: t.string, color: "#059669" },
  { tag: t.number, color: "#2563EB" },
  { tag: t.bool, color: "#7C3AED" },
  { tag: t.null, color: "#7C3AED", fontStyle: "italic" },
  { tag: t.comment, color: "#9CA3AF", fontStyle: "italic" },
  { tag: t.lineComment, color: "#9CA3AF", fontStyle: "italic" },
  { tag: t.blockComment, color: "#9CA3AF", fontStyle: "italic" },
  { tag: t.operator, color: "#6B7280" },
  { tag: t.punctuation, color: "#6B7280" },
  { tag: t.variableName, color: "#1E293B" },
  { tag: t.typeName, color: "#D97706" },
  {
    tag: t.function(t.variableName),
    color: "#7C3AED",
    fontWeight: "500",
  },
  { tag: t.special(t.string), color: "#059669" },
]);

export default function SqlEditor({
  value,
  onChange,
  onRun,
  loading = false,
  disabled = false,
}: SqlEditorProps) {
  const handleFormat = useCallback(() => {
    try {
      const formatted = format(value, {
        language: "postgresql",
        tabWidth: 2,
        keywordCase: "upper",
        linesBetweenQueries: 2,
      });
      onChange(formatted);
    } catch {
      // If formatting fails, keep the current value
    }
  }, [value, onChange]);

  /* Ctrl+Enter to run */
  const runKeymap = useMemo(
    () =>
      keymap.of([
        {
          key: "Ctrl-Enter",
          mac: "Cmd-Enter",
          run: () => {
            onRun();
            return true;
          },
        },
      ]),
    [onRun]
  );

  const extensions = useMemo(
    () => [
      sql({ dialect: PostgreSQL }),
      editorTheme,
      syntaxHighlighting(orangeHighlight),
      runKeymap,
      EditorView.lineWrapping,
    ],
    [runKeymap]
  );

  return (
    <div className={styles.wrapper} id="sql-editor">
      {/* Toolbar */}
      <div className={styles.toolbar}>
        <div className={styles.toolbarLeft}>
          <span className={styles.label}>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="16 18 22 12 16 6" />
              <polyline points="8 6 2 12 8 18" />
            </svg>
            SQL Editor
          </span>
          <span className={styles.hint}>PostgreSQL</span>
        </div>

        <div className={styles.toolbarRight}>
          <button
            className={styles.formatBtn}
            onClick={handleFormat}
            disabled={disabled || !value.trim()}
            title="Format SQL"
            id="format-sql-btn"
          >
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M21 10H3" />
              <path d="M21 6H3" />
              <path d="M21 14H3" />
              <path d="M21 18H3" />
            </svg>
            Format
          </button>

          <button
            className={styles.runBtn}
            onClick={onRun}
            disabled={disabled || loading || !value.trim()}
            id="run-query-btn"
          >
            {loading ? (
              <span className={styles.spinner} />
            ) : (
              <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                <path d="M8 5v14l11-7z" />
              </svg>
            )}
            {loading ? "Running..." : "Run Query"}
            {!loading && (
              <kbd className={styles.kbd}>⌘↵</kbd>
            )}
          </button>
        </div>
      </div>

      {/* Editor */}
      <div className={styles.editorContainer}>
        <CodeMirror
          value={value}
          onChange={onChange}
          height="320px"
          extensions={extensions}
          editable={!disabled && !loading}
          basicSetup={{
            lineNumbers: true,
            highlightActiveLineGutter: true,
            highlightActiveLine: true,
            bracketMatching: true,
            closeBrackets: true,
            autocompletion: true,
            foldGutter: true,
            indentOnInput: true,
            history: true,
            drawSelection: true,
            syntaxHighlighting: false,
          }}
          placeholder="Write your SQL query here..."
        />
      </div>
    </div>
  );
}
