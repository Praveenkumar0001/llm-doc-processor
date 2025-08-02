TEMPLATE = '''
You are a policy expert. Given the entities:
{entities}
and the following document chunks:
{chunks}
Decide which chunks are relevant.
Return a JSON list of selected chunk IDs.
'''