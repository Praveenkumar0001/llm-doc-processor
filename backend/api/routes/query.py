from fastapi import APIRouter, Depends
from ..models import QueryRequest, QueryResponse
from ..dependencies import get_db
from ...ingestion.pdf_parser import extract_text
from ...embeddings.chunking import chunk_text
from ...embeddings.embedder import get_embedding
from ...embeddings.vector_store import query as vs_query
from ...llm_orchestration.parser_prompt import TEMPLATE as PARSE_TMPL
from ...llm_orchestration.search_prompt import TEMPLATE as SEARCH_TMPL
from ...rules_engine.rules import evaluate
import openai

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def process_query(req: QueryRequest):
    # 1. parse
    parse_prompt = PARSE_TMPL.format(query=req.query)
    parse_res = openai.ChatCompletion.create(model="gpt-4", messages=[{"role":"user","content":parse_prompt}])
    entities = parse_res.choices[0].message.content
    # 2. semantic search
    emb = get_embedding(req.query)
    search_res = vs_query(emb)
    top_ids = [m['id'] for m in search_res['matches']]
    clauses = [{'clause_id': i, 'text': '...'} for i in top_ids]
    # 3. evaluate
    result = evaluate(entities, clauses)
    return result