from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


# --- Request Schemas ---

class SchemaName(str, Enum):
    """Mirror of config.enums.Schema for API validation."""
    ECOMMERCE = "ecommerce"
    BANKING = "banking"
    SOCIAL = "social"
    INVENTORY = "inventory"
    ANALYTICS = "analytics"


class EvaluateRequest(BaseModel):
    """Full pipeline: evaluate a user's SQL query."""
    sql: str = Field(..., example="SELECT * FROM customers")
    schema_name: SchemaName = Field(..., example="ecommerce")
    problem_id: str = Field(..., description="Identifier of the problem being attempted; used to fetch expected hash from DB")


class NormalizeRequest(BaseModel):
    """Normalize a SQL query."""
    sql: str = Field(..., example="select  *  from   customers  WHERE id=1")


class FingerprintRequest(BaseModel):
    """Generate a fingerprint for a normalized query."""
    sql: str = Field(..., example="SELECT * FROM customers WHERE id = 1")
    schema_name: SchemaName = Field(..., example="ecommerce")
    problem_id: Optional[str] = Field(None, description="Identifier of the problem being fingerprinted")


class RulesRequest(BaseModel):
    """Run rule engine on a SQL query."""
    sql: str = Field(..., example="SELECT * FROM customers, orders")


# --- Response Schemas ---

class NormalizeResponse(BaseModel):
    normalized_sql: Optional[str] = None
    error: Optional[str] = None


class FingerprintResponse(BaseModel):
    fingerprint: str
    normalized_sql: str


class RuleIssue(BaseModel):
    triggered: bool
    issue: str
    category: str
    explanation: str


class RulesResponse(BaseModel):
    normalized_sql: str
    issues_count: int
    issues: list[RuleIssue]


class QuestionAttempt(BaseModel):
    problem_id: Optional[str] = None
    raw_sql: Optional[str] = None
    normalized_sql: Optional[str] = None
    runtime_status: Optional[str] = None
    preview_columns: Optional[list[str]] = None
    preview_rows: Optional[list[dict]] = None
    row_count: Optional[int] = None


class EvaluateResponse(BaseModel):
    cached: Optional[bool] = None
    fingerprint: Optional[str] = None
    result_hash: Optional[str] = None
    correct: Optional[bool] = None
    rule_results: Optional[list[dict]] = None
    feedback: Optional[dict] = None
    question_attempt: Optional[QuestionAttempt] = None
    error: Optional[str] = None


class ProblemResponse(BaseModel):
    problem_id: str
    title: str
    pattern: str
    schema: str
    query: str
