# E-commerce Gold Zone Schema Design

## 1. Overview

Business-ready Gold model for analytics and BI.

**Approach:** Fact-Dimension + OBT + Optional aggregates/features.

**Schema:** `gold_ecommerce` with naming: `dim_`, `fact_`, `obt_`, `feat_` prefix.

---

## 2. Dimension Tables

| Dimension | Grain | Key Columns |
|-----------|-------|------------|
| dim_customer | one per customer | customer_key (SK), customer_id (BK), signup_ts, country, segment, marketing_opt_in |
| dim_product | one per product | product_key (SK), product_id (BK), category, brand, base_price, is_active, created_ts |
| dim_date | one per date | date_key (yyyymmdd), calendar_date, day_of_week, month, year, is_weekend |
| dim_payment_method | one per method | payment_method_key (SK), payment_method (name) |
| dim_order_status | one per status | order_status_key (SK), order_status (name) |

**Notes:**
- Use SCD2 (valid_from_ts, valid_to_ts, is_current) if attributes change over time.
- SK = surrogate key (data warehouse-generated), BK = business key (natural identifier).

---

## 3. Fact Tables

### 3.1 fact_order
**Grain:** one per order. **Keys:** customer_key, order_date_key, order_status_key.  
**Measures:** order_gross_amount, order_discount_amount, order_net_amount, item_count.  
**Note:** Handles schema evolution (old orders missing coupon_code, shipping_method).

### 3.2 fact_order_item
**Grain:** one per line item. **Keys:** customer_key, product_key, order_date_key.  
**Measures:** quantity, unit_price, discount_amount, line_net_amount.  
**Note:** Apply deduplication before load (2% duplicate rate from source).

### 3.3 fact_payment_attempt
**Grain:** one per payment. **Keys:** customer_key, payment_date_key, payment_method_key.  
**Measures:** amount, is_payment_success (0/1), is_payment_failed (0/1).

---

## 4. OBT Table

### 4.1 obt_order_performance
**Grain:** one per order
**Purpose:** Denormalized table for BI queries.  
**Columns:** order_id, customer_id, order_timestamp, country, segment, total_quantity, order_net_amount, payment_status_last, shipping_city, coupon_code (+ needed fact/dimension columns).

---

## 5. Refresh & Data Quality

**Refresh SLAs:**
- Dimensions: daily (or real-time if attributes change)
- Facts: incremental append/merge every 15-30 minutes
- OBT: merge by order_id every 15-30 minutes

*Note:* SLA (Service Level Agreement) is basically an agreed target for service quality, such as freshness, latency, availability, and reliability.

**Quality checks:**
- Uniqueness: order_id, order_item_id, payment_id per fact table
- Referential: facts link to dimensions
- Total match check: sum(line_net_amount) should be close to order_net_amount
- Duplicate check: monitor order_items before and after dedup
- Null check: required keys/measures should stay filled

---

## 6. Feature Store

Keep ML features in Gold:

Each feature row should include `event_timestamp` for point-in-time joins and `created_ts` for dedup.

**Feature tables:**
1. `feat_customer_90d` (grain: customer_id, event_timestamp)
   - f_customer_total_orders_90d, f_customer_avg_order_value_90d, f_customer_distinct_categories_90d
2. `feat_stream_60m` (grain: customer_id, event_timestamp)
   - f_stream_views_30m, f_stream_add_to_cart_30m, f_stream_cart_to_purchase_ratio_60m
3. `feat_customer_unified` (grain: customer_id, event_timestamp)
   - Join offline + streaming for training/scoring

**Point-in-time correctness:** Do not use feature data later than the label/reference timestamp.

**Dedup note:** use `created_ts` to keep the latest row when multiple rows share the same entity key and `event_timestamp`.

**Refresh:** 15-60 min (feat_90d), 1-5 min (feat_stream), 5-15 min (unified).