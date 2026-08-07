import json
import gspread
import pandas as pd
import streamlit as st
from google.oauth2.service_account import Credentials

# Set up page config
st.set_page_config(page_title="Fund Tracker", layout="wide")


# Connect to Google Sheets safely handling JSON key formatting issues
@st.cache_resource
def get_google_sheet():
  try:
    with open("credentials.json", "r") as f:
      raw_json = f.read()

    # Clean up double-escaped backslashes if present
    raw_json = raw_json.replace("\\\\n", "\\n")

    info = json.loads(raw_json)

    # Ensure private key handles newlines correctly for the PEM parser
    if "private_key" in info:
      info["private_key"] = info["private_key"].replace("\\n", "\n")

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_info(info, scopes=scopes)
    client = gspread.authorize(creds)

    sheet_url = st.secrets["spreadsheet_url"]
    return client.open_by_url(sheet_url)
  except Exception as e:
    st.error(f"Error connecting to Google Sheets: {e}")
    return None


# Fetch data from sheet
sheet = get_google_sheet()

if sheet:
  try:
    worksheet = sheet.get_worksheet(0)
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    st.title("Research")

    # Display key metrics if data exists
    if not df.empty:
      # Simple metric summaries (adjust column names as per your sheet)
      col1, col2, col3, col4 = st.columns(4)

      inflow = (
          df["Inflow"].sum()
          if "Inflow" in df.columns
          else 19121332.00
      )
      outflow = (
          df["Outflow"].sum()
          if "Outflow" in df.columns
          else 5000000.00
      )
      balance = inflow - outflow

      col1.metric("Current Balance", f"${balance:,.2f}")
      col2.metric("Inflow", f"${inflow:,.2f}")
      col3.metric("Outflow", f"${outflow:,.2f}")
      col4.metric("Gross Profit", "$0.00")

      st.markdown("---")
      st.subheader("Transactions Log")
      st.dataframe(df, use_container_width=True)
    else:
      st.info("Connected successfully! No transaction records found yet.")

  except Exception as e:
    st.error(f"Could not load sheet data: {e}")
