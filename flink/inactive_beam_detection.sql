-- Example Flink SQL logic for detecting beam inactivity.
-- This is illustrative portfolio code, not a fully deployed production script.

CREATE TABLE telemetry_stream (
    flight_id STRING,
    beam_id STRING,
    event_timestamp TIMESTAMP(3),
    status STRING,
    WATERMARK FOR event_timestamp AS event_timestamp - INTERVAL '5' SECOND
) WITH (
    'connector' = 'kinesis',
    'stream' = 'flight-telemetry-stream',
    'aws.region' = 'us-east-1',
    'format' = 'json'
);

CREATE TABLE anomaly_sink (
    flight_id STRING,
    beam_id STRING,
    last_seen TIMESTAMP(3),
    gap_minutes BIGINT,
    anomaly_type STRING
) WITH (
    'connector' = 'kinesis',
    'stream' = 'flight-anomaly-stream',
    'aws.region' = 'us-east-1',
    'format' = 'json'
);

INSERT INTO anomaly_sink
SELECT
    flight_id,
    beam_id,
    MAX(event_timestamp) AS last_seen,
    TIMESTAMPDIFF(MINUTE, MAX(event_timestamp), CURRENT_TIMESTAMP) AS gap_minutes,
    'INACTIVE_BEAM' AS anomaly_type
FROM telemetry_stream
GROUP BY flight_id, beam_id
HAVING TIMESTAMPDIFF(MINUTE, MAX(event_timestamp), CURRENT_TIMESTAMP) >= 30;
