# E-commerce ML Design

## 1. Goal

Build a simple ML use case on top of Gold data and feature tables.

**Suggested task:** predict whether a customer will purchase in the next session.

**Why this task:** it uses offline + streaming features and is easy to explain.

---

## 2. Prediction Setup

**Entity:** customer_id

**Label:** `will_purchase_next_session` (1 = yes, 0 = no)

**Prediction time:** use the feature snapshot at `event_timestamp`.

**Training rule:** do not use data after the prediction time.

---

## 3. High-Level ML Design

End-to-end flow:
1. Use Gold feature tables and Gold label table from 02 and 03.
2. Use `ml_customer_purchase_training` as the model input.
3. Train and evaluate a baseline classifier.
4. Publish prediction scores for batch or near-real-time use.
5. Monitor drift, logs, metrics, and traces.

Other flows:
- **CI/CD:** automate test, train, validate, and deploy steps in a repeatable pipeline.
- **Versioning:** version data snapshots, features, model artifacts, and config files.

Example of high level ML system designs: https://fullstackdatascience.com/hall-of-fame

Student note: students should also explain your key design decisions for security, resilience, training/inference pattern, storage, and routing/gateway.

---

## 4. Low-Level ML Design

When we talk about Low-Level Design (LLD) for Machine Learning, we move away from abstract boxes like "Model" or "Database" and focus on class structures, code interfaces, and data schemas that make the system maintainable.

In the world of Machine Learning, LLD is where you decide exactly how your code will handle the "three pillars" of production AI: Data, Models, and Pipelines. Here below is example of LLD for this ecommerce task.

Use 5 key classes. Each class can have multiple functions.

```python
class TrainingDataService:
    def read_training_table(self) -> DataFrame: ...
    def validate_schema(self, df: DataFrame) -> None: ...
    def dedup_by_created_ts(self, df: DataFrame) -> DataFrame: ...

class SplitService:
    def get_split_boundaries(self, df: DataFrame) -> dict: ...
    def split_by_time(self, df: DataFrame) -> tuple[DataFrame, DataFrame, DataFrame]: ...

class ModelService:
    def train(self, train_df: DataFrame) -> ModelArtifact: ...
    def evaluate(self, model: ModelArtifact, test_df: DataFrame) -> dict: ...
    def save_model(self, model: ModelArtifact, model_version: str) -> None: ...

class ScoringService:
    def score_batch(self, model: ModelArtifact, df: DataFrame) -> DataFrame: ...
    def write_scores(self, score_df: DataFrame, model_version: str) -> None: ...

class MonitoringService:
    def publish_model_metrics(self, metrics: dict) -> None: ...
    def publish_drift_metrics(self, drift_stats: dict) -> None: ...
    def trigger_alerts(self, metrics: dict) -> None: ...
```

---

## 5. Training Table

Training table: `ml_customer_purchase_training`

This table is already created in 03_data_generator_with_drift.md (Gold zone).

**Grain:** one row per customer_id per timestamp.

**Columns:**
- customer_id
- event_timestamp
- created_ts
- label
- feature columns from the Gold feature tables

**Use:** this is the input table for model training in this document.

---

## 6. Split Strategy

For some cases, we must use a time-based split:
- Train: older data
- Validation: middle period
- Test: latest period

Do not use a random split.

---

## 7. Baseline Model

Start with a simple model:
- Logistic Regression
- Decision Tree if you want another simple option

Keep the first version small.

---

## 8. Metrics

Use classification metrics:
- Precision
- Recall
- F1

Start with F1.

---

## 9. Serving Design

**Offline scoring:** batch score daily.

**Near-real-time scoring:** join the latest streaming features with the latest offline snapshot.

**Serving output:** customer_id, score, model_version, score_ts

---

## 10. Monitoring

Monitor three things:
- data drift in key features
- prediction drift in model scores
- label drift in conversion rate

Also monitor:
- logs for errors and warnings
- metrics for model and system behavior
- traces for request flow and latency

Add simple alerts when values change too much.

---

## 11. Retraining Strategy

Use a simple retraining policy:
- Scheduled retrain: once per week (or once per month for stable data).
- Triggered retrain: retrain when drift or model quality crosses threshold.

Example triggers:
- feature drift alert stays high for multiple days
- F1 drops below agreed baseline
- data volume/seasonality changes significantly

Operational rules:
- Train candidate model on latest training window.
- Compare candidate vs current production model.
- Promote only if candidate is better and passes quality checks.
- Keep rollback path to previous `model_version`.

---

## 12. Deliverables

1. Use `ml_customer_purchase_training` from 03 (Gold zone) as model input.
2. High-Level ML design: end-to-end flow + key decisions for CI/CD, versioning, security, resilience, training/inference pattern, storage, and routing/gateway.
3. Low-Level ML design: propose key classes/interfaces (about 5 core classes is enough) and explain responsibilities.
4. Model plan: split strategy, baseline model choice, and evaluation metrics.
5. Serving, monitoring, and retraining plan: scoring output, drift checks, observability (logs, metrics, traces), and retrain/rollback policy.