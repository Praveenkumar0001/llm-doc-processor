# backend/api/app.py

import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# ─── Load environment variables ────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(dotenv_path=BASE_DIR / ".env")

# ─── Create FastAPI app ────────────────────────────────────────────────────────
app = FastAPI(
    title="LLM Document Processor",
    version="1.0.0",
)

# ─── CORS ───────────────────────────────────────────────────────────────────────
origins = os.getenv("CORS_ORIGINS", "").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Include routers ───────────────────────────────────────────────────────────
from api.routes import query, documents

app.include_router(query.router, prefix="/query", tags=["Query"])
app.include_router(documents.router, prefix="/documents", tags=["Documents"])

# ─── Pinecone init ─────────────────────────────────────────────────────────────
from embeddings.vector_store import init_pinecone

@app.on_event("startup")
def startup_event():
    try:
        init_pinecone()
        print("✅ Pinecone initialized successfully.")
    except Exception as e:
        print(f"⚠️ Pinecone init failed: {e}")

# ─── Health check ──────────────────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok", "version": app.version}

@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Welcome! See /docs for API."}
