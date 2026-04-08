# Engineering for Data & AI — Coursework Proposal

## 1. Course Objective

Each group will design **and implement (code)** an end-to-end **Data + AI system** in a domain of your choice.

Examples of domains:
- e-commerce
- logistics
- healthcare
- finance
- education
- IoT/smart city

E-commerce is only a reference example. You may choose another domain if the same engineering requirements are covered.

Students can review reference materials in `coursework/sample_design` before starting their own design.

---

## 2. What Students Need to Build

Your coursework follows three core parts plus one AI track. Each part requires design + code artifacts.

1. **Data Generator Design**
	- Design offline and streaming datasets with clear grain and schema.
	- Inject realistic data issues (required + optional).
	- Keep generator configurable by parameters.
	- Implement generator code and produce sample outputs.

2. **Gold Layer Schema Design**
	- Design business-ready Gold tables (facts, dimensions, optional OBT/aggregates).
	- Define refresh SLAs and data quality checks.
	- Define feature tables for ML with point-in-time correctness and dedup strategy.
	- Implement schema/table creation and transformation code.

3. **Drift Design + Track-Specific Gold Tables**
	- Add at least one feature drift scenario.
	- **If ML track (4A):** create Gold label table and Gold training table.
	- **If LLM track (4B):** training table is optional; create Gold LLM knowledge/evaluation tables instead.
	- Implement drift injection and table build code.

4. **Choose One AI Design Track (either 4A or 4B)**
	- **4A ML System Design**
		- High-level design: model lifecycle and system decisions.
		- Low-level design: core classes/interfaces and responsibilities.
		- Define split strategy, baseline model, metrics, serving, and monitoring.
		- Implement training, scoring, monitoring, and retraining code.
	- **4B LLM/Agent System Design**
		- Design an LLM use case in the same domain.
		- Include RAG/knowledge sources, agent/tool flow, safety, and observability.
		- Define serving pattern and evaluation plan.
		- Implement agent workflow, retrieval/prompt flow, and monitoring code.

---

## 3. Required Data Challenges

### Offline (required)
- Data skew
- High cardinality
- Schema evolution

### Streaming (required)
- Bursty traffic
- Late arrivals

### Optional (choose at least one)
- Duplicate records/events
- Missing/null values
- Out-of-order events
- Inconsistent formats

---

## 4. Timestamp and Join Rules

Use consistent time semantics across your pipeline:
- `event_timestamp`: business event time, used for point-in-time joins
- `created_ts`: row creation time, used for dedup

For ML track (4A):
- label table has no features
- training table = label table + feature tables (joined by entity + `event_timestamp`)

For LLM track (4B):
- training table is not required
- use knowledge and evaluation tables (for example chunks, query logs, feedback)

---

## 5. Quality, Reliability, and Security Expectations

Students should explain key design decisions for:
- CI/CD approach
- versioning (data/features/models/config)
- security (auth, RBAC, secrets, encryption)
- resilience in distributed systems (retry, idempotency, checkpointing, recovery)
- observability (logs, metrics, traces)

---

## 6. Deliverables

Submit both **design documents** and **working code** for these sections:

1. **01 Data Generator Design**
2. **02 Gold Schema Design**
3. **03 Drift + Track-Specific Data Design**
4. **Choose one:**
	- **04 ML Design (HLD + LLD)**, or
	- **05 LLM/Agent Design (HLD + LLD)**

Each submitted section should include:
- key assumptions
- key design decisions and trade-offs
- expected outputs/tables
- how you will monitor quality and reliability

Minimum code evidence:
- runnable scripts/notebooks/services for implemented steps
- sample output files/tables
- short run instructions (how to execute)

Note:
- ML track: perfect label correctness is not required, but clear and consistent label logic is highly appreciated.
- LLM track: quality of knowledge sources, retrieval design, and evaluation logic is highly appreciated.

---

## 7. Coursework Phasing

Work is split into two phases:

1. **Mini-coursework phase**
	- Complete Section 01 (Data Generator Design)
	- Complete Section 02 (Gold Schema Design)
	- Submit design docs + code for 01 and 02

2. **Final coursework phase**
	- Complete Section 03 (Drift + Track-Specific Data Design)
	- Complete one AI track:
		- Section 04 (ML Design), or
		- Section 05 (LLM/Agent Design)
	- Submit design docs + code for the completed sections

This phased plan ensures the data foundation is finished first, then extended into ML or LLM system design.