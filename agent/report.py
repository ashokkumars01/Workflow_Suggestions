import os
import json
import requests

def post_comment(body: str):
    """
    Posts optimization suggestions as a PR comment.
    Runs ONLY inside GitHub Actions.
    """

    # GitHub provides event metadata here
    event_path = os.getenv("GITHUB_EVENT_PATH")
    if not event_path:
        # Running locally → do nothing
        return

    with open(event_path, "r", encoding="utf-8") as f:
        event = json.load(f)

    # Only comment on Pull Requests
    if "pull_request" not in event:
        return

    comments_url = event["pull_request"]["comments_url"]
    token = os.getenv("GITHUB_TOKEN")

    if not token:
        raise RuntimeError("GITHUB_TOKEN not found")

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

    payload = {
        "body": body
    }

    response = requests.post(
        comments_url,
        headers=headers,
        json=payload,
        timeout=10
    )

    if response.status_code >= 300:
        raise RuntimeError(
            f"Failed to post PR comment: {response.status_code} {response.text}"
        )
