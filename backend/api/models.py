from pydantic import BaseModel
from typing import List, Any

class QueryRequest(BaseModel):
    query: str

class Clause(BaseModel):
    clause_id: str
    text: str

class QueryResponse(BaseModel):
    decision: str
    amount: int
    justification: List[Clause]