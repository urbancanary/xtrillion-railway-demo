# fetch_data.py - Optimized with caching

import streamlit as st
import requests
import json
import pandas as pd

# Cache data for 1 hour (3600 seconds)
@st.cache_data(ttl=3600, show_spinner=False)
def fetch_fund_data(fund_name, time_selection):
    """
    Fetches fund data from the API with caching.
    Data is cached for 1 hour to improve performance.
    """
    url = "https://my-combined-app-44056503414.us-central1.run.app/process_json"
    table_name = "fund_holdings_latest" if time_selection == "Latest" else "fund_holdings_me"

    payload = {
        "sample_key": json.dumps({
            "db_path": "consolidated.db",
            "table": table_name,
            "filters": {"fund_name": fund_name},
            "fields": "*",
            "page": 1,
            "page_size": 100
        })
    }

    headers = {
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()  # Raises HTTPError for bad responses
        data = response.json()
        return pd.DataFrame(data)
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching fund data: {str(e)}")
        return pd.DataFrame()  # Return empty DataFrame on error

# Wrapper for backward compatibility
def fetch_fund_data_with_cache(fund_name, time_selection="Latest"):
    """
    Backward compatible wrapper that uses cached version.
    """
    return fetch_fund_data(fund_name, time_selection)
