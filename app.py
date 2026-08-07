import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Page Configuration
st.set_page_config(page_title="Fund Tracker", layout="wide", initial_sidebar_state="collapsed")

# Custom Dark Theme Styling
st.markdown("""
<style>
    .stApp { background-color: #0d0e12; color: #ffffff; }
    div[data-testid="stMetric"] {
        background-color: #1a1c23;
        border: 1px solid #2d303e;
        border-radius: 8px;
        padding: 12px 18px;
    }
    .stMetricLabel { color: #9da3ae !important; font-size: 14px; }
    .stMetricValue { font-size: 22px !important; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# Navigation Header
st.caption("Dashboard / Research")
st.title("Research")
st.header("$14,715,130.25")
st.caption("Current Balance")

# KPI Summary Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Inflow", "$19,121,332.00")
col2.metric("Outflow", "$5,000,000.00")
col3.metric("Latest Interest", "$28,136.39")
col4.metric("Gross Profit", "$0.00")

# Fixed Layout for Sub-Metrics (Using Markdown Columns instead of raw HTML)
m1, m2, m3, m4 = st.columns(4)
m1.markdown("**7-Day Interest:**<br>$258,622.73", unsafe_allow_html=True)
m2.markdown("**30-Day Interest:**<br>$593,798.25", unsafe_allow_html=True)
m3.markdown("**Total Interest:**<br>$593,798.25", unsafe_allow_html=True)
m4.markdown("**Loan Deductions:**<br>$0.00", unsafe_allow_html=True)

st.markdown("---")

# Tabs Navigation
tab1, tab2, tab3, tab4 = st.tabs(["Transactions", "Interest Log", "Loan Log", "Customize"])

# Tab 1: Transactions
with tab1:
    st.markdown("### Add Transaction")
    with st.form("add_tx_form", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        tx_date = c1.date_input("Date")
        tx_inflow = c2.number_input("Inflow ($)", min_value=0.0)
        tx_outflow = c3.number_input("Outflow ($)", min_value=0.0)
        
        c4, c5 = st.columns(2)
        tx_gross = c4.number_input("Gross Profit ($)", min_value=0.0)
        tx_desc = c5.text_input("Description", placeholder="e.g. Starting Balance")
        
        if st.form_submit_button("+ Add Transaction", type="primary"):
            st.success("Transaction submitted successfully!")

    st.markdown("### Transaction Log")
    st.info("Your app layout is ready. Link your Google Sheet via Streamlit secrets to display live table rows.")

# Tab 2: Interest Log
with tab2:
    st.markdown("### Add Interest Entry")
    with st.form("add_interest_form"):
        i_date = st.date_input("Date", key="i_date")
        i_amount = st.number_input("Interest Earned ($)", min_value=0.0)
        if st.form_submit_button("+ Add"):
            st.success("Interest entry saved!")

# Tab 3: Loan Log
with tab3:
    st.markdown("### Add Loan Entry")
    with st.form("add_loan_form"):
        l_date = st.date_input("Date", key="l_date")
        l_amount = st.number_input("Loan Amount ($)", min_value=0.0)
        l_deduct = st.number_input("Interest Deduction ($)", min_value=0.0)
        if st.form_submit_button("+ Add"):
            st.success("Loan entry saved!")

# Tab 4: Customize
with tab4:
    st.markdown("### Gross Profit %")
    rate = st.number_input("Rate (%)", value=10)
    if st.button("Save Rate"):
        st.success("Rate updated!")
