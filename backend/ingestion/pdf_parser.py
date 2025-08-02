import PyPDF2

def extract_text(path: str) -> str:
    reader = PyPDF2.PdfReader(path)
    return "\n".join(p.extract_text() or "" for p in reader.pages)