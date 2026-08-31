# Data Incident Action Agent

An agentic incident-response prototype for data engineers. It turns a schema
drift report and dependency evidence into:

- a severity classification and technical diagnosis;
- affected transformations and dashboards with business impact;
- a prioritised, owner-assigned recovery plan;
- an incident brief and stakeholder notification draft;
- a human approval record before any communication could be sent; and
- Gemini latency, token usage, and configurable estimated cost.

The built-in scenario models a breaking change to `CUSTOMER_ORDERS`:
`customer_id` becomes `customer_key`, while `order_total` changes from
`NUMERIC` to `STRING`. This breaks `fct_customer_orders` and leaves Finance and
Operations dashboards stale.

## Safety and evidence boundaries

- Dependency data in this prototype is clearly labelled demo metadata.
- Gemini is instructed to reason only from the supplied report and evidence.
- The application does not send email, chat messages, or mutate data systems.
- The **Approve draft** action records a UTC timestamp only.
- There is no fabricated fallback. Preview mode is explicitly labelled as
  deterministic sample output.

## Architecture

See [docs/architecture.md](docs/architecture.md).

## Run locally

Requires Python 3.12.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export GOOGLE_CLOUD_PROJECT=all-things-agentic-deepthy
export GOOGLE_CLOUD_LOCATION=global
export GEMINI_MODEL=gemini-3.7-flash
gcloud auth application-default login
streamlit run app.py
```

For a clearly labelled UI preview that makes no Gemini call:

```bash
APP_DEMO_MODE=true streamlit run app.py
```

## Optional cost estimate

Gemini token counts are recorded from SDK usage metadata. To display an
estimated USD cost, configure current per-million-token prices:

```bash
export GEMINI_INPUT_USD_PER_1M_TOKENS="<current input price>"
export GEMINI_OUTPUT_USD_PER_1M_TOKENS="<current output price>"
```

If rates are absent, the UI displays **Unavailable**, never a false zero.

## Test

```bash
pytest -q
python -m compileall -q .
```

The suite covers Pydantic contracts, invalid input, usage/cost handling,
structured Gemini service output with a fake client, and the full Streamlit
preview sequence including approval and reset.

## Deploy to Cloud Run

From Google Cloud Shell:

```bash
gcloud config set project all-things-agentic-deepthy
gcloud services enable run.googleapis.com cloudbuild.googleapis.com aiplatform.googleapis.com
gcloud run deploy data-incident-action-agent \
  --source . \
  --region europe-west1 \
  --allow-unauthenticated \
  --min 0 \
  --max 1 \
  --set-env-vars GOOGLE_CLOUD_PROJECT=all-things-agentic-deepthy,GOOGLE_CLOUD_LOCATION=global,GEMINI_MODEL=gemini-3.7-flash
```

The Cloud Run runtime service account needs permission to call Vertex AI,
normally the `Vertex AI User` role.

## Technology

- Python 3.12
- Streamlit
- Google Gen AI SDK in Vertex AI mode
- Gemini 3.7 Flash
- Pydantic structured output
- pytest
- Docker and Google Cloud Run

## AI disclosure

The project was designed and implemented with Codex assistance. Gemini performs
the incident analysis at runtime. The participant selected the problem,
scenario, product behaviour, safety boundary, and deployment approach, and
reviews the generated recovery and communication outputs.

## Licence

Apache-2.0.

