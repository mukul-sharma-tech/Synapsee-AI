import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


# ---------- SAFE CSV LOADER ---------- #
def load_trends_csv(uploaded_file):
    """
    Loads Google Trends CSV safely, skipping metadata lines.
    """
    try:
        df = pd.read_csv(uploaded_file, skiprows=1)  # Skip first line 'Category: ...'
    except Exception as e:
        st.error(f"CSV read error: {e}")
        return None

    # Ensure there are at least 2 columns
    if df.shape[1] < 2:
        return None

    # Rename columns for consistency
    df.columns = ["date", "value"]

    # Convert types
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    df = df.dropna()

    if df.empty:
        return None

    return df

# ---------- DEMAND PLOT ---------- #
def plot_demand(df):
    st.subheader("📈 Demand & Seasonality")

    if df is None or df.empty:
        st.warning("No numeric demand data found in Google Trends file.")
        return

    fig, ax = plt.subplots()
    ax.plot(df["date"], df["value"], marker="o")
    ax.set_xlabel("Date")
    ax.set_ylabel("Search Interest Index")
    ax.set_title("Google Trends – Demand Over Time")
    ax.grid(True)

    st.pyplot(fig)


# ---------- DEMAND ANALYSIS ---------- #
def analyze_trends(df):
    if df is None or df.empty:
        return {
            "peak": None,
            "trend": "Insufficient data",
            "timing": "Unknown"
        }

    peak = int(df["value"].max())
    peak_date = df.loc[df["value"].idxmax(), "date"].strftime("%b %Y")

    trend = "Increasing" if df["value"].iloc[-1] > df["value"].iloc[0] else "Seasonal / Declining"

    timing = "Pre-winter (Sep–Oct)" if peak >= 50 else "Low seasonal impact"

    return {
        "peak": peak,
        "peak_date": peak_date,
        "trend": trend,
        "timing": timing
    }
