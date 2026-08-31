import json
from types import SimpleNamespace

from agent import analyse_incident, build_prompt
from demo_data import DEMO_EVIDENCE, DEMO_INCIDENT


VALID_ANALYSIS = {
    "severity": "HIGH",
    "severity_rationale": "Two business dashboards are stale.",
    "technical_diagnosis": "A rename and type change broke the transformation.",
    "likely_root_cause": "An uncoordinated upstream schema deployment.",
    "impacted_assets": [{
        "name": "Executive Revenue Overview",
        "asset_type": "DASHBOARD",
        "impact_reason": "Its source transformation failed.",
        "business_impact": "Finance lacks current revenue reporting.",
    }],
    "recovery_actions": [{
        "priority": "P0",
        "owner": "Data Engineering",
        "action": "Patch the transformation for the new schema.",
        "success_check": "The transformation and dashboards refresh successfully.",
    }],
    "containment_summary": "Pause dependent refreshes and label dashboards stale.",
    "prevention_follow_up": "Add schema contracts and compatibility checks.",
    "incident_brief": "CUSTOMER_ORDERS drift broke reporting.",
    "stakeholder_notification": "DRAFT — requires human approval before sending.",
}


class FakeModels:
    def generate_content(self, **kwargs):
        self.kwargs = kwargs
        return SimpleNamespace(
            text=json.dumps(VALID_ANALYSIS),
            usage_metadata=SimpleNamespace(
                prompt_token_count=120,
                candidates_token_count=80,
                total_token_count=200,
            ),
        )


def test_analysis_returns_validated_output_and_metrics():
    fake = SimpleNamespace(models=FakeModels())
    result = analyse_incident(DEMO_INCIDENT, DEMO_EVIDENCE, client=fake)
    assert result.analysis.severity == "HIGH"
    assert result.metrics.total_tokens == 200
    assert result.metrics.model == "gemini-3.7-flash"


def test_prompt_discloses_demo_evidence_and_approval_gate():
    prompt = build_prompt(DEMO_INCIDENT, DEMO_EVIDENCE)
    assert "demo evidence" in prompt.lower()
    assert "human approval" in prompt.lower()

