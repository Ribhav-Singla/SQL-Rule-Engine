"""
SQL Rule Engine — FastAPI Application
"""

from fastapi import FastAPI
from api.routes import router


# --- FastAPI App ---

app = FastAPI(
    title="SQL Rule Engine",
    description="Evaluate SQL queries: normalize, lint, execute, and compare results.",
    version="1.0.0",
)

app.include_router(router, prefix="/api")
