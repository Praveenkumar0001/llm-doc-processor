TEMPLATE = '''
Extract the following fields from the user query:
- age
- procedure
- location
- policy_duration (in months)

User Query: "{query}"

Respond in JSON with keys: age, procedure, location, policy_duration.
'''