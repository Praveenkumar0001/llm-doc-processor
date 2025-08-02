# backend/embeddings/vector_store.py

import os
from pathlib import Path

from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec, PineconeException

# ─── Load environment variables ────────────────────────────────────────────────
# `.env` is expected one level up from this file
ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=ENV_PATH)

API_KEY       = os.getenv("PINECONE_API_KEY")
ENVIRONMENT   = os.getenv("PINECONE_ENVIRONMENT")    # e.g. "us-west1-gcp"
INDEX_NAME    = os.getenv("PINECONE_INDEX", "documents")
VECTOR_DIM    = int(os.getenv("VECTOR_DIMENSION", 1536))
METRIC        = os.getenv("PINECONE_METRIC", "cosine")  # or "euclidean"

if not API_KEY or not ENVIRONMENT:
    raise RuntimeError("Missing PINECONE_API_KEY or PINECONE_ENVIRONMENT in .env")

# ─── Initialize Pinecone client ────────────────────────────────────────────────
pc = Pinecone(api_key=API_KEY, environment=ENVIRONMENT)

# ─── Ensure index exists ───────────────────────────────────────────────────────
try:
    existing = pc.list_indexes().names()
except PineconeException as e:
    raise RuntimeError(f"Pinecone list_indexes() failed: {e}")

if INDEX_NAME not in existing:
    pc.create_index(
        name=INDEX_NAME,
        dimension=VECTOR_DIM,
        metric=METRIC,
        spec=ServerlessSpec(cloud="aws", region="us-west-2")
    )

# ─── Obtain a handle to the index ──────────────────────────────────────────────
index = pc.Index(INDEX_NAME)


def upsert(id: str, vector: list[float], metadata: dict) -> dict:
    """
    Upsert a single vector (and optional metadata) into the Pinecone index.
    
    :param id:      Unique string ID for the vector.
    :param vector:  The embedding vector.
    :param metadata: Arbitrary JSON-serializable metadata.
    :return:        Pinecone response dict.
    """
    return index.upsert(items=[(id, vector, metadata)])


def query(vector: list[float], top_k: int = 5, include_metadata: bool = True) -> dict:
    """
    Query the index for the top_k most similar vectors.
    
    :param vector:          The query embedding.
    :param top_k:           How many results to return.
    :param include_metadata: Whether to include stored metadata in the results.
    :return:                Pinecone query response dict.
    """
    return index.query(
        queries=[vector],
        top_k=top_k,
        include_values=False,
        include_metadata=include_metadata
    )


def delete_index() -> None:
    """
    (Utility) Delete the entire index. Use with caution!
    """
    pc.delete_index(name=INDEX_NAME)
