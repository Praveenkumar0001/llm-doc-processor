# backend/embeddings/vector_store.py

import os
from pathlib import Path
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec, PineconeException
from typing import Optional

# Load .env (one level up)
ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=ENV_PATH)

API_KEY     = os.getenv("PINECONE_API_KEY")
ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
INDEX_NAME  = os.getenv("PINECONE_INDEX", "documents")
VECTOR_DIM  = int(os.getenv("VECTOR_DIMENSION", 1536))
METRIC      = os.getenv("PINECONE_METRIC", "cosine")

if not API_KEY or not ENVIRONMENT:
    # We delay raising until FastAPI startup so the import itself never fails.
    _pinecone_configured = False
else:
    _pinecone_configured = True

_pc: Optional[Pinecone] = None
_index = None


def init_pinecone():
    """Initialize Pinecone client and index. Call once on app startup."""
    global _pc, _index

    if not _pinecone_configured:
        raise RuntimeError("PINECONE_API_KEY or PINECONE_ENVIRONMENT not set in .env")

    # Create client
    _pc = Pinecone(api_key=API_KEY, environment=ENVIRONMENT)

    # Ensure index exists
    try:
        names = _pc.list_indexes().names()
    except PineconeException as e:
        raise RuntimeError(f"Pinecone list_indexes() failed: {e}")

    if INDEX_NAME not in names:
        _pc.create_index(
            name=INDEX_NAME,
            dimension=VECTOR_DIM,
            metric=METRIC,
            spec=ServerlessSpec(cloud="aws", region="us-west-2")
        )

    _index = _pc.Index(INDEX_NAME)


def upsert(id: str, vector: list[float], metadata: dict) -> dict:
    if _index is None:
        raise RuntimeError("Pinecone not initialized. Call init_pinecone() first.")
    return _index.upsert(items=[(id, vector, metadata)])


def query(vector: list[float], top_k: int = 5, include_metadata: bool = True) -> dict:
    if _index is None:
        raise RuntimeError("Pinecone not initialized. Call init_pinecone() first.")
    return _index.query(
        queries=[vector],
        top_k=top_k,
        include_values=False,
        include_metadata=include_metadata
    )
