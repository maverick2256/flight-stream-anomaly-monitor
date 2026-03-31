# Architecture Notes

## Goal
Detect inactive flight beams in near real time and alert operations before downstream SLAs are breached.

## Data flow

### 1. Producer layer
A telemetry producer emits records such as:
- flight_id
- beam_id
- event_timestamp
- altitude
- latitude
- longitude
- status

### 2. Streaming ingestion
Telemetry events are pushed into Amazon Kinesis Data Streams.

### 3. Real-time processing
Managed Apache Flink consumes events, groups them by flight and beam, and checks whether the gap since the last event exceeds the business threshold.

### 4. Alert routing
When inactivity is detected, a compact anomaly event is pushed downstream and handled by Lambda for:
- SNS email alerts
- webhook-based notifications
- incident logging

### 5. Storage and analytics
Raw telemetry lands in S3. Glue transforms JSON/CSV into partitioned Parquet. Curated datasets are queried in Redshift or Athena for operational dashboards.

## Data quality rules
- flight_id must not be null
- beam_id must not be null
- event_timestamp must be parseable
- event_timestamp cannot be in the future beyond tolerance
- coordinates must be within valid geographic ranges
- duplicate events should be flagged

## Interview talking points

### Why Kinesis?
Managed, scalable streaming ingestion with low operational overhead.

### Why Flink?
Strong support for stateful stream processing and rolling window anomaly logic.

### Why Glue + Parquet?
Efficient transformation, partitioning, and analytics performance optimization.

### Why Lambda for alerts?
Simple event-driven integration for lightweight notification fan-out.

## Production hardening ideas
- schema registry
- dead-letter queue for malformed events
- replay mechanism for failed windows
- CloudWatch dashboards and alarms
- IAM least privilege policies
- backfill support for missed telemetry

