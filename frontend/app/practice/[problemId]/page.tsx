"use client";

import { useState, useCallback } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import SqlEditor from "@/components/SqlEditor";
import ResultsPanel from "@/components/ResultsPanel";
import SchemaReference from "@/components/SchemaReference";
import { api } from "@/lib/api";
import type { EvaluateResult } from "@/lib/api";
import { getProblemById, patternColors } from "@/lib/problems";
import styles from "./page.module.css";

export default function PracticePage() {
  const params = useParams();
  const problemId = params.problemId as string;
  const problem = getProblemById(problemId);

  const [sqlValue, setSqlValue] = useState("");
  const [result, setResult] = useState<EvaluateResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleRun = useCallback(async () => {
    if (!sqlValue.trim() || !problem) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await api.evaluate(
        sqlValue,
        problem.schema,
        problem.problem_id
      );
      setResult(response);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "An unexpected error occurred"
      );
    } finally {
      setLoading(false);
    }
  }, [sqlValue, problem]);

  if (!problem) {
    return (
      <div className={styles.notFound}>
        <h2>Problem not found</h2>
        <p>
          No problem with ID <strong>{problemId}</strong> exists.
        </p>
        <Link href="/" className={styles.backLink}>
          ← Back to Problems
        </Link>
      </div>
    );
  }

  const patternColor = patternColors[problem.pattern] || "#F97316";

  return (
    <div className={styles.page}>
      {/* Breadcrumb + Problem Info */}
      <div className={styles.topBar}>
        <div className={styles.topBarInner}>
          <Link href="/" className={styles.backLink} id="back-to-problems">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="m15 18-6-6 6-6" />
            </svg>
            Problems
          </Link>

          <div className={styles.problemInfo}>
            <span className={styles.problemId}>{problem.problem_id}</span>
            <h1 className={styles.problemTitle}>{problem.title}</h1>
            <span
              className={styles.patternTag}
              style={{
                backgroundColor: `${patternColor}12`,
                color: patternColor,
                borderColor: `${patternColor}30`,
              }}
            >
              {problem.pattern}
            </span>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className={styles.content}>
        {/* Left: Editor */}
        <div className={styles.editorCol}>
          <SqlEditor
            value={sqlValue}
            onChange={setSqlValue}
            onRun={handleRun}
            loading={loading}
          />
        </div>

        {/* Right: Schema Reference */}
        <div className={styles.schemaCol}>
          <SchemaReference />
        </div>
      </div>

      {/* Results */}
      <div className={styles.results}>
        <ResultsPanel result={result} loading={loading} error={error} />
      </div>
    </div>
  );
}
