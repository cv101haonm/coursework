# E-commerce LLM Design

## 1. Goal

Design a simple LLM use case for e-commerce.

Suggested use case:
- customer support assistant for order and product questions

Main outcomes:
- answer user questions with grounded data
- reduce hallucination with retrieval and guardrails
- log and monitor quality, latency, and safety

---

## 2. High-Level Agentic LLM Design

End-to-end flow:
1. User sends a question.
2. Gateway authenticates and routes request.
3. Agent decides intent (simple answer vs tool call).
4. Planner creates steps (retrieve data, reason, answer).
5. Tool executor runs allowed tools (search, SQL/read-only table lookup, policy lookup).
6. Prompt builder composes system prompt + user question + tool outputs.
7. LLM generates answer.
8. Safety layer checks output.
9. Response is returned and logged.

Key decisions students should explain:
- model choice (hosted API vs self-hosted)
- agent pattern (single-agent vs planner-executor)
- tool policy (which tools are allowed, timeout, retry)
- retrieval strategy (dense, sparse or hybrid search)
- latency/cost trade-off
- safety and compliance controls
- fallback behavior when confidence is low

---

## 3. Data and Knowledge Sources

Use trusted sources only:
- product catalog and policy docs
- FAQ and support playbooks
- selected Gold tables (read-only views)

Recommended table pattern in Gold:
- `llm_knowledge_chunks` (chunk_id, source_type, source_id, content, updated_ts)
- `llm_query_logs` (request_id, user_id, prompt_hash, response_hash, latency_ms, created_ts)
- `llm_feedback` (request_id, rating, comment, created_ts)

---

## 4. Low-Level Agent Design

Move from abstract blocks to concrete interfaces and schemas.

Example key classes:

```python
class AgentOrchestrator:
    def handle_request(self, user_id: str, question: str) -> dict: ...
    def finalize_response(self, result: dict) -> dict: ...

class PlannerService:
    def classify_intent(self, question: str) -> str: ...
    def build_plan(self, question: str) -> list[dict]: ...

class ToolExecutor:
    def execute_step(self, step: dict) -> dict: ...
    def run_with_timeout(self, step: dict, timeout_s: int) -> dict: ...

class RetrievalService:
    def search(self, query: str, top_k: int) -> list[dict]: ...
    def rerank(self, query: str, docs: list[dict]) -> list[dict]: ...

class PromptService:
    def build_system_prompt(self) -> str: ...
    def build_user_prompt(self, question: str, context: list[dict]) -> str: ...

class LLMService:
    def generate(self, prompt: str) -> dict: ...
    def estimate_tokens(self, prompt: str) -> int: ...

class MemoryService:
    def get_session_context(self, user_id: str) -> dict: ...
    def save_turn(self, user_id: str, turn: dict) -> None: ...

class SafetyService:
    def validate_input(self, question: str) -> None: ...
    def validate_output(self, answer: str) -> None: ...

class EvaluationService:
    def score_grounding(self, answer: str, sources: list[dict]) -> float: ...
    def score_helpfulness(self, answer: str) -> float: ...

class ObservabilityService:
    def log_request(self, payload: dict) -> None: ...
    def publish_metrics(self, metrics: dict) -> None: ...
```

---

## 5. Prompt, RAG, and Agent Pattern

Simple prompt structure:
- system prompt: role, policy, and tone
- context block: retrieved chunks with source ids
- user prompt: question

Simple agent loop:
1. planner creates steps
2. tool executor runs steps
3. prompt service builds final prompt
4. LLM generates answer
5. evaluator/safety checks before returning output

Response rules:
- cite source ids when possible
- if confidence is low, say "I do not have enough context"
- do not invent order status, prices, or policy details

---

## 6. Serving Pattern

Recommended start:
- synchronous API for chat requests
- cache frequent queries
- timeout and retry policy

Scale options:
- async queue for long tasks
- model fallback chain (small model -> larger model)

---

## 7. Security and Safety

Minimum controls:
- API auth and RBAC
- secret management for model keys
- PII masking in logs
- prompt injection checks
- output filtering for harmful or policy-violating content

---

## 8. Monitoring

Track:
- quality: answer helpfulness and user rating
- reliability: error rate and timeout rate
- performance: p95 latency and throughput
- cost: token usage by route and model
- safety: blocked prompts and blocked outputs

Also collect:
- logs, metrics, traces

---

## 9. Evaluation

Evaluate with:
- offline test set (known Q&A)
- retrieval quality (precision@k)
- response quality review rubric
- safety checks (prompt injection and policy tests)

---

## 10. Deliverables

1. Use trusted knowledge sources (for example `llm_knowledge_chunks`) as LLM context input.
2. High-level LLM/agent design: end-to-end flow + key decisions for model choice, tool policy, and fallback behavior.
3. Low-level design: propose key classes/interfaces (about 5 core classes is enough) and explain responsibilities.
4. Prompt + RAG + agent execution plan: retrieval, context building, response rules, and guardrails.
5. Serving, monitoring, and evaluation plan: latency/cost targets, logs/metrics/traces, and quality/safety checks.
