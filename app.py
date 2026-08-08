import pandas as pd
import streamlit as st

st.set_page_config(page_title="Fund Tracker", layout="wide")

SHEET_ID = "1PKfZ0ayHnYIrs9EI5dkpYLkaOOg6s6yUs23O1AalQD0"
CSV_URL = (
    f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"
)


@st.cache_data(ttl=60)
def load_data():
  return pd.read_csv(CSV_URL)


try:
  raw_df = load_data()

  st.title("Research")

  # 1. Separate Transactions Log (Columns A to F)
  tx_cols = [
      c
      for c in [
          "Date",
          "Inflow",
          "Gross Profit",
          "Outflow",
          "Balance",
          "Description",
      ]
      if c in raw_df.columns
  ]
  df_tx = raw_df[tx_cols].copy()

  # Remove empty date rows created by side-table alignment
  df_tx = df_tx.dropna(subset=["Date"]).reset_index(drop=True)

  # Clean currency strings to floating point numbers
  for col in ["Inflow", "Outflow", "Balance"]:
    if col in df_tx.columns:
      df_tx[col] = pd.to_numeric(
          df_tx[col].astype(str).str.replace(r"[$,]", "", regex=True),
          errors="coerce",
      ).fillna(0)

  # 2. Separate Sidebar Stats Table (Columns G to L)
  stats_cols = [c for c in raw_df.columns if c not in tx_cols]
  df_stats = raw_df[stats_cols].dropna(how="all").reset_index(drop=True)

  if not df_tx.empty:
    inflow = df_tx["Inflow"].sum()
    outflow = df_tx["Outflow"].sum()

    # Get latest running balance from the top row of Column E
    current_balance = (
        df_tx["Balance"].iloc[0] if "Balance" in df_tx.columns else 0.0
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Current Balance", f"${current_balance:,.2f}")
    col2.metric("Inflow", f"${inflow:,.2f}")
    col3.metric("Outflow", f"${outflow:,.2f}")
    col4.metric("Gross Profit", "$0.00")

    st.markdown("---")
    st.subheader("Transactions Log")
    st.dataframe(df_tx, use_container_width=True)

    if not df_stats.empty:
      st.markdown("---")
      st.subheader("Summary Stats & Loans")
      st.dataframe(df_stats, use_container_width=True)

  else:
    st.info("Connected successfully! No transaction records found.")

except Exception as e:
  st.error(f"Error loading sheet data: {e}")
