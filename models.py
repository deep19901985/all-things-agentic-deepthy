"""Typed contracts and input validation for the incident agent."""

from __future__ import annotations

from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field


Severity = Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
Priority = Literal["P0", "P1", "P2"]
AssetType = Literal["TABLE", "TRANSFORMATION", "DASHBOARD", "OTHER"]


class ImpactedAsset(BaseModel):
    name: str = Field(min_length=1)
    asset_type: AssetType
    impact_reason: str = Field(min_length=1)
    business_impact: str = Field(min_length=1)


class RecoveryAction(BaseModel):
    priority: Priority
    owner: str = Field(min_length=1)
    action: str = Field(min_length=1)
    success_check: str = Field(min_length=1)


class IncidentAnalysis(BaseModel):
    severity: Severity
    severity_rationale: str = Field(min_length=1)
    technical_diagnosis: str = Field(min_length=1)
    likely_root_cause: str = Field(min_length=1)
    impacted_assets: list[ImpactedAsset] = Field(min_length=1)
    recovery_actions: list[RecoveryAction] = Field(min_length=1)
    containment_summary: str = Field(min_length=1)
    prevention_follow_up: str = Field(min_length=1)
    incident_brief: str = Field(min_length=1)
    stakeholder_notification: str = Field(min_length=1)


class RunMetrics(BaseModel):
    model: str
    latency_ms: int = Field(ge=0)
    input_tokens: int | None = Field(default=None, ge=0)
    output_tokens: int | None = Field(default=None, ge=0)
    total_tokens: int | None = Field(default=None, ge=0)
    estimated_cost_usd: Decimal | None = Field(default=None, ge=0)
    cost_status: Literal["estimated", "unavailable"]


class AnalysisResult(BaseModel):
    analysis: IncidentAnalysis
    metrics: RunMetrics


def validate_incident_text(value: str, *, max_chars: int = 8_000) -> str:
    """Return clean incident text or raise a user-safe validation error."""
    clean = value.strip()
    if not clean:
        raise ValueError("Enter an incident description before running the agent.")
    if len(clean) > max_chars:
        raise ValueError(f"Keep the incident description under {max_chars:,} characters.")
    return clean
