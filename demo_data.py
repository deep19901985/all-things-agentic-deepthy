"""Deterministic demo evidence used to make the hackathon flow reproducible."""

DEMO_INCIDENT = """Schema drift detected in CUSTOMER_ORDERS.
The upstream team renamed customer_id to customer_key and changed order_total
from NUMERIC to STRING without notice. The overnight transformation failed and
the morning revenue dashboards have not refreshed."""

DEMO_EVIDENCE = {
    "source_table": {
        "name": "CUSTOMER_ORDERS",
        "status": "schema_changed",
        "expected_schema": {
            "order_id": "STRING",
            "customer_id": "STRING",
            "order_total": "NUMERIC",
            "ordered_at": "TIMESTAMP",
        },
        "observed_schema": {
            "order_id": "STRING",
            "customer_key": "STRING",
            "order_total": "STRING",
            "ordered_at": "TIMESTAMP",
        },
        "changes": [
            "customer_id renamed to customer_key",
            "order_total changed from NUMERIC to STRING",
        ],
    },
    "transformations": [{
        "name": "fct_customer_orders",
        "status": "failed",
        "reason": "Missing customer_id and incompatible SUM(order_total)",
    }],
    "dashboards": [
        {
            "name": "Executive Revenue Overview",
            "status": "stale",
            "business_owner": "Finance",
        },
        {
            "name": "Customer Order Health",
            "status": "stale",
            "business_owner": "Operations",
        },
    ],
    "freshness": {
        "last_successful_load": "2026-08-31T01:00:00Z",
        "expected_refresh": "2026-08-31T07:00:00Z",
    },
    "provenance": "Built-in demo metadata; no production systems queried.",
}

DEMO_ANALYSIS = {
    "severity": "HIGH",
    "severity_rationale": (
        "The failed transformation leaves two operational dashboards stale, "
        "including executive revenue reporting."
    ),
    "technical_diagnosis": (
        "CUSTOMER_ORDERS introduced two breaking changes: customer_id was renamed "
        "to customer_key and order_total changed from NUMERIC to STRING. "
        "fct_customer_orders still references the old field and applies a numeric "
        "aggregation, so its scheduled run failed."
    ),
    "likely_root_cause": (
        "An upstream schema deployment was released without a compatibility "
        "contract or downstream notification."
    ),
    "impacted_assets": [
        {
            "name": "fct_customer_orders",
            "asset_type": "TRANSFORMATION",
            "impact_reason": "Missing customer_id and incompatible SUM(order_total).",
            "business_impact": "All dependent order metrics stop refreshing.",
        },
        {
            "name": "Executive Revenue Overview",
            "asset_type": "DASHBOARD",
            "impact_reason": "Its source transformation failed.",
            "business_impact": "Finance cannot rely on current revenue figures.",
        },
        {
            "name": "Customer Order Health",
            "asset_type": "DASHBOARD",
            "impact_reason": "Its source transformation failed.",
            "business_impact": "Operations cannot monitor current order health.",
        },
    ],
    "recovery_actions": [
        {
            "priority": "P0",
            "owner": "Data Engineering",
            "action": (
                "Contain the incident: pause dependent refreshes and label both "
                "dashboards as stale."
            ),
            "success_check": "No consumer sees the stale dashboards as current.",
        },
        {
            "priority": "P0",
            "owner": "Data Engineering",
            "action": (
                "Patch fct_customer_orders to use customer_key and safely cast "
                "order_total to NUMERIC after rejecting invalid values."
            ),
            "success_check": "The transformation completes with zero invalid casts.",
        },
        {
            "priority": "P1",
            "owner": "Analytics Engineering",
            "action": "Backfill the missed partition and refresh both dashboards.",
            "success_check": "Freshness checks pass and totals reconcile to source.",
        },
        {
            "priority": "P2",
            "owner": "Data Platform",
            "action": "Add schema contracts and pre-deployment compatibility checks.",
            "success_check": "A breaking schema change fails CI before release.",
        },
    ],
    "containment_summary": (
        "Pause dependent refreshes, label dashboards stale, and preserve the last "
        "known-good output until validation completes."
    ),
    "prevention_follow_up": (
        "Introduce versioned schema contracts, ownership metadata, and automated "
        "compatibility tests for CUSTOMER_ORDERS."
    ),
    "incident_brief": (
        "A breaking schema change in CUSTOMER_ORDERS caused fct_customer_orders to "
        "fail, leaving Finance and Operations dashboards stale. Data Engineering "
        "should contain visibility, patch the rename and type conversion, validate "
        "the backfill, then restore refreshes."
    ),
    "stakeholder_notification": (
        "DRAFT — requires human approval before sending. We identified an upstream "
        "schema change affecting the Executive Revenue Overview and Customer Order "
        "Health dashboards. Current figures may be stale. Data Engineering is "
        "patching and validating the pipeline; a further update will follow after "
        "freshness and reconciliation checks pass."
    ),
}
