from costs import build_run_metrics


def test_metrics_estimate_cost_when_rates_exist(monkeypatch):
    monkeypatch.setenv("GEMINI_INPUT_USD_PER_1M_TOKENS", "1")
    monkeypatch.setenv("GEMINI_OUTPUT_USD_PER_1M_TOKENS", "2")
    metrics = build_run_metrics(
        {"prompt_token_count": 1000, "candidates_token_count": 500},
        model="gemini-test",
        latency_ms=120,
    )
    assert str(metrics.estimated_cost_usd) == "0.002"
    assert metrics.cost_status == "estimated"
    assert metrics.total_tokens == 1500


def test_metrics_report_unavailable_without_rates(monkeypatch):
    monkeypatch.delenv("GEMINI_INPUT_USD_PER_1M_TOKENS", raising=False)
    monkeypatch.delenv("GEMINI_OUTPUT_USD_PER_1M_TOKENS", raising=False)
    metrics = build_run_metrics(None, model="gemini-test", latency_ms=0)
    assert metrics.estimated_cost_usd is None
    assert metrics.cost_status == "unavailable"
