# backend/api/app.py

import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# ─── Load .env ─────────────────────────────────────────────────────────────────
# Assume .env lives in backend/
BASE_DIR = Path(__file__).resolve().parents[1]
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# ─── Create FastAPI app ────────────────────────────────────────────────────────
app = FastAPI(
    title="LLM Document Processor",
    description="API for parsing queries, retrieving clauses via embeddings, and returning structured decisions.",
    version="1.0.0",
)

# ─── CORS (adjust origins as needed) ────────────────────────────────────────────
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# ─── Include routers ───────────────────────────────────────────────────────────
from .routes import query, documents

app.include_router(query.router, prefix="/query", tags=["Query"])
app.include_router(documents.router, prefix="/documents", tags=["Documents"])

# ─── Health check endpoint ────────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
async def health():
    """
    Simple health check.
    """
    return {"status": "ok", "version": app.version}

# ─── Root redirect or welcome ──────────────────────────────────────────────────
@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Welcome to the LLM Document Processor API. See /docs for OpenAPI UI."}
