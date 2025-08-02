import pinecone

pinecone.init(api_key="YOUR_KEY", environment="us-west1-gcp")
idx = pinecone.Index("documents")

def upsert(id: str, vector: list[float], metadata: dict):
    idx.upsert([(id, vector, metadata)])

def query(vector: list[float], top_k: int = 5):
    return idx.query(vector=vector, top_k=top_k)