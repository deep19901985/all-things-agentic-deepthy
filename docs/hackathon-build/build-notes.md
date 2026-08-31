# Build Notes

## Onboarding

- Deepening rounds completed: 3
- Project direction accepted: Data Incident Action Agent.
- Primary user: data engineer.
- Trigger: schema drift in `CUSTOMER_ORDERS`.
- Autonomous work: severity classification, downstream impact assessment, prioritised recovery plan, incident brief, and notification drafting.
- Safety boundary: no notification or change is executed before explicit human approval.
- Demo flow: Detected → Analysed → Plan Ready → Awaiting Approval → Approved.
- Visual direction: calm professional data-operations control room, navy/blue palette, structured result cards.
- Active shaping: Deepthy replaced the generic pipeline-failure scenario with a specific schema-drift incident and confirmed the autonomous actions and approval boundary.

## Scope

- Time budget: 3–4 hours total, with roughly 2 hours reserved for implementation.
- Inspirations: DataHub impact analysis, Monte Carlo incident intelligence, and dbt schema contracts.
- Scope cut: no real external integrations, mutations, authentication, persistence, multiple incident types, or complex multi-agent orchestration.
- Added by participant: per-run Gemini token usage and estimated cost.
- Demo emphasis: technical diagnosis and business impact have equal visibility; the recovery plan is the hero output.
- Confirmed project name: Data Incident Action Agent.
- Deepening rounds completed: 1

## PRD

- Confirmed initial state: detected incident with high-attention status.
- Confirmed behaviour: editable input, single analysis action, visible workflow progression, result cards, approval simulation, and run metrics.
- Confirmed edge cases: invalid input, duplicate clicks, model/validation failure, retry, and state reset before a new analysis.
- Confirmed wow moment: raw drift evidence becomes a sequenced recovery plan in one action.
- Confirmed detail: impacted assets show type and reason; recovery actions show priority and owner; approval shows a timestamp.
- Persistence remains out of scope; the experience is anonymous and session-only.
- Deepening rounds completed: 1

## Spec

- Stack: Python 3.12, Streamlit, Google Gen AI SDK in Vertex mode, Pydantic, pytest, Docker, and Cloud Run.
- Authentication: Application Default Credentials locally and Cloud Run service identity in production; no API key.
- Architecture: one Streamlit service, one Gemini call, deterministic evidence, structured validation, session-only approval.
- Deployment: public Cloud Run URL in `europe-west1`, minimum instances 0, maximum instances 1.
- Model: environment-configured, default `gemini-3.7-flash`.
- Cost: configurable per-million-token rates; unavailable rather than false zero when not configured.
- Failure rule: honest retry errors only; no silent mock fallback.
- Deepening rounds completed: 1

## Checklist

- Plan and implementation handed off to Codex.
- Build mode: autonomous speed-run.
- Verification pauses: after local MVP and after public Cloud Run verification.
- Git cadence: small verified milestone commits once repository setup permits.
- Wow moment strengthened to: evidence → diagnosis → owner-assigned recovery plan → human approval.
- Ten sequenced build items approved by Deepthy.
# Build execution update — 31 August 2026

- Created the Python 3.12, Streamlit, Google Gen AI SDK, Pydantic, pytest, and
  Cloud Run container scaffold.
- Added typed structured-output contracts and safe incident validation.
- Added labelled demo evidence for CUSTOMER_ORDERS schema drift, one failed
  transformation, and two stale dashboards.
- Added token, latency, and configurable estimated-cost accounting. Missing
  pricing is reported as unavailable rather than zero.
- Implemented the evidence-bound Vertex AI Gemini service and safe errors.
- Implemented the complete Streamlit workflow, human approval timestamp, and
  explicit no-send behaviour.
- Verification: 9 tests pass, compileall passes, and Streamlit health returns
  `ok` in preview mode.
- Deferred verification: real Gemini call and Cloud Run deployment require
  Google Cloud authentication outside this workspace.
- Published the application, tests, Docker configuration, README, architecture,
  licence, and build documentation to the public GitHub repository
  `deep19901985/all-things-agentic-deepthy`.
