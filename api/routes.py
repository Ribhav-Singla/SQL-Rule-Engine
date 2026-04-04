import json
import os

from fastapi import APIRouter, HTTPException

from api.schemas import (
    EvaluateRequest, EvaluateResponse,
    NormalizeRequest, NormalizeResponse,
    FingerprintRequest, FingerprintResponse,
    RulesRequest, RulesResponse, RuleIssue,
    ProblemResponse,
)
from config.enums import Schema
from normalization.query import normalize_sql
from hasher.fingerprint import generate_query_fingerprint
from rules import run_rules
from evaluator import evaluate_query

router = APIRouter()

# Load problems once at startup
_PROBLEMS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "Problems", "problems.json"
)
with open(_PROBLEMS_PATH, "r", encoding="utf-8") as f:
    _PROBLEMS: list[dict] = json.load(f)


@router.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@router.get("/problems", response_model=list[ProblemResponse])
def list_problems():
    """Return all available SQL problems."""
    return _PROBLEMS


@router.get("/problems/{problem_id}", response_model=ProblemResponse)
def get_problem(problem_id: str):
    """Return a single SQL problem by ID."""
    for p in _PROBLEMS:
        if p["problem_id"] == problem_id:
            return p
    raise HTTPException(status_code=404, detail=f"Problem '{problem_id}' not found")


@router.post("/normalize", response_model=NormalizeResponse)
def normalize(req: NormalizeRequest):
    """
    Parse and normalize a SQL query.
    Returns the normalized SQL string.
    """
    result = normalize_sql(req.sql)
    if result["error"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return NormalizeResponse(normalized_sql=result["normalized_sql"])


@router.post("/fingerprint", response_model=FingerprintResponse)
def fingerprint(req: FingerprintRequest):
    """
    Generate a unique fingerprint for a SQL query + schema.
    Format: schema_name:sha256(normalized_sql)
    """
    parsed = normalize_sql(req.sql)
    if parsed["error"]:
        raise HTTPException(status_code=400, detail=parsed["error"])

    schema = Schema(req.schema_name.value)
    fp = generate_query_fingerprint(req.problem_id, schema, parsed["normalized_sql"])
    return FingerprintResponse(fingerprint=fp, normalized_sql=parsed["normalized_sql"])


@router.post("/rules", response_model=RulesResponse)
def check_rules(req: RulesRequest):
    """
    Run the rule engine on a SQL query.
    Returns triggered issues (select *, missing WHERE, cartesian join, etc.)
    """
    parsed = normalize_sql(req.sql)
    if parsed["error"]:
        raise HTTPException(status_code=400, detail=parsed["error"])

    issues = run_rules(parsed["ast"])
    return RulesResponse(
        normalized_sql=parsed["normalized_sql"],
        issues_count=len(issues),
        issues=[RuleIssue(**i) for i in issues],
    )


@router.post("/evaluate", response_model=EvaluateResponse)
def evaluate(req: EvaluateRequest):
    """
    Full pipeline: normalize → fingerprint → cache check →
    rules + execute → hash → compare → feedback → cache update.
    """
    schema = Schema(req.schema_name.value)
    result = evaluate_query(req.sql, schema, req.problem_id)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return EvaluateResponse(**result)
