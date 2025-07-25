def build_prompt(email_text):
    return f"""
You are a cybersecurity analyst assistant.

Analyze the following email and decide:
1. Is this a phishing attempt? (Yes/No)
2. What makes it suspicious?
3. What should the user do next?

Email:
\"\"\"
{email_text}
\"\"\"

Respond clearly and briefly.
"""
