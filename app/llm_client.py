import json
from typing import Any, Dict, Optional

from openai import OpenAI
from .config import get_settings

settings = get_settings()

# Initialize OpenRouter client
client = OpenAI(
    api_key=settings.openai_api_key,
    base_url="https://openrouter.ai/api/v1"
)


def call_llm(system_prompt: str, user_prompt: str, model: Optional[str] = None) -> str:
    """
    Basic chat completion wrapper.
    If no API key is set, returns a mock response for development.
    """
    # Mock mode if no key
    if not settings.openai_api_key or settings.openai_api_key.strip() == "":
        return (
            "MOCK RESPONSE (no API key detected)\n\n"
            f"System: {system_prompt}\n\n"
            f"User: {user_prompt[:300]}..."
        )

    chosen_model = model or settings.llm_model

    response = client.chat.completions.create(
        model=chosen_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content


def call_llm_json(system_prompt: str, user_prompt: str, model: Optional[str] = None) -> Dict[str, Any]:
    """
    Ask the LLM to return valid JSON and parse it.
    """
    json_instructions = (
        "Return ONLY valid JSON. Do not include markdown or comments. "
        "Only return a JSON object that can be parsed by json.loads."
    )

    full_system = system_prompt + "\n\n" + json_instructions
    raw = call_llm(full_system, user_prompt, model=model)

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {
            "error": "JSON parsing failed",
            "raw_response": raw
        }
