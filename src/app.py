from __future__ import annotations

from pathlib import Path
import pandas as pd
import streamlit as st

from simulate_pipeline import detect_inactive_beams

DATA_PATH = Path(__file__).resolve().parents[1] / 'data' / 'sample_telemetry.csv'

st.set_page_config(page_title='Flight Stream Anomaly Monitor', layout='wide')
st.title('Flight Stream Anomaly Monitor')
st.caption('Portfolio dashboard for real-time telemetry anomaly detection')

telemetry = pd.read_csv(DATA_PATH)
anomalies = detect_inactive_beams(telemetry.copy())

col1, col2, col3 = st.columns(3)
col1.metric('Total Events', len(telemetry))
col2.metric('Flights', telemetry['flight_id'].nunique())
col3.metric('Inactive Beams', len(anomalies))

st.subheader('Recent Telemetry')
st.dataframe(telemetry.tail(20), use_container_width=True)

st.subheader('Detected Inactive Beams')
if anomalies.empty:
    st.success('No anomalies detected in current sample.')
else:
    st.dataframe(anomalies, use_container_width=True)
