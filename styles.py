"""Shared Streamlit presentation helpers."""


APP_CSS = """
<style>
    .stApp {
        background:
          radial-gradient(circle at 90% 0%, rgba(56,189,248,.12), transparent 30rem),
          radial-gradient(circle at 5% 35%, rgba(99,102,241,.10), transparent 28rem),
          #f7f9fc;
    }
    .block-container {max-width: 1180px; padding-top: 2rem;}
    .hero {
        padding: 1.35rem 1.5rem;
        color: white;
        border-radius: 18px;
        background: linear-gradient(120deg, #172554, #312e81 55%, #155e75);
        box-shadow: 0 18px 45px rgba(30, 41, 59, .16);
        margin-bottom: 1rem;
    }
    .hero h1 {margin: 0; font-size: 2.1rem;}
    .hero p {margin: .45rem 0 0; color: #dbeafe;}
    .eyebrow {
        font-size: .75rem;
        font-weight: 750;
        letter-spacing: .08em;
        text-transform: uppercase;
        color: #64748b;
    }
    .panel {
        border: 1px solid #dbe4f0;
        border-radius: 14px;
        padding: 1rem;
        background: rgba(255,255,255,.88);
        margin: .3rem 0 .85rem;
    }
    .approval {
        border: 1px solid #f59e0b;
        border-radius: 14px;
        padding: 1rem;
        background: #fffbeb;
    }
    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: .8rem;
    }
</style>
"""


def severity_color(severity: str) -> str:
    return {
        "LOW": "#16803c",
        "MEDIUM": "#a15c00",
        "HIGH": "#c23b22",
        "CRITICAL": "#9c1c1c",
    }.get(severity, "#475569")


def severity_badge(severity: str) -> str:
    color = severity_color(severity)
    return (
        f'<span style="background:{color};color:white;padding:.3rem .65rem;'
        f'border-radius:999px;font-weight:750">{severity}</span>'
    )
