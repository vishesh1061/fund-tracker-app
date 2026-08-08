import pandas as pd
import streamlit as st

st.set_page_config(page_title="Fund Tracker", layout="wide")

SHEET_ID = "1PKfZ0ayHnYIrs9El5dkpYLkaOOg6s6yUs23O1AalQD0"
CSV_URL = (
    f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"
)


@st.cache_data(ttl=60)
def load_data():
  return pd.read_csv(CSV_URL)


try:
  df = load_data()

  st.title("Research")

  if not df.empty:
    # Clean up currency string values to numbers ($ and commas)
    for col in ["Inflow", "Outflow"]:
      if col in df.columns:
        df[col] = pd.to_numeric(
            df[col].astype(str).str.replace(r"[$,]", "", regex=True),
            errors="coerce",
        ).fillna(0)

    col1, col2, col3, col4 = st.columns(4)

    inflow = df["Inflow"].sum() if "Inflow" in df.columns else 0.0
    outflow = df["Outflow"].sum() if "Outflow" in df.columns else 0.0
    balance = inflow - outflow

    col1.metric("Current Balance", f"${balance:,.2f}")
    col2.metric("Inflow", f"${inflow:,.2f}")
    col3.metric("Outflow", f"${outflow:,.2f}")
    col4.metric("Gross Profit", "$0.00")

    st.markdown("---")
    st.subheader("Transactions Log")
    st.dataframe(df, use_container_width=True)
  else:
    st.info("Connected successfully! No transaction records found.")

except Exception as e:
  st.error(f"Error loading sheet data: {e}")
