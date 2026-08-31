"""Streamlit UI for the Data Incident Action Agent."""

from __future__ import annotations

import os
from datetime import datetime, timezone

import streamlit as st

from agent import AgentServiceError, analyse_incident
from costs import build_run_metrics
from demo_data import DEMO_ANALYSIS, DEMO_EVIDENCE, DEMO_INCIDENT
from models import AnalysisResult, IncidentAnalysis, validate_incident_text
from styles import APP_CSS, severity_badge


st.set_page_config(
    page_title="Data Incident Action Agent",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(APP_CSS, unsafe_allow_html=True)


def _initialise_state() -> None:
    defaults = {
        "incident_text": DEMO_INCIDENT,
        "result": None,
        "approved_at": None,
        "last_error": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _demo_result() -> AnalysisResult:
    return AnalysisResult(
        analysis=IncidentAnalysis.model_validate(DEMO_ANALYSIS),
        metrics=build_run_metrics(
            {
                "prompt_token_count": 842,
                "candidates_token_count": 611,
                "total_token_count": 1_453,
            },
            model="demo-preview (not a live Gemini call)",
            latency_ms=640,
        ),
    )


def _run_analysis() -> None:
    st.session_state.result = None
    st.session_state.approved_at = None
    st.session_state.last_error = None
    try:
        incident = validate_incident_text(st.session_state.incident_text)
        if os.getenv("APP_DEMO_MODE", "").lower() in {"1", "true", "yes"}:
            st.session_state.result = _demo_result()
        else:
            st.session_state.result = analyse_incident(incident, DEMO_EVIDENCE)
    except (ValueError, AgentServiceError) as exc:
        st.session_state.last_error = str(exc)


def _reset() -> None:
    st.session_state.incident_text = DEMO_INCIDENT
    st.session_state.result = None
    st.session_state.approved_at = None
    st.session_state.last_error = None


def _approve() -> None:
    st.session_state.approved_at = datetime.now(timezone.utc).isoformat(
        timespec="seconds"
    )


def _render_evidence() -> None:
    source = DEMO_EVIDENCE["source_table"]
    st.markdown(
        '<div class="eyebrow">Evidence supplied to the agent</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f"**{source['name']}** · `{source['status']}`  \n"
        + "  \n".join(f"- {change}" for change in source["changes"])
    )
    with st.expander("View demo dependency metadata"):
        st.caption(DEMO_EVIDENCE["provenance"])
        for item in DEMO_EVIDENCE["transformations"] + DEMO_EVIDENCE["dashboards"]:
            st.write(f"**{item['name']}** — {item['status']}")


def _render_analysis(result: AnalysisResult) -> None:
    analysis = result.analysis
    st.markdown("---")
    status_col, stage_col = st.columns([1, 3])
    with status_col:
        st.markdown(severity_badge(analysis.severity), unsafe_allow_html=True)
    with stage_col:
        stage = "Approved" if st.session_state.approved_at else "Awaiting approval"
        st.caption(f"Detected → Analysed → Plan ready → **{stage}**")

    st.subheader("Diagnosis and impact")
    tech_col, business_col = st.columns(2)
    with tech_col:
        st.markdown(
            '<div class="eyebrow">Technical diagnosis</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="panel">{analysis.technical_diagnosis}</div>',
            unsafe_allow_html=True,
        )
        st.markdown("**Likely root cause**")
        st.write(analysis.likely_root_cause)
    with business_col:
        st.markdown(
            '<div class="eyebrow">Business severity</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="panel">{analysis.severity_rationale}</div>',
            unsafe_allow_html=True,
        )
        st.markdown("**Impacted assets**")
        for asset in analysis.impacted_assets:
            st.markdown(
                f"- **{asset.name}** · {asset.asset_type.title()}  \n"
                f"  {asset.business_impact}"
            )

    st.subheader("Recovery plan")
    st.caption("Prioritised actions generated from the incident report and demo evidence.")
    for action in analysis.recovery_actions:
        with st.container(border=True):
            left, right = st.columns([1, 5])
            left.markdown(f"### {action.priority}")
            right.markdown(f"**{action.owner}** — {action.action}")
            right.caption(f"Success check: {action.success_check}")

    brief_col, follow_col = st.columns(2)
    with brief_col:
        st.subheader("Incident brief")
        st.info(analysis.incident_brief)
    with follow_col:
        st.subheader("Contain and prevent")
        st.markdown(f"**Containment:** {analysis.containment_summary}")
        st.markdown(f"**Follow-up:** {analysis.prevention_follow_up}")

    st.subheader("Stakeholder notification")
    st.warning(
        "Human approval gate: this application never sends email or messages. "
        "Approval only records that the draft was reviewed."
    )
    st.text_area(
        "Notification draft",
        value=analysis.stakeholder_notification,
        height=150,
        disabled=True,
    )
    if st.session_state.approved_at:
        st.success(f"Approved at {st.session_state.approved_at} UTC — still not sent.")
    else:
        st.button("Approve draft", type="primary", key="approve", on_click=_approve)

    st.subheader("Run metrics")
    metrics = result.metrics
    metric_cols = st.columns([1.6, 1, 1, 1, 1])
    metric_cols[0].metric("Model", metrics.model)
    metric_cols[1].metric("Latency", f"{metrics.latency_ms} ms")
    metric_cols[2].metric("Input tokens", metrics.input_tokens or "Unavailable")
    metric_cols[3].metric("Output tokens", metrics.output_tokens or "Unavailable")
    if metrics.estimated_cost_usd is None:
        metric_cols[4].metric("Estimated cost", "Unavailable")
        st.caption(
            "Set GEMINI_INPUT_USD_PER_1M_TOKENS and "
            "GEMINI_OUTPUT_USD_PER_1M_TOKENS to show an estimate."
        )
    else:
        metric_cols[4].metric("Estimated cost", f"${metrics.estimated_cost_usd:.6f}")


_initialise_state()

st.markdown(
    """
    <div class="hero">
      <div style="font-size:.78rem;letter-spacing:.12em;text-transform:uppercase">
        AI-assisted incident response
      </div>
      <h1>Data Incident Action Agent</h1>
      <p>Turn schema-drift evidence into technical diagnosis, business impact,
      an owner-assigned recovery plan, and an approval-gated incident brief.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if os.getenv("APP_DEMO_MODE", "").lower() in {"1", "true", "yes"}:
    st.info("Preview mode: results are deterministic sample output, not a live Gemini call.")

input_col, evidence_col = st.columns([3, 2])
with input_col:
    st.text_area(
        "Incident report",
        key="incident_text",
        height=190,
        max_chars=8_000,
        help="Describe what changed, what failed, and any known business impact.",
    )
    analyse_col, reset_col = st.columns([1, 4])
    analyse_col.button(
        "Analyse incident",
        type="primary",
        key="analyse",
        on_click=_run_analysis,
        use_container_width=True,
    )
    reset_col.button("Reset", key="reset", on_click=_reset)
with evidence_col:
    _render_evidence()

if st.session_state.last_error:
    st.error(st.session_state.last_error)
    st.caption("Correct the input or configuration, then choose Analyse incident again.")

if st.session_state.result:
    _render_analysis(st.session_state.result)

st.markdown("---")
st.caption(
    "Hackathon prototype · Demo lineage metadata is clearly labelled · "
    "No stakeholder messages are sent."
)
