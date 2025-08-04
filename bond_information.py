# bond_information.py
import streamlit as st
import pandas as pd
import requests
import json
import numpy as np

def load_bond_data():
    """
    Fetches bond data from the 'fund_holdings_latest' table with Streamlit logging and caching.
    """
    try:
        # Fetch data using the cached internal function
        data = _fetch_bond_data_cached()
        return pd.DataFrame(data)
    except requests.exceptions.Timeout:
        st.error("The request timed out. Please try again later.")
        return None
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
        return None
    except requests.exceptions.RequestException as req_err:
        st.error(f"Request exception: {req_err}")
        return None
    except ValueError as val_err:
        st.error(f"JSON decoding failed: {val_err}")
        return None


# 1. Define the cached internal function
@st.cache_data(show_spinner=True, ttl=3600)
def _fetch_bond_data_cached():
    """
    Internal function to fetch bond data from the API.
    This function is cached to improve performance.
    """
    url = "https://my-combined-app-44056503414.us-central1.run.app/process_json"
    table_name = "fund_holdings_latest"

    payload = {
        "sample_key": json.dumps({
            "db_path": "consolidated.db",
            "table": table_name,
            "filters": {},  # No filters for bonds
            "fields": "*",
            "page": 1,
            "page_size": 100
        })
    }

    headers = {
        "Content-Type": "application/json",
    }

    response = requests.post(url, json=payload, headers=headers, timeout=10)
    response.raise_for_status()  # Raises HTTPError for bad responses
    data = response.json()
    return data


def get_bond_options(csv_file_path='data.csv'):
    # Load the CSV file into a DataFrame
    data = pd.read_csv(csv_file_path)
    return data['name'].unique().tolist()  # Convert to list before returning

def create_bond_information_tab():
    st.title("Bond Information")
    
    # Assume you have some logic to load `bond_data`
    bond_data = load_bond_data()  # Example function to load bond data

    if bond_data.empty:
        st.warning("No bond data available.")
        return  # Exit the function if there's no data

    # Proceed with displaying bond details only if bond_data is not empty
    st.subheader(f"Bond Information for {bond_data['bond_name'].values[0]}")
    
    st.markdown(f"""
    <table>
        <tr><th>ISIN</th><td>{bond_data['isin'].values[0]}</td></tr>
        <tr><th>Issuer</th><td>{bond_data['issuer'].values[0]}</td></tr>
        <tr><th>Coupon</th><td>{bond_data['coupon'].values[0]}</td></tr>
        <tr><th>Maturity</th><td>{bond_data['maturity'].values[0]}</td></tr>
        <tr><th>Price</th><td>{bond_data['price'].values[0]}</td></tr>
    </table>
    """, unsafe_allow_html=True)

    # Additional bond details or charts can be added here

    # Custom CSS
    st.markdown("""
    <style>
    .bond-info-table {
        width: 100%;
        border-collapse: collapse;
    }
    .bond-info-table th {
        text-align: left;
        padding: 8px;
        background-color: #2f2f2f;
        color: #ffa500;
    }
    .bond-info-table tr:nth-child(even) td {
        background-color: #ffa500;
        color: #000000;
    }
    .bond-info-table tr:nth-child(odd) td {
        background-color: #ffb732;
        color: #000000;
    }
    .fund-holdings-table {
        width: 100%;
        border-collapse: collapse;
    }
    .fund-holdings-table th {
        text-align: left;
        padding: 8px;
        background-color: #2f2f2f;
        color: #ffa500;
    }
    .fund-holdings-table td {
        text-align: left;
        padding: 8px;
        background-color: #1f1f1f;
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

    # Get the selected bond from the sidebar
    selected_bond = st.session_state.bond_selection_sidebar

    # Filter the DataFrame based on the selected bond
    bond_data = data[data['name'] == selected_bond]

    # Bond Information Layout and Content
    st.title("Bond Information", anchor=False)
    st.header(f"Bond Information for {selected_bond}")

    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("Bond Details")
        bond_info_html = f"""
        <table class="bond-info-table">
        <tr><th>Total Face Amount</th><td>{bond_data['face_amount'].sum():,.0f}</td></tr>
        <tr><th>ISIN</th><td>{bond_data['isin'].values[0]}</td></tr>
        <tr><th>Closing Price</th><td>{bond_data['closing_price'].values[0]:,.3f}</td></tr>
        <tr><th>Yield</th><td>{bond_data['yield'].values[0]:,.4f}</td></tr>
        <tr><th>Duration</th><td>{bond_data['duration'].values[0]:,.4f}</td></tr>
        <tr><th>Spread</th><td>{bond_data['spread'].values[0]:,.4f}</td></tr>
        <tr><th>Market Value</th><td>{bond_data['market_value'].values[0]:,.2f}</td></tr>
        <tr><th>Accrued Interest</th><td>{bond_data['accrued_interest'].values[0]:,.4f}</td></tr>
        <tr><th>BPDate</th><td>{bond_data['bpdate'].values[0]}</td></tr>
        <tr><th>Currency</th><td>{bond_data['currency'].values[0]}</td></tr>
        <tr><th>Total Cost</th><td>{bond_data['total_cost'].values[0]:,.2f}</td></tr>
        </table>
        """
        st.markdown(bond_info_html, unsafe_allow_html=True)

        st.subheader("Valuation and Trade Information")
        valuation_html = f"""
        <table class="bond-info-table">
        <tr><th>Trade Date</th><td>{bond_data['trade_date'].values[0]}</td></tr>
        <tr><th>Price</th><td>{bond_data['price'].values[0]:,.3f}</td></tr>
        </table>
        """
        st.markdown(valuation_html, unsafe_allow_html=True)

    with col2:
        st.subheader("Descriptive Information")
        descriptive_cols = ['country', 'region', 'msci_esg_rating', 'nfa_star_rating', 'esg_country_star_rating', 'emdm', 'nfa', 'esg']
        descriptive_html = "<table class='bond-info-table'>"
        for i, col in enumerate(descriptive_cols):
            if col in bond_data.columns:
                value = bond_data[col].values[0]
                descriptive_html += f"<tr class='{'even' if i % 2 == 0 else 'odd'}'><th>{col.replace('_', ' ').title()}</th><td>{value}</td></tr>"
        descriptive_html += "</table>"
        st.markdown(descriptive_html, unsafe_allow_html=True)

    st.subheader("Fund Specific Holdings")
    fund_holdings_html = """
    <table class="fund-holdings-table">
    <tr><th>Fund Name</th><th>Face Amount</th></tr>
    """
    for _, row in bond_data.iterrows():
        fund_holdings_html += f"<tr><td>{row['fund_name']}</td><td>{row['face_amount']:,.0f}</td></tr>"
    fund_holdings_html += "</table>"
    st.markdown(fund_holdings_html, unsafe_allow_html=True)