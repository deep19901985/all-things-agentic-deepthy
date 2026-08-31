import pytest
from pydantic import ValidationError

from models import IncidentAnalysis, validate_incident_text


def test_incident_analysis_rejects_unknown_severity():
    with pytest.raises(ValidationError):
        IncidentAnalysis.model_validate({
            "severity": "URGENT",
            "severity_rationale": "Impact",
            "technical_diagnosis": "Diagnosis",
            "likely_root_cause": "Cause",
            "impacted_assets": [{
                "name": "dashboard",
                "asset_type": "DASHBOARD",
                "impact_reason": "Stale",
                "business_impact": "Decisions delayed",
            }],
            "recovery_actions": [{
                "priority": "P0",
                "owner": "Data Engineering",
                "action": "Repair",
                "success_check": "Refresh succeeds",
            }],
            "containment_summary": "Contain",
            "prevention_follow_up": "Prevent",
            "incident_brief": "Brief",
            "stakeholder_notification": "Draft",
        })


def test_incident_text_validation():
    assert validate_incident_text("  schema drift  ") == "schema drift"
    with pytest.raises(ValueError):
        validate_incident_text("   ")

