# fetch_data.py

import requests
import json
import pandas as pd

def fetch_fund_data(fund_name, time_selection):
    """
    Fetches fund data from the API.
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

    response = requests.post(url, json=payload, headers=headers, timeout=10)
    response.raise_for_status()  # Raises HTTPError for bad responses
    data = response.json()
    return pd.DataFrame(data)
