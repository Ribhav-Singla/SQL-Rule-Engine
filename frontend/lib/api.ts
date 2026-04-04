/* ── API Client for SQL Rule Engine ── */

const API_BASE = "/api";

export interface EvaluateRequest {
  sql: string;
  schema_name: string;
  problem_id: string;
}

export interface QuestionAttempt {
  problem_id: string;
  raw_sql: string;
  normalized_sql: string;
  runtime_status: string;
  preview_columns: string[];
  preview_rows: Record<string, unknown>[];
  row_count: number;
}

export interface RuleIssue {
  triggered: boolean;
  issue: string;
  category: string;
  explanation: string;
}

export interface EvaluateResult {
  cached?: boolean;
  fingerprint?: string;
  result_hash?: string;
  correct?: boolean;
  rule_results?: RuleIssue[];
  feedback?: Record<string, unknown>;
  question_attempt?: QuestionAttempt;
  error?: string;
}

export interface NormalizeResult {
  normalized_sql?: string;
  error?: string;
}

export interface Problem {
  problem_id: string;
  title: string;
  pattern: string;
  schema: string;
  query: string;
}

class ApiClient {
  private async request<T>(
    endpoint: string,
    options?: RequestInit
  ): Promise<T> {
    const res = await fetch(`${API_BASE}${endpoint}`, {
      headers: { "Content-Type": "application/json" },
      ...options,
    });

    if (!res.ok) {
      const body = await res.json().catch(() => ({}));
      throw new Error(body.detail || `API error: ${res.status}`);
    }

    return res.json();
  }

  async evaluate(
    sql: string,
    schemaName: string,
    problemId: string
  ): Promise<EvaluateResult> {
    return this.request<EvaluateResult>("/evaluate", {
      method: "POST",
      body: JSON.stringify({
        sql,
        schema_name: schemaName,
        problem_id: problemId,
      }),
    });
  }

  async normalize(sql: string): Promise<NormalizeResult> {
    return this.request<NormalizeResult>("/normalize", {
      method: "POST",
      body: JSON.stringify({ sql }),
    });
  }

  async healthCheck(): Promise<{ status: string }> {
    return this.request<{ status: string }>("/health");
  }

  async getProblems(): Promise<Problem[]> {
    return this.request<Problem[]>("/problems");
  }
}

export const api = new ApiClient();
