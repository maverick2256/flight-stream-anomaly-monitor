-- Count anomalies by day
SELECT event_date, COUNT(*) AS anomaly_count
FROM curated.flight_telemetry t
JOIN curated.flight_anomalies a
  ON t.flight_id = a.flight_id
 AND t.beam_id = a.beam_id
GROUP BY event_date
ORDER BY event_date DESC;

-- Most frequently inactive beams
SELECT beam_id, COUNT(*) AS occurrences
FROM curated.flight_anomalies
GROUP BY beam_id
ORDER BY occurrences DESC
LIMIT 20;

-- Flights with latest anomaly timestamps
SELECT flight_id, MAX(detected_at) AS latest_anomaly_time
FROM curated.flight_anomalies
GROUP BY flight_id
ORDER BY latest_anomaly_time DESC;
