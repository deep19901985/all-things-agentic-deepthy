# Technical Spec

## Overview

Data Incident Action Agent is a single-service Python/Streamlit application deployed to Google Cloud Run. It uses the Google Gen AI Python SDK in Vertex AI mode to call Gemini 3.7 Flash once per incident. A deterministic demo dependency catalogue grounds the request. Gemini returns one structured JSON response, which Pydantic validates before the UI stores or renders it.

The design prioritises a reliable demonstration, explainability, safe human approval, and minimal infrastructure. There is no database, background worker, external notification integration, or API key.

## Stack

- Python 3.12
- Streamlit for the web UI and session state
- Google Gen AI SDK (`google-genai`) in Vertex AI mode
- Gemini model configured by `GEMINI_MODEL`, default `gemini-3.7-flash`
- Pydantic v2 for structured response validation
- pytest for unit tests
- Docker for a deterministic Cloud Run container
- Google Cloud Run in `europe-west1`
- Vertex authentication via Application Default Credentials locally and the Cloud Run service account in production

Official references:

- [Google Gen AI Python SDK](https://googleapis.github.io/python-genai/)
- [Structured output](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/capabilities/control-generated-output)
- [Cloud Run source deployment](https://docs.cloud.google.com/run/docs/deploying-source-code)
- [Cloud Run container contract](https://docs.cloud.google.com/run/docs/container-contract)

## Architecture

### Streamlit Presentation Layer

Implements: `prd.md > Epic 1`, `Epic 4`, and `Epic 5`.

Renders the incident editor, status progression, analysis action, result cards, approval, timestamp, errors, and run metrics. It owns browser-session state only.

### Incident Agent Service

Implements: `prd.md > Epic 2`, `Epic 3`, and `Epic 5`.

Builds a grounded prompt from the incident and demo metadata, invokes Gemini, measures elapsed time, validates the response, and returns one typed result plus usage metrics. It has no UI logic.

### Structured Domain Models

Implements: acceptance criteria across `prd.md > Epic 2`, `Epic 3`, and `Epic 4`.

Pydantic models define exactly what successful analysis means. Validation failure is handled as an error rather than partial success.

### Deterministic Evidence Catalogue

Implements: `prd.md > Epic 2`.

Supplies the expected schema, observed drift, transformations, dashboards, and dependency reasons. The UI and README label this as demo evidence, not live lineage.

### Operational Metrics

Implements: `prd.md > Epic 5`.

Extracts prompt, candidate, and total token counts from response usage metadata, measures latency, and estimates cost from configurable rates. The estimate is explicitly labelled and is never presented as a live billing charge.

### Cloud Runtime

Implements: `prd.md > Submission Proof Points`.

Cloud Run serves the container publicly for judging. It scales to zero, caps maximum instances at one, receives `PORT`, and uses its service identity for Vertex access.

## File Structure

```text
data-incident-action-agent/
├── app.py                     # Streamlit layout, actions, state, cards, approval
├── agent.py                   # Gemini client, prompt construction, validated call
├── models.py                  # Pydantic response and metric models
├── demo_data.py               # Fixed CUSTOMER_ORDERS schema and dependencies
├── costs.py                   # Usage extraction and configurable cost estimate
├── styles.py                  # Small navy/blue CSS block
├── requirements.txt           # Runtime and test dependencies
├── Dockerfile                 # Streamlit on 0.0.0.0:$PORT
├── .dockerignore              # Excludes local/cache/git files
├── .gitignore                 # Excludes credentials, caches, environment files
├── README.md                  # Problem, architecture, setup, deploy, disclosure
├── LICENSE                    # Apache-2.0
├── architecture.md            # Mermaid source for architecture diagram
├── tests/
│   ├── test_costs.py          # Token-cost calculation and unavailable cases
│   ├── test_models.py         # Valid/invalid structured analysis
│   └── test_validation.py     # Incident input rules
└── docs/hackathon-build/      # Scope, PRD, spec, checklist, build notes
```

## Data Contracts

### Incident Input

- `incident_text`: trimmed string, minimum 30 characters, maximum 4,000 characters.

### Evidence Input

- Source asset and expected schema.
- Observed schema changes.
- Dependencies with name, asset type, dependency reason, and business process.

### Gemini Response: `IncidentAnalysis`

- `severity`: LOW, MEDIUM, HIGH, or CRITICAL.
- `severity_rationale`, `technical_diagnosis`, and `likely_root_cause`.
- `impacted_assets[]`: name, asset type, impact reason, business impact.
- `recovery_actions[]`: P0/P1/P2 priority, owner, action, success check.
- `containment_summary` and `prevention_follow_up`.
- `incident_brief` and `stakeholder_notification`.

### Run Metrics

- Model, latency, input/output/total tokens, and estimated cost or unavailable.

## Data Flow

1. `app.py` initialises session state with no analysis and no approval.
2. `demo_data.py` provides the editable default incident and deterministic catalogue.
3. The user selects **Analyse Incident**.
4. Input validation rejects blank, short, or overly long text without calling Gemini.
5. `app.py` clears stale results and approval before calling `agent.analyse_incident`.
6. `agent.py` serialises the incident and evidence into a concise grounded prompt.
7. The SDK calls Gemini through Vertex AI with JSON response MIME type and the response schema.
8. `models.py` validates the response. Any API, parse, or validation error becomes a retryable UI failure.
9. Usage metadata and latency are converted to run metrics; `costs.py` calculates an estimate only when token counts and rates exist.
10. Successful analysis and metrics enter Streamlit session state.
11. Result cards render with the notification in **Awaiting approval**.
12. Approval records an ISO UTC timestamp and displays **Simulation only—nothing was sent**.
13. Refreshing the browser or starting a new run resets session-only state.

## Components And Responsibilities

### `app.py`

Implements: `prd.md > Core User Journey`.

- Page layout, styling, workflow indicator, incident input, validation, buttons, result cards, approval, and metrics.
- Calls the agent once per deliberate click.
- Never fabricates fallback analysis.

### `agent.py`

Implements: `prd.md > Epic 2` and `Epic 3`.

- Creates a Vertex-mode Gen AI client from project and location environment variables.
- Creates an evidence-bound prompt and requests structured JSON.
- Measures latency and returns validated output plus usage metadata.
- Raises a small application error with a safe message.

### `models.py`

- Defines severity/priority values and Pydantic models.
- Rejects missing fields and invalid values.

### `demo_data.py`

- Stores the default incident, expected/observed schema facts, one transformation, and at least two dashboards.
- Contains no sensitive or production data.

### `costs.py`

- Extracts token counts defensively.
- Reads configurable input/output costs per million tokens.
- Returns unavailable when pricing is not configured.
- Uses Decimal arithmetic and labels the result estimated.

### `styles.py`

- Contains compact high-contrast navy/blue CSS.
- Avoids custom JavaScript.

## External APIs And Dependencies

- `google-genai`: Gemini content generation and usage metadata.
- `streamlit`: interface and session state.
- `pydantic`: response validation.
- `pytest`: tests.
- Vertex/Agent Platform API: model access.
- Cloud Run Admin API: deployment.
- Cloud Build and Artifact Registry may be enabled automatically by source deployment.

No DataHub, dbt, database, email, Slack, Jira, or billing API is called.

## AI Usage

Gemini receives the editable incident, deterministic schema/dependency evidence, an incident-response role, evidence-bound reasoning rules, and the structured output schema. Gemini performs severity reasoning, technical diagnosis, business interpretation, action ordering, incident-brief generation, and stakeholder-language translation.

Application code owns validation, evidence supply, output validation, state, approval, metrics, and rendering. This makes AI central without delegating safety or truth boundaries to the model.

## Error Strategy

1. Local input error: show guidance and do not call Gemini.
2. Credential/model/API error: preserve input, keep results empty, show retry.
3. Structured-output error: do not render partial content; show retry.
4. Missing usage/pricing: show unavailable; keep analysis successful.
5. Deployment error: check container port, logs, service-account permission, project, model, and region in order.

## Security And Cost Controls

- No API key or credential file committed.
- Local authentication uses `gcloud auth application-default login`.
- Cloud Run uses its service account with only required Vertex permission.
- Minimum instances 0; maximum instances 1.
- Public access is accepted for judging and can be removed later.
- Model and price rates are environment configuration.
- User input is length-limited.

## Deployment

Environment:

```text
GOOGLE_CLOUD_PROJECT=all-things-agentic-deepthy
GOOGLE_CLOUD_LOCATION=europe-west1
GEMINI_MODEL=gemini-3.7-flash
INPUT_COST_PER_MILLION_USD=<current configured rate>
OUTPUT_COST_PER_MILLION_USD=<current configured rate>
```

Container command:

```text
streamlit run app.py --server.address=0.0.0.0 --server.port=${PORT:-8080} --server.headless=true
```

Deployment shape:

```text
gcloud run deploy data-incident-action-agent \
  --source . \
  --project all-things-agentic-deepthy \
  --region europe-west1 \
  --allow-unauthenticated \
  --min 0 \
  --max 1 \
  --set-env-vars GOOGLE_CLOUD_PROJECT=all-things-agentic-deepthy,GOOGLE_CLOUD_LOCATION=europe-west1,GEMINI_MODEL=gemini-3.7-flash
```

The exact command will be checked against the installed `gcloud` CLI before use.

## Risks And Verification

### Model identifier or regional availability

Risk: `gemini-3.7-flash` may not be callable in `europe-west1` even though it appears in Agent Studio.

Verification: run one SDK smoke test before UI work. If unavailable, use a supported Vertex location while leaving Cloud Run in Europe, and record the actual location.

### Cloud Run service-account permission

Risk: local credentials work but the deployed identity cannot invoke Gemini.

Verification: verify the deployed service account and grant the minimal Vertex role if required, then test the public URL and inspect logs.

### Streamlit rerun behaviour

Risk: edits or clicks accidentally retain stale approval.

Verification: analyse → approve → edit → analyse; approval must clear.

### Structured output

Risk: schema incompatibility or incomplete response.

Verification: run one real call, validate it, and keep the schema compact.

### Deadline

Risk: polish consumes deployment and video time.

Verification: local flow first, Cloud Run second, README/diagram third, styling last.

## Verification Plan

- Unit tests for valid/invalid Pydantic payloads.
- Unit tests for configured/unconfigured cost estimation.
- Unit tests for incident validation.
- Local Streamlit smoke test.
- Real Vertex AI smoke test.
- Cloud Run health and public-access check.
- Manual analysis, approval, timestamp, and reset path.
- Incognito test of the public URL.
- Capture Cloud Run and Vertex proof for the video.

## Demo And Submission Flow

1. Open the Cloud Run URL with the detected incident.
2. Explain the schema drift and demo dependency catalogue.
3. Select **Analyse Incident**.
4. Show severity, diagnosis, impacted assets, and business impact.
5. Focus on the sequenced recovery plan.
6. Show the notification awaiting approval.
7. Approve and show timestamp plus simulation disclosure.
8. Show model, tokens, estimated cost, and latency.
9. Show Cloud Run/Vertex evidence, diagram, and repository.

## Build Checklist Handoff

1. Scaffold models, demo data, costs, and tests.
2. Implement and smoke-test Gemini.
3. Build the minimum Streamlit workflow.
4. Run automated and manual verification.
5. Deploy to Cloud Run and verify public access.
6. Finish README, architecture diagram, and demo materials.
7. Add polish only if time remains.
