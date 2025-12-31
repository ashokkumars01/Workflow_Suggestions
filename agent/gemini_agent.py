# agent/gemini_agent.py
import os
from google import genai
from typing import List, Dict

# ---------------------
# Configure Gemini client
# ---------------------
def get_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not found in environment variables")
    genai.configure(api_key=api_key)
    return genai

# ---------------------
# Generate prompt for Gemini
# ---------------------
def generate_prompt(metadata: List[Dict]) -> str:
    """
    Converts sanitized static-analysis metadata into a prompt for Gemini.
    """
    prompt = """
You are a senior software optimization expert.

You are given ONLY anonymized static-analysis metadata.
You DO NOT see source code.

Your job:
- Detect redundant logic patterns
- Identify performance bottlenecks
- Suggest safe refactoring ideas
- Never infer business logic

Metadata:
"""
    for file_data in metadata:
        file_name = file_data.get("file", "unknown")
        prompt += f"\nFile: {file_name}\n"
        for issue in file_data.get("issues", []):
            issue_type = issue.get("type", "unknown")
            line = issue.get("line", "-")
            desc = issue.get("description", "")
            # Include occurrences for redundant_code
            occurrences = issue.get("occurrences")
            if occurrences:
                occurrence_lines = ", ".join(str(fn.get("line")) for fn in occurrences)
                prompt += f"- {issue_type} at lines: {occurrence_lines}\n"
            else:
                prompt += f"- {issue_type} at line {line}. {desc}\n"

    prompt += "\nRespond in MARKDOWN with code suggestions and explanations."
    return prompt

# ---------------------
# Call Gemini to optimize
# ---------------------
def optimize(metadata: List[Dict]) -> str:
    """
    Sends static-analysis metadata to Gemini and returns optimization suggestions.
    """
    client = get_client()
    prompt = generate_prompt(metadata)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "temperature": 0.2,
            "max_output_tokens": 10000  # safe upper limit
        }
    )

    # Gemini v2.5 returns a 'content' list of text items
    if hasattr(response, "content"):
        # Collect all text parts
        text_parts = [item.text for item in response.content if hasattr(item, "text")]
        return "\n".join(text_parts)
    # Fallback
    return getattr(response, "text", "")
