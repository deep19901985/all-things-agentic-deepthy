# Product Requirements Document

## Product Summary

Data Incident Action Agent helps a data engineer convert raw schema-drift evidence into a coordinated incident response. The user reviews an editable `CUSTOMER_ORDERS` incident, asks the agent to analyse it, and receives a grounded technical diagnosis, downstream impact assessment, prioritised recovery plan, incident brief, and stakeholder notification draft. The agent does meaningful analysis autonomously while keeping outward action behind explicit human approval.

The product is a focused proof of concept for one reliable incident path. Its emotional promise is calm control during a disruptive data failure: the interface should make the engineer feel that the problem has been contained, understood, and converted into clear next actions.

## Target User

The primary user is an on-call data engineer or analytics engineer responsible for responding to upstream changes that break transformations and business dashboards. They understand tables, columns, data types, dependencies, and recovery steps, but need to diagnose and communicate the incident quickly.

## Core User Journey

1. The user opens the application and immediately sees a detected, high-attention schema-drift incident.
2. The incident description is prefilled and editable. It states that `customer_id` was renamed to `customer_key` and `order_total` changed from numeric to string in `CUSTOMER_ORDERS`.
3. The user selects **Analyse Incident**.
4. The interface disables duplicate analysis and visibly progresses through analysis stages.
5. The application displays technical diagnosis and business impact with equal prominence.
6. The application identifies affected assets using supplied demo dependency evidence and explains why each asset is affected.
7. The application presents the recovery plan as the hero result, with ordered priorities and responsible roles.
8. The application displays an incident brief and a concise stakeholder notification draft.
9. The notification is marked **Awaiting approval**. Nothing has been sent.
10. The user selects **Approve Notification**.
11. The product records a green approval banner and timestamp while clearly stating that approval is simulated and nothing was sent.
12. Run metrics show the Gemini model, latency, token usage, total tokens, and labelled estimated cost.

## Epics And User Stories

### Epic 1: Review and initiate an incident

- As a data engineer, I want to see a detected schema-drift incident immediately so that I understand what triggered the response.
- As a data engineer, I want to edit the incident description so that I can correct or add context before analysis.
- As a data engineer, I want one obvious analysis action so that the workflow is unambiguous.

Acceptance criteria:

- The initial status visibly reads **Detected** and **High attention required**.
- The incident text contains the table, renamed column, and changed data type.
- The incident text is editable.
- **Analyse Incident** is the primary action.
- Blank or very short input produces a visible validation message and does not start analysis.

### Epic 2: Understand technical and business impact

- As a data engineer, I want a concise diagnosis so that I can understand the likely failure mechanism.
- As a data engineer, I want impacted assets with evidence so that the result is traceable rather than generic.
- As a data engineer, I want technical and business consequences separated so that I can communicate to different audiences.

Acceptance criteria:

- The diagnosis names `CUSTOMER_ORDERS`, `customer_id/customer_key`, and the `order_total` type mismatch.
- Severity is visible and accompanied by a short rationale.
- Each impacted asset displays its name, type, and reason for impact.
- The interface includes at least one transformation and two business-facing dashboards.
- Technical diagnosis and business impact appear as equally prominent cards.
- The interface identifies the dependency catalogue as demo evidence rather than live lineage.

### Epic 3: Produce a prioritised recovery plan

- As a data engineer, I want ordered remediation steps so that I know what to fix first.
- As a data engineer, I want every step to show a priority and suggested owner so that the response can be coordinated.
- As a data engineer, I want validation steps so that I can determine when service is restored.

Acceptance criteria:

- The recovery plan is the most visually prominent result.
- The plan contains a short ordered sequence rather than an unstructured paragraph.
- Each action includes a priority such as P0/P1/P2 and a suggested owner.
- The plan addresses schema compatibility, transformation repair, data validation, dashboard verification, and stakeholder communication.
- The plan distinguishes immediate containment from follow-up prevention.

### Epic 4: Prepare controlled communication

- As a data engineer, I want an incident brief so that the technical record is captured.
- As a data engineer, I want a plain-language stakeholder draft so that I do not have to translate the incident manually.
- As a responsible operator, I want approval before outward action so that the agent cannot communicate without oversight.

Acceptance criteria:

- The incident brief includes status, severity, cause, impact, and recovery summary.
- The stakeholder draft avoids unnecessary technical jargon and clearly describes business impact.
- Before approval, the notification displays **Awaiting approval**.
- The approval button is unavailable until a successful analysis exists.
- After approval, the card displays a green banner and timestamp.
- The interface explicitly says **Simulation only—nothing was sent**.
- Editing or running a new incident clears any previous approval.

### Epic 5: Show trustworthy execution

- As a data engineer, I want visible processing state so that I know the application is working.
- As a reviewer, I want operational metrics so that I can evaluate cost and runtime awareness.
- As a user, I want honest failure handling so that the product never presents fabricated analysis.

Acceptance criteria:

- Duplicate analysis actions are disabled while a run is active.
- The workflow visibly transitions through Detected, Analysed, Plan Ready, Awaiting Approval, and Approved.
- Metrics show Gemini 3.7 Flash, latency, input tokens, output tokens, total tokens, and **Estimated cost**.
- Estimated cost is clearly labelled and not represented as a live billing charge.
- If the model call fails, the application shows an understandable error and a **Retry** action.
- A failed call does not populate result cards with placeholder or invented model output.

## Edge Cases

- **Empty incident:** analysis is blocked with guidance to enter a meaningful incident.
- **Duplicate click:** the analysis control is disabled during execution.
- **Model or network failure:** existing input remains; no results are invented; retry is offered.
- **Incomplete model output:** the product reports that structured analysis could not be validated and offers retry.
- **New run after approval:** previous results, timestamp, and approval state are cleared.
- **Very long edited input:** the app may limit input length and explains the limit.
- **Cost unavailable:** token metrics remain visible when available; estimated cost shows unavailable rather than zero.

## What We Are Building

- Anonymous single-session experience.
- One editable schema-drift scenario.
- One autonomous analysis action.
- Structured result cards for diagnosis, impact, recovery, incident brief, communication, and metrics.
- One simulated approval action.
- Professional navy/blue control-room visual design.
- A complete, reliable path suitable for a short demo.

## What We Would Add With More Time

- Live DataHub/dbt/catalogue integration for real lineage.
- Database schema comparison and contract validation.
- Slack, email, PagerDuty, or Jira integrations after approval.
- Persistent incident history, authentication, and team collaboration.
- Multiple incident templates and free-form asset discovery.
- Feedback loops, long-term memory, observability dashboards, and automated evaluation.

These are excluded because the current product must be deployable and demonstrable within a 3–4 hour total budget.

## Submission Proof Points

- Gemini performs the high-value reasoning rather than serving as a generic chatbot.
- Deterministic dependency evidence grounds the analysis.
- The recovery plan demonstrates autonomous operational utility.
- Explicit human approval demonstrates a production-minded safety boundary.
- Structured errors and state clearing demonstrate reliability.
- Token, cost, and latency metrics demonstrate operational awareness.
- The Cloud Run URL and Vertex AI evidence prove Google Cloud deployment.
- The single scenario is coherent, reproducible, and easy for judges to understand.
