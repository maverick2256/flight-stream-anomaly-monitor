from __future__ import annotations

import csv
import random
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path

OUTPUT_PATH = Path(__file__).resolve().parents[1] / 'data' / 'sample_telemetry.csv'

@dataclass
class TelemetryEvent:
    flight_id: str
    beam_id: str
    event_timestamp: str
    latitude: float
    longitude: float
    altitude: int
    status: str


def generate_events(num_flights: int = 5, events_per_flight: int = 24) -> list[TelemetryEvent]:
    now = datetime.utcnow().replace(second=0, microsecond=0)
    events: list[TelemetryEvent] = []

    for i in range(1, num_flights + 1):
        flight_id = f"FLIGHT_{100 + i}"
        beam_id = f"BEAM_{i}"
        start_time = now - timedelta(minutes=90)

        for j in range(events_per_flight):
            # Create an inactivity gap for one flight to simulate anomaly.
            if flight_id == 'FLIGHT_103' and 10 <= j <= 15:
                start_time += timedelta(minutes=8)
            else:
                start_time += timedelta(minutes=random.choice([2, 3, 4]))

            event = TelemetryEvent(
                flight_id=flight_id,
                beam_id=beam_id,
                event_timestamp=start_time.isoformat(),
                latitude=round(random.uniform(-80, 80), 6),
                longitude=round(random.uniform(-170, 170), 6),
                altitude=random.randint(28000, 39000),
                status=random.choice(['ACTIVE', 'ACTIVE', 'ACTIVE', 'DEGRADED']),
            )
            events.append(event)

    return sorted(events, key=lambda e: e.event_timestamp)


def write_csv(events: list[TelemetryEvent]) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open('w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=list(asdict(events[0]).keys()))
        writer.writeheader()
        for event in events:
            writer.writerow(asdict(event))


if __name__ == '__main__':
    data = generate_events()
    write_csv(data)
    print(f'Generated {len(data)} telemetry events at {OUTPUT_PATH}')
