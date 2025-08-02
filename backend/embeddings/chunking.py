import re

def chunk_text(text: str, max_len: int = 500) -> list[str]:
    words = text.split()
    chunks, curr = [], []
    for w in words:
        curr.append(w)
        if len(" ".join(curr)) > max_len:
            chunks.append(" ".join(curr))
            curr = []
    if curr:
        chunks.append(" ".join(curr))
    return chunks