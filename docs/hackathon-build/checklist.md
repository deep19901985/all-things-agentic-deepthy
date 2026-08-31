# Build Checklist

## Build Preferences

- **Plan design:** Handed off to Codex
- **Build mode:** Autonomous
- **Comprehension checks:** N/A during execution; explanations included in handoff
- **Git:** Small commits after coherent verified milestones, once a repository is initialised
- **Verification:** Two participant look-at-it pauses
- **Check-in cadence:** Speed-run
- **Pause 1:** After the local MVP passes automated and manual checks
- **Pause 2:** After the public Cloud Run URL works end-to-end
- **Wow moment:** Evidence → diagnosis → owner-assigned recovery plan → human approval

## Checklist

- [x] **1. Scaffold the repository and runtime**
  Spec ref: `spec.md > File Structure`
  What to build: Create the project files, Python dependencies, ignore rules, Apache-2.0 licence, Dockerfile, and minimal package layout. Preserve the existing planning documents under `docs/hackathon-build/`.
  Acceptance: The repository contains every required runtime file, contains no secrets, and Python can import the project modules.
  Verify: Run `python -m compileall .` and inspect `git status --short` for unexpected files.

- [x] **2. Define validated domain models and input rules**
  Spec ref: `spec.md > Data Contracts`
  What to build: Implement severity, impacted-asset, recovery-action, incident-analysis, and run-metric Pydantic models plus incident length validation.
  Acceptance: Valid structured analysis passes; missing fields, invalid priorities, and invalid incident lengths fail clearly.
  Verify: Run `pytest -q tests/test_models.py tests/test_validation.py`.

- [x] **3. Add deterministic schema and dependency evidence**
  Spec ref: `spec.md > Components And Responsibilities > demo_data.py`
  What to build: Add the editable CUSTOMER_ORDERS incident, expected and observed schema, one transformation, and at least two dashboards with dependency and business reasons.
  Acceptance: Evidence covers both schema changes and every demo asset; the data is clearly labelled as demo metadata.
  Verify: Import and print the evidence payload; manually compare it with the PRD scenario.

- [x] **4. Implement usage metrics and cost estimation**
  Spec ref: `spec.md > Components And Responsibilities > costs.py`
  What to build: Defensively extract SDK usage metadata and calculate a Decimal estimate from configurable per-million-token rates, returning unavailable when needed.
  Acceptance: Input/output/total tokens are preserved; configured prices calculate correctly; missing prices never display false zero.
  Verify: Run `pytest -q tests/test_costs.py`.

- [ ] **5. Implement and smoke-test the Gemini service**
  Spec ref: `spec.md > Components And Responsibilities > agent.py`
  What to build: Create the Vertex-mode Gen AI client, evidence-bound prompt, structured response call, Pydantic validation, latency measurement, and safe error translation.
  Acceptance: One real CUSTOMER_ORDERS request returns a validated analysis with severity, impacted assets, recovery actions, brief, notification, and usage metadata.
  Verify: Run a small command-line smoke test using Application Default Credentials. Record the actual model and Vertex location.

  Status: Service and mocked structured-response tests are complete. The real
  smoke test is deferred to Google Cloud Shell because this build workspace has
  no Application Default Credentials.

- [x] **6. Build the minimum Streamlit workflow**
  Spec ref: `spec.md > Components And Responsibilities > app.py`
  What to build: Implement the incident editor, Analyse action, workflow state, diagnosis and business cards, hero recovery plan, incident brief, approval-gated notification, approval timestamp, metrics, and retryable error display.
  Acceptance: All PRD epics work in one browser session; new analysis clears stale results and approval; nothing is sent externally.
  Verify: Start Streamlit locally and manually run Detected → Analysed → Plan Ready → Awaiting Approval → Approved.

- [ ] **7. Verify the local MVP**
  Spec ref: `spec.md > Verification Plan`
  What to build: Complete automated tests and manual acceptance checks, including invalid input, model failure presentation, approval, timestamp, and reset.
  Acceptance: Tests pass and the primary demo path works reliably without fabricated fallback output.
  Verify: Run `pytest -q`, `python -m compileall .`, and the manual acceptance sequence.

  Status: Nine automated tests, compilation, Streamlit health, approval, reset,
  invalid-input, and deterministic preview checks pass. Final acceptance remains
  open until the real Gemini path is exercised.

  **Participant pause 1:** Show Deepthy the local MVP and request visual/behaviour feedback before deployment polish.

- [ ] **8. Add presentation and reproducibility assets**
  Spec ref: `spec.md > Demo And Submission Flow`
  What to build: Add compact control-room styling, a complete README with setup/deployment/testing/disclosure, and an architecture diagram source plus exportable image.
  Acceptance: A stranger can understand, run, and deploy the project; the interface clearly distinguishes demo metadata and estimated cost.
  Verify: Follow README setup in a clean environment where practical; render/inspect the architecture diagram and UI.

- [ ] **9. Deploy and verify on Cloud Run**
  Spec ref: `spec.md > Deployment`
  What to build: Deploy the container with project, model, region, min-zero/max-one settings and service-account Vertex access; enable only required deployment APIs when prompted.
  Acceptance: The public URL loads and completes a real Gemini analysis; Cloud Run/Vertex proof can be shown; no API key is exposed.
  Verify: Test the URL normally and in an incognito window, inspect Cloud Run logs, and record the deployed revision and URL.

  **Participant pause 2:** Show Deepthy the public URL and request final functional confirmation.

- [ ] **10. Prepare Devpost handoff**
  Spec ref: `prd.md > Submission Proof Points`
  What to build: Gather the project story, screenshots, repository link, Cloud Run/Vertex proof, architecture image, three-to-four-minute demo outline, testing instructions, technology list, and learning notes.
  Acceptance: The participant has enough verified material to run `$prepare-submission` without inventing claims.
  Verify: Review every official required field against the actual build and confirm the next command is `$prepare-submission`.
