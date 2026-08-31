"""Token and estimated-cost accounting for a Gemini run."""

from __future__ import annotations

import os
from decimal import Decimal, InvalidOperation
from typing import Any

from models import RunMetrics


def _get(source: Any, *names: str) -> int | None:
    if source is None:
        return None
    for name in names:
        value = source.get(name) if isinstance(source, dict) else getattr(source, name, None)
        if value is not None:
            return int(value)
    return None


def _rate(name: str) -> Decimal | None:
    value = os.getenv(name)
    if not value:
        return None
    try:
        rate = Decimal(value)
    except InvalidOperation:
        return None
    return rate if rate >= 0 else None


def estimate_cost_usd(input_tokens: int | None, output_tokens: int | None) -> Decimal | None:
    """Estimate cost using explicitly configured USD rates per million tokens."""
    input_rate = _rate("GEMINI_INPUT_USD_PER_1M_TOKENS")
    output_rate = _rate("GEMINI_OUTPUT_USD_PER_1M_TOKENS")
    if input_tokens is None or output_tokens is None or input_rate is None or output_rate is None:
        return None
    million = Decimal(1_000_000)
    return (Decimal(input_tokens) * input_rate + Decimal(output_tokens) * output_rate) / million


def build_run_metrics(metadata: Any, *, model: str, latency_ms: int) -> RunMetrics:
    input_tokens = _get(metadata, "prompt_token_count", "promptTokenCount", "input_token_count")
    output_tokens = _get(metadata, "candidates_token_count", "candidatesTokenCount", "output_token_count")
    total_tokens = _get(metadata, "total_token_count", "totalTokenCount")
    if total_tokens is None and input_tokens is not None and output_tokens is not None:
        total_tokens = input_tokens + output_tokens
    cost = estimate_cost_usd(input_tokens, output_tokens)
    return RunMetrics(
        model=model,
        latency_ms=latency_ms,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
        estimated_cost_usd=cost,
        cost_status="estimated" if cost is not None else "unavailable",
    )
