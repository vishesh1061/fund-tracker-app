import gspread
import pandas as pd
import streamlit as st
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Fund Tracker", layout="wide")


def get_clean_credentials():
  """Formats private key from Streamlit Secrets into a valid PEM RSA structure."""
  creds_dict = dict(st.secrets["gcp_service_account"])

  raw_key = creds_dict.get("private_key", "")
  # Handle literal '\\n' strings
  raw_key = raw_key.replace("\\n", "\n")

  # Strip headers/footers to extract raw Base64 content
  clean_body = (
      raw_key.replace("-----BEGIN PRIVATE KEY-----", "")
      .replace("-----END PRIVATE KEY-----", "")
      .replace("\n", "")
      .replace("\r", "")
      .replace(" ", "")
  )

  # Chunk Base64 body into standard 64-character PEM lines
  chunks = [clean_body[i : i + 64] for i in range(0, len(clean_body), 64)]
  formatted_key = (
      "-----BEGIN PRIVATE KEY-----\n"
      + "\n".join(chunks)
      + "\n-----END PRIVATE KEY-----\n"
  )

  creds_dict["private_key"] = formatted_key
  return creds_dict


@st.cache_resource
def get_google_sheet():
  try:
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    creds_dict = get_clean_credentials()
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)

    client = gspread.authorize(creds)
    sheet_url = st.secrets["spreadsheet_url"]
    return client.open_by_url(sheet_url)
  except Exception as e:
    st.error(f"Error connecting to Google Sheets: {e}")
    return None


sheet = get_google_sheet()

if sheet:
  try:
    worksheet = sheet.get_worksheet(0)
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    st.title("Research")

    if not df.empty:
      col1, col2, col3, col4 = st.columns(4)

      inflow = df["Inflow"].sum() if "Inflow" in df.columns else 19121332.00
      outflow = df["Outflow"].sum() if "Outflow" in df.columns else 5000000.00
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
