from __future__ import annotations

import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[1] / 'data' / 'sample_telemetry.csv'
THRESHOLD_MINUTES = 30


def detect_inactive_beams(df: pd.DataFrame) -> pd.DataFrame:
    df['event_timestamp'] = pd.to_datetime(df['event_timestamp'])
    df = df.sort_values(['flight_id', 'beam_id', 'event_timestamp'])

    grouped = (
        df.groupby(['flight_id', 'beam_id'])['event_timestamp']
        .max()
        .reset_index(name='last_seen')
    )

    latest_overall = df['event_timestamp'].max()
    grouped['gap_minutes'] = (latest_overall - grouped['last_seen']).dt.total_seconds() / 60
    anomalies = grouped[grouped['gap_minutes'] >= THRESHOLD_MINUTES].copy()
    anomalies['anomaly_type'] = 'INACTIVE_BEAM'
    return anomalies.sort_values('gap_minutes', ascending=False)


if __name__ == '__main__':
    df = pd.read_csv(DATA_PATH)
    anomalies = detect_inactive_beams(df)

    print('Detected anomalies')
    print('-' * 80)
    if anomalies.empty:
        print('No inactive beams detected.')
    else:
        print(anomalies.to_string(index=False))
