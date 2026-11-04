"""The only place in the backend that calls a model.

Purpose: one shared wrapper for every model call, with a MOCK path for
offline runs and an optional request log for the prompts coverage check.
Original author: [CUE: teammate who wrote the first version] (query_llm, AsyncOpenAI, Responses API)
Rewritten by: Claude (claude.ai chat), model Claude Fable 5.1, 2026-11-02, directed and reviewed by Torian Styles
Human edits: [CUE]
External sources: none

What changed from the first version, and why:
  - os.environ[""] -> the SDK reads OPENAI_API_KEY itself; the empty-name lookup raised KeyError at import.
  - a stray token after the closing paren was a SyntaxError.
  - query_llm called an AsyncOpenAI method without await, so it returned a coroutine, not text; it is now async.
  - added the sync functions the educator loop needs (chat, chat_json, mode, usage_totals), the MOCK path,
    and PROMPT_LOG logging. One file, one call path, so the prompts PDF documents one thing.
  - the default model is still gpt-4.1-mini, read from SHD_MODEL; note that OpenAI lists the 4o/4.1 family
    for retirement on 2027-01-14 (gpt-6-luna is the documented successor), so change SHD_MODEL before then.

Environment:
    OPENAI_API_KEY   required for live calls (read by the openai SDK; never by this code)
    SHD_MODEL        model name (default gpt-4.1-mini)
    MOCK_LLM=1       force the mock path even if a key is present
    PROMPT_LOG=1     append every request and reply to logs/model_calls.jsonl
"""

import json
import os
import time
from pathlib import Path

MODEL = os.environ.get("SHD_MODEL", "gpt-4.1-mini")
LOG_PATH = Path(__file__).resolve().parents[1] / "logs" / "model_calls.jsonl"
CALLS = []  # in-memory tally for the current process (usage_totals)


def mock_enabled():
    """MOCK: true when there is no key or MOCK_LLM=1; callers then get their mock_reply."""
    return os.environ.get("MOCK_LLM") == "1" or not os.environ.get("OPENAI_API_KEY")


def _log(record):
    if os.environ.get("PROMPT_LOG") != "1":
        return
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def _record(prompt_id, messages, reply, usage=None, model=None):
    record = {"t": time.time(), "prompt_id": prompt_id, "model": model or MODEL, "messages": messages, "reply": reply}
    if usage is not None:
        record["tokens_in"] = getattr(usage, "input_tokens", None) or getattr(usage, "prompt_tokens", None)
        record["tokens_out"] = getattr(usage, "output_tokens", None) or getattr(usage, "completion_tokens", None)
    CALLS.append(record)
    _log(record)


# ---------------------------------------------------------------- original entry point, fixed


async def query_llm(prompt: str, prompt_id: str | None = None, mock_reply: str | None = None) -> str:
    """Single-prompt call through the Responses API (the first version's design, made to run)."""
    if mock_enabled():
        _record(prompt_id, [{"role": "user", "content": prompt}], mock_reply, model="mock")
        return mock_reply or "(mock LLM reply)"

    from openai import AsyncOpenAI  # lazy so the mock path needs no package

    client = AsyncOpenAI()
    response = await client.responses.create(model=MODEL, input=prompt)
    _record(prompt_id, [{"role": "user", "content": prompt}], response.output_text, getattr(response, "usage", None))
    return response.output_text


# ---------------------------------------------------------------- what the educator loop uses (sync)


def chat(messages, temperature=0.2, mock_reply=None, json_mode=False, prompt_id=None):
    """Send a messages list and return the reply text.

    mock_reply is returned verbatim on the MOCK path.
    json_mode asks the model for a single JSON object.
    prompt_id is recorded in the log so scripts/check_prompt_coverage.py can match it to prompts/.
    """
    if mock_enabled():
        _record(prompt_id, messages, mock_reply, model="mock")
        return mock_reply or "(mock LLM reply)"

    from openai import OpenAI

    client = OpenAI()
    kwargs = {"model": MODEL, "messages": messages, "temperature": temperature}
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
    response = client.chat.completions.create(**kwargs)
    text = response.choices[0].message.content.strip()
    _record(prompt_id, messages, text, getattr(response, "usage", None))
    return text


def chat_json(messages, mock_reply=None, temperature=0.2, prompt_id=None):
    """Like chat(), but parses the reply as a JSON object. Returns None if it can't."""
    text = chat(
        messages,
        temperature=temperature,
        json_mode=True,
        prompt_id=prompt_id,
        mock_reply=json.dumps(mock_reply) if mock_reply is not None else None,
    )
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        start, end = text.find("{"), text.rfind("}")
        if start != -1 and end > start:
            try:
                return json.loads(text[start : end + 1])
            except json.JSONDecodeError:
                pass
        return None


def mode():
    return "mock" if mock_enabled() else MODEL


def usage_totals():
    return {
        "calls": len(CALLS),
        "tokens_in": sum(c.get("tokens_in") or 0 for c in CALLS),
        "tokens_out": sum(c.get("tokens_out") or 0 for c in CALLS),
    }
