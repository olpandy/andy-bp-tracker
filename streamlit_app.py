import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.io as pio

st.set_page_config(page_title="Andy BP Tracker", layout="centered")

st.title("Andy Blood Pressure Tracker")

st.markdown("Upload your blood pressure CSV or use sample data to view trends, tables, and export PDFs.")

# ---------- Sample data ----------
def generate_sample_data():
    days = 14
    dates = [datetime.today() - timedelta(days=i) for i in range(days)][::-1]
    np.random.seed(42)
    systolic = np.random.normal(125, 8, days).astype(int)
    diastolic = np.random.normal(80, 5, days).astype(int)
    return pd.DataFrame({
        "Date": dates,
        "Systolic": systolic,
        "Diastolic": diastolic
    })

# ---------- Input: CSV upload ----------
st.subheader("Upload CSV (Date, Systolic, Diastolic)")

uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"], label_visibility="collapsed")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"])
        else:
            st.error("CSV must contain a 'Date' column.")
            df = generate_sample_data()
    except Exception:
        st.error("Could not read CSV. Using sample data instead.")
        df = generate_sample_data()
else:
    df = generate_sample_data()
    st.info("No file uploaded. Showing sample data.")

# ---------- Chart ----------
st.subheader("Blood Pressure Over Time")

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df["Date"], y=df["Systolic"],
    mode="lines+markers", name="Systolic (mmHg)"
))
fig.add_trace(go.Scatter(
    x=df["Date"], y=df["Diastolic"],
    mode="lines+markers", name="Diastolic (mmHg)"
))

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Blood Pressure (mmHg)",
    hovermode="x unified",
    margin=dict(l=40, r=20, t=40, b=40),
    height=450
)

st.plotly_chart(fig, use_container_width=True)

# ---------- Table ----------
st.subheader("Data Table")
st.dataframe(df, use_container_width=True)

# ---------- Download chart as PDF ----------
st.subheader("Export")

if st.button("Download chart as PDF"):
    pdf_bytes = pio.to_image(fig, format="pdf")
    st.download_button(
        label="Click to download chart PDF",
        data=pdf_bytes,
        file_name="blood_pressure_chart.pdf",
        mime="application/pdf"
    )

st.markdown(
    """
    **Full dashboard PDF:**  
    Use your browser’s **Print → Save as PDF** to capture the entire page.

    **CSV format example**

    ```text
    Date,Systolic,Diastolic
    2026-05-01,128,82
    2026-05-02,131,85
    2026-05-03,122,78
    ```
    """
)
