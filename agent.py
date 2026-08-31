"""Evidence-bound Gemini analysis service using Vertex AI authentication."""

from __future__ import annotations

import json
import os
import time
from typing import Any

from google import genai
from google.genai import types
from pydantic import ValidationError

from costs import build_run_metrics
from models import AnalysisResult, IncidentAnalysis, validate_incident_text


DEFAULT_MODEL = "gemini-3.7-flash"
DEFAULT_LOCATION = "global"


class AgentServiceError(RuntimeError):
    """A safe, actionable error suitable for the Streamlit interface."""


def build_prompt(incident_text: str, evidence: dict[str, Any]) -> str:
    return f"""You are a data incident response agent supporting data engineers.

Analyse the incident using only the supplied incident report and demo evidence.
Do not claim to have queried live systems. Separate technical impact from
business impact. Prioritise recovery actions as P0, P1, or P2 and assign a
plausible team owner. The stakeholder notification is a DRAFT and must state
that it requires human approval before sending.

INCIDENT REPORT:
{incident_text}

DEMO EVIDENCE:
{json.dumps(evidence, indent=2, sort_keys=True)}
"""


def _client(project: str, location: str):
    return genai.Client(vertexai=True, project=project, location=location)


def analyse_incident(
    incident_text: str,
    evidence: dict[str, Any],
    *,
    client: Any | None = None,
    project: str | None = None,
    location: str | None = None,
    model: str | None = None,
) -> AnalysisResult:
    incident_text = validate_incident_text(incident_text)
    project = project or os.getenv("GOOGLE_CLOUD_PROJECT")
    location = location or os.getenv("GOOGLE_CLOUD_LOCATION", DEFAULT_LOCATION)
    model = model or os.getenv("GEMINI_MODEL", DEFAULT_MODEL)
    if client is None and not project:
        raise AgentServiceError(
            "GOOGLE_CLOUD_PROJECT is not set. Set it to your Google Cloud project ID."
        )

    active_client = client or _client(project, location)
    started = time.perf_counter()
    try:
        response = active_client.models.generate_content(
            model=model,
            contents=build_prompt(incident_text, evidence),
            config=types.GenerateContentConfig(
                temperature=0.2,
                response_mime_type="application/json",
                response_json_schema=IncidentAnalysis.model_json_schema(),
            ),
        )
        if not response.text:
            raise AgentServiceError("Gemini returned an empty response. Please retry.")
        analysis = IncidentAnalysis.model_validate_json(response.text)
    except AgentServiceError:
        raise
    except ValidationError as exc:
        raise AgentServiceError(
            "Gemini returned an incomplete incident analysis. Please retry."
        ) from exc
    except Exception as exc:
        raise AgentServiceError(
            "Gemini analysis could not run. Check Vertex AI access, project settings, "
            "and the selected model, then retry."
        ) from exc

    latency_ms = round((time.perf_counter() - started) * 1000)
    metrics = build_run_metrics(
        getattr(response, "usage_metadata", None),
        model=model,
        latency_ms=latency_ms,
    )
    return AnalysisResult(analysis=analysis, metrics=metrics)

