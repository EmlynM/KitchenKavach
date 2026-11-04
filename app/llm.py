import httpx

from app.config import get_settings


class LLMServiceError(Exception):
    pass


async def call_model(question, context, api_key, base_url, model):
    if not api_key or not base_url or not model:
        raise LLMServiceError("LLM configuration is incomplete.")

    evidence = "\n\n".join(context)

    system_prompt = f"""
    You are KitchenKavach, an FSSAI compliance assistant.

    Rules:
    1. Answer only using the supplied FSSAI evidence.
    2. Never invent regulations.
    3. If evidence is insufficient, clearly say:
       I couldn't find sufficient supporting evidence
       in the available FSSAI documents.
    4. Provide source references wherever available.

    Evidence:
    {evidence}
    """

    async with httpx.AsyncClient(timeout=20) as client:

        response = await client.post(
            f"{base_url.rstrip('/')}/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "temperature": 0.1,
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            }
        )

        response.raise_for_status()

        data = response.json()

        answer = data["choices"][0]["message"]["content"]

        if not isinstance(answer, str) or not answer.strip():
            raise LLMServiceError("Empty model response.")

        usage = data.get("usage") or {}

        return {
            "answer": answer.strip(),
            "model": model,
            "usage": {
                "prompt_tokens": usage.get("prompt_tokens", 0),
                "completion_tokens": usage.get("completion_tokens", 0),
                "total_tokens": usage.get("total_tokens", 0)
            }
        }


async def call_primary(question, context):
    settings = get_settings()

    return await call_model(
        question,
        context,
        settings.llm_api_key,
        settings.llm_base_url,
        settings.primary_model
    )


async def call_fallback(question, context):
    settings = get_settings()

    return await call_model(
        question,
        context,
        settings.fallback_api_key,
        settings.fallback_base_url,
        settings.fallback_model
    )


async def generate_answer(question, context):

    try:
        result = await call_primary(question, context)

        result["used_fallback"] = False

        return result

    except (httpx.TimeoutException, httpx.TransportError):
        pass

    except httpx.HTTPStatusError as error:
        if error.response.status_code not in (408, 429) and error.response.status_code < 500:
            raise LLMServiceError(
                f"Primary model rejected the request: {error.response.status_code}"
            ) from error

    try:
        result = await call_fallback(question, context)

        result["used_fallback"] = True

        return result

    except (httpx.HTTPError, KeyError, IndexError, TypeError, ValueError) as error:
        raise LLMServiceError(
            "Both primary and fallback model attempts failed."
        ) from error