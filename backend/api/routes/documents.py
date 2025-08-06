from fastapi import APIRouter, UploadFile, File
from ingestion.pdf_parser import extract_text
from embeddings.chunking import chunk_text
from embeddings.embedder import get_embedding
from embeddings.vector_store import upsert
import uuid

router = APIRouter()

@router.post("/documents/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    contents = await file.read()
    path = f"/tmp/{file.filename}"
    with open(path, 'wb') as f: f.write(contents)
    text = extract_text(path)
    for i, chunk in enumerate(chunk_text(text)):
        vec = get_embedding(chunk)
        upsert(str(uuid.uuid4()), vec, {"text": chunk})
    return {"status": "ok"}