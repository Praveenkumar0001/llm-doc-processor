from fastapi import FastAPI
from .routes import query, documents

app = FastAPI()
app.include_router(query.router)
app.include_router(documents.router)