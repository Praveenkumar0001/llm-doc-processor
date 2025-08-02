import mailparser

def extract_text(path: str) -> str:
    m = mailparser.parse_from_file(path)
    return m.body