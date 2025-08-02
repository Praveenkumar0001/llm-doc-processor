def evaluate(entities: dict, clauses: list[dict]) -> dict:
    # stub: always approve for demo
    return {
        "decision": "approved",
        "amount": 100000,
        "justification": clauses[:2]
    }