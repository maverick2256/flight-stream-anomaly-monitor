CREATE TABLE IF NOT EXISTS curated.flight_telemetry (
    flight_id        VARCHAR(50),
    beam_id          VARCHAR(50),
    event_timestamp  TIMESTAMP,
    latitude         DECIMAL(9,6),
    longitude        DECIMAL(9,6),
    altitude         INTEGER,
    status           VARCHAR(30),
    event_date       DATE
);

CREATE TABLE IF NOT EXISTS curated.flight_anomalies (
    flight_id        VARCHAR(50),
    beam_id          VARCHAR(50),
    last_seen        TIMESTAMP,
    gap_minutes      INTEGER,
    anomaly_type     VARCHAR(50),
    detected_at      TIMESTAMP DEFAULT GETDATE()
);
