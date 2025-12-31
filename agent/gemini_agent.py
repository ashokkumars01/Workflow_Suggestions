import os
from google import genai

def optimize(metadata):
    """
    Sends sanitized metadata ONLY (no source code)
    """

    client = genai.Client(
        api_key=os.environ["AIzaSyAzRrx82-E88UiamJDY_DRTtWdbUt-Cz1o"]
    )

    prompt = f"""
You are a senior software optimization expert.

You are given ONLY anonymized static-analysis metadata.
You DO NOT see source code.

Your job:
- Detect redundant logic patterns
- Identify performance bottlenecks
- Suggest safe refactoring ideas
- Never infer business logic

Metadata:
{metadata}

Respond in MARKDOWN.
"""

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt,
        config={
            "temperature": 0.2,
            "max_output_tokens": 1000000
        }
    )

    return response.text
