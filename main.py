"""
SQL Rule Engine — FastAPI Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router


# --- FastAPI App ---

app = FastAPI(
    title="SQL Rule Engine",
    description="Evaluate SQL queries: normalize, lint, execute, and compare results.",
    version="1.0.0",
)

# CORS — allow Next.js dev server and common localhost ports
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")
