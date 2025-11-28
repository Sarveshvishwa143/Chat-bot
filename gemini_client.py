import requests

# Correct Gemini REST endpoint
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def get_gemini_response(prompt: str, model: str = "gemini-2.0-flash") -> str:
    # Use your existing key (you can also move this to env var later)
    api_key = "AIzaSyB-KxAGTYRs_VEU9iezX2QQrc9KB8AlBXE"

    if not api_key:
        raise RuntimeError("Set Gemini API key")

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key,
    }

    # Correct request body for generateContent
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    resp = requests.post(API_URL, json=payload, headers=headers, timeout=60)

    # If the server returns non‑200, show raw text to help debug instead of JSON error
    try:
        resp.raise_for_status()
    except requests.HTTPError:
        return f"HTTP {resp.status_code}: {resp.text}"

    data = resp.json()

    # Correct key is "candidates", not "condidates"
    candidates = data.get("candidates", [])
    if candidates:
        content = candidates[0].get("content", {})
        parts = content.get("parts", [])
        if parts and "text" in parts[0]:
            return parts[0]["text"]

    # Fallback: just show full JSON
    return str(data)
