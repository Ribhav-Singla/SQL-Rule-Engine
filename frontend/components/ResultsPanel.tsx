"use client";

import styles from "./ResultsPanel.module.css";
import type { EvaluateResult } from "@/lib/api";

interface ResultsPanelProps {
  result: EvaluateResult | null;
  loading?: boolean;
  error?: string | null;
}

export default function ResultsPanel({
  result,
  loading = false,
  error,
}: ResultsPanelProps) {
  if (loading) {
    return (
      <div className={styles.panel} id="results-panel">
        <div className={styles.loadingState}>
          <div className={styles.loadingSpinner} />
          <p className={styles.loadingText}>Evaluating your query...</p>
          <p className={styles.loadingHint}>
            Normalizing → Executing → Comparing → Analyzing
          </p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.panel} id="results-panel">
        <div className={styles.errorState}>
          <div className={styles.statusIcon} data-status="error">✗</div>
          <h3 className={styles.errorTitle}>Error</h3>
          <p className={styles.errorMessage}>{error}</p>
        </div>
      </div>
    );
  }

  if (!result) {
    return (
      <div className={styles.panel} id="results-panel">
        <div className={styles.emptyState}>
          <div className={styles.emptyIcon}>
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M12 20h9" />
              <path d="M16.376 3.622a1 1 0 0 1 3.002 3.002L7.368 18.635a2 2 0 0 1-.855.506l-2.872.838a.5.5 0 0 1-.62-.62l.838-2.872a2 2 0 0 1 .506-.854z" />
            </svg>
          </div>
          <h3 className={styles.emptyTitle}>Ready to evaluate</h3>
          <p className={styles.emptyText}>
            Write your SQL query above and click <strong>Run Query</strong> to
            see results.
          </p>
        </div>
      </div>
    );
  }

  const attempt = result.question_attempt;
  const rules = result.rule_results || [];

  return (
    <div className={styles.panel} id="results-panel">
      {/* Status Banner */}
      <div
        className={styles.statusBanner}
        data-correct={result.correct ? "true" : "false"}
      >
        <div className={styles.statusLeft}>
          <div
            className={styles.statusIcon}
            data-status={result.correct ? "success" : "error"}
          >
            {result.correct ? "✓" : "✗"}
          </div>
          <div>
            <h3 className={styles.statusTitle}>
              {result.correct ? "Correct!" : "Incorrect"}
            </h3>
            <p className={styles.statusSub}>
              {result.correct
                ? "Your query produces the expected result."
                : "Your query result doesn't match the expected output."}
            </p>
          </div>
        </div>

        <div className={styles.statusMeta}>
          {attempt && (
            <span className={styles.metaItem}>
              {attempt.row_count} row{attempt.row_count !== 1 ? "s" : ""}
            </span>
          )}
          {result.cached && (
            <span className={styles.cachedBadge}>Cached</span>
          )}
        </div>
      </div>

      {/* Rule Violations */}
      {rules.length > 0 && (
        <div className={styles.section}>
          <h4 className={styles.sectionTitle}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3" />
              <path d="M12 9v4" />
              <path d="M12 17h.01" />
            </svg>
            Rule Issues ({rules.length})
          </h4>
          <div className={styles.ruleList}>
            {rules.map((rule, i) => (
              <div key={i} className={styles.ruleItem}>
                <span className={styles.ruleCategory}>{rule.category}</span>
                <span className={styles.ruleIssue}>{rule.issue}</span>
                <p className={styles.ruleExplanation}>{rule.explanation}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {rules.length === 0 && result.correct !== undefined && (
        <div className={styles.section}>
          <div className={styles.noIssues}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
              <polyline points="22 4 12 14.01 9 11.01" />
            </svg>
            No rule violations found — clean query!
          </div>
        </div>
      )}

      {/* Data Preview */}
      {attempt && attempt.preview_columns.length > 0 && (
        <div className={styles.section}>
          <h4 className={styles.sectionTitle}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <rect x="3" y="3" width="18" height="18" rx="2" />
              <path d="M3 9h18" />
              <path d="M9 21V9" />
            </svg>
            Data Preview
            <span className={styles.previewCount}>
              {attempt.preview_rows.length} of {attempt.row_count} rows
            </span>
          </h4>
          <div className={styles.tableWrapper}>
            <table className={styles.table} id="data-preview-table">
              <thead>
                <tr>
                  {attempt.preview_columns.map((col) => (
                    <th key={col}>{col}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {attempt.preview_rows.map((row, i) => (
                  <tr key={i}>
                    {attempt.preview_columns.map((col) => (
                      <td key={col}>
                        {row[col] === null ? (
                          <span className={styles.nullValue}>NULL</span>
                        ) : (
                          String(row[col])
                        )}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Normalized SQL */}
      {attempt?.normalized_sql && (
        <div className={styles.section}>
          <h4 className={styles.sectionTitle}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="16 18 22 12 16 6" />
              <polyline points="8 6 2 12 8 18" />
            </svg>
            Normalized SQL
          </h4>
          <pre className={styles.normalizedSql}>
            <code>{attempt.normalized_sql}</code>
          </pre>
        </div>
      )}
    </div>
  );
}
