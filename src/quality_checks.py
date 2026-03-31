from __future__ import annotations

import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[1] / 'data' / 'sample_telemetry.csv'


def run_checks(df: pd.DataFrame) -> dict[str, int]:
    results = {
        'null_flight_id': int(df['flight_id'].isna().sum()),
        'null_beam_id': int(df['beam_id'].isna().sum()),
        'duplicate_rows': int(df.duplicated().sum()),
        'invalid_latitude': int(((df['latitude'] < -90) | (df['latitude'] > 90)).sum()),
        'invalid_longitude': int(((df['longitude'] < -180) | (df['longitude'] > 180)).sum()),
    }
    return results


if __name__ == '__main__':
    df = pd.read_csv(DATA_PATH)
    summary = run_checks(df)
    print('Data Quality Summary')
    print('-' * 40)
    for key, value in summary.items():
        print(f'{key}: {value}')
