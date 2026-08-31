# Project Scope

## Project Name Candidates

- Data Incident Action Agent — confirmed

## One-Line Summary

A Gemini-powered incident-response agent that diagnoses a `CUSTOMER_ORDERS` schema drift, traces technical and business impact, produces a prioritised recovery plan, and drafts an approval-gated stakeholder notification.

## Target User

A data engineer responsible for diagnosing and coordinating the response to breaking upstream schema changes.

## Problem

Upstream teams can rename columns or change data types without notice. This breaks downstream transformations and dashboards, while data engineers must manually determine severity, trace impact, decide the repair order, and explain the incident to stakeholders.

## Core Workflow

1. The user opens a prefilled, editable `CUSTOMER_ORDERS` schema-drift incident.
2. The app validates the incident and combines it with a small built-in dependency catalogue.
3. Gemini 3.7 Flash analyses the technical failure and business impact.
4. The agent classifies severity, identifies affected assets, explains likely cause, and produces a prioritised recovery plan.
5. The agent generates an incident brief and one stakeholder notification draft.
6. The user explicitly approves the draft; the app records approval but sends nothing.
7. The app shows run metrics: model, latency, input/output/total tokens, and labelled estimated Gemini cost.

## What We Are Building

- One polished schema-drift scenario.
- Simple Python service using the Google GenAI SDK and Vertex AI.
- Gemini 3.7 Flash structured analysis.
- Deterministic built-in dependency data for explainable impact grounding.
- Technical diagnosis and business-impact cards with equal prominence.
- Recovery plan as the primary demo output.
- Human-approval state transition.
- Run metrics and estimated per-analysis model cost.
- Professional navy/blue data-operations control-room interface.
- Cloud Run deployment, reproducible README, architecture diagram, and short demo.

## What We Are Not Building

- Real database, dbt, DataHub, email, Slack, or ticketing integrations — cut to meet the deadline and avoid unreliable credentials.
- Automatic schema repair or message sending — cut for safety; approval is demonstrated without mutation.
- Login, multiple users, multiple incident types, persistent memory, or historical analytics — cut because they do not strengthen the single demo path enough.
- Live Google Billing integration — cut because token-based estimated cost is sufficient and easier to explain.
- A complex multi-agent system — cut in favour of one understandable agent with explicit steps.

## Inspiration And References

- DataHub lineage-style downstream impact analysis.
- Monte Carlo-style incident diagnosis and prioritisation.
- dbt contract/schema-test concepts for column and data-type failures.

## Demo Path

Detected → Analysed → Plan Ready → Awaiting Approval → Approved.

The demo begins with `customer_id` renamed to `customer_key` and `order_total` changed from numeric to string. It ends with an evidence-grounded recovery plan, stakeholder draft, approval event, and visible Cloud Run/Vertex AI proof.

## Submission Story

Data engineers lose critical time translating a raw schema failure into a coordinated response. Data Incident Action Agent uses Gemini to turn deterministic lineage evidence into an actionable technical and business recovery package, while keeping external communication behind human approval. The project demonstrates autonomous high-value work, production-minded safety, cost transparency, and deployment on Google Cloud.

## Time Budget And Definition Of Done

- Total available: approximately 3–4 hours.
- Build target: roughly 2 hours.
- Remaining time: deployment, README, architecture diagram, video, and Devpost form.
- Done means the single scenario works end-to-end on Cloud Run and can be demonstrated reliably; additional features are secondary.
