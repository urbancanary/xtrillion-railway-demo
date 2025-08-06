# fetch_data_optimized.py - Optimized version with caching

import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import hashlib

# Cache data for 1 hour (3600 seconds)
@st.cache_data(ttl=3600, show_spinner=False)
def fetch_fund_data_cached(fund_name, time_selection):
    """
    Fetches fund data from the API with caching.
    Cache key includes fund_name and time_selection to cache different requests separately.
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
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {str(e)}")
        return pd.DataFrame()  # Return empty DataFrame on error

# Cache country data for 2 hours
@st.cache_data(ttl=7200, show_spinner=False)
def fetch_country_data_cached(country_name):
    """
    Fetches country report data with caching.
    """
    url = "https://my-combined-app-44056503414.us-central1.run.app/process_json"
    
    payload = {
        "sample_key": json.dumps({
            "db_path": "credit_research.db",
            "table": "FullReport",
            "filters": {"Country": country_name},
            "fields": "*",
            "page": 1,
            "page_size": 10
        })
    }
    
    headers = {
        "Content-Type": "application/json",
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data[0] if data else None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching country data: {str(e)}")
        return None

# Cache portfolio data loaded from CSV
@st.cache_data(show_spinner=False)
def load_portfolio_data_cached(file_path="data.csv"):
    """
    Load portfolio data from CSV with caching.
    """
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        st.error(f"Error loading portfolio data: {str(e)}")
        return pd.DataFrame()

# Cache expensive computations
@st.cache_data(show_spinner=False)
def calculate_portfolio_metrics_cached(df):
    """
    Calculate portfolio metrics with caching.
    """
    if df.empty:
        return {}
    
    metrics = {
        'total_holdings': len(df),
        'total_value': df['weighting'].sum() if 'weighting' in df.columns else 0,
        'avg_yield': df['yield'].mean() if 'yield' in df.columns else 0,
        'avg_duration': df['duration'].mean() if 'duration' in df.columns else 0,
    }
    return metrics

# Cache chart generation
@st.cache_data(show_spinner=False)
def generate_pie_chart_cached(df, column, title, color_sequence):
    """
    Generate pie chart with caching.
    Returns the chart configuration as a dict to avoid serialization issues.
    """
    import plotly.express as px
    
    if df.empty or column not in df.columns:
        return None
    
    # Fill NaN values with 'Cash' for certain columns
    if column in ['nfa_star_rating', 'esg_country_star_rating']:
        df = df.copy()
        df[column] = df[column].fillna('Cash')
    
    fig = px.pie(df, names=column, values='weighting', title=title,
                 color_discrete_sequence=color_sequence, hole=0.4)
    
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(
        paper_bgcolor='#1f1f1f',
        plot_bgcolor='#1f1f1f',
        font=dict(color='white'),
        height=400,
        margin=dict(t=40, b=20, l=20, r=20),
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02
        )
    )
    
    return fig.to_dict()  # Return as dict for caching

# Preload common data to warm up cache
def preload_cache():
    """
    Preload commonly used data into cache to improve initial load time.
    """
    common_funds = [
        "GGI Wealthy Nations Bond Fund",
        "Shin Kong Emerging Wealthy Nations Bond Fund",
        "Shin Kong Environmental Sustainability Bond Fund"
    ]
    
    common_countries = ["Israel", "Qatar", "Mexico", "Saudi Arabia"]
    
    # Preload fund data
    for fund in common_funds:
        try:
            fetch_fund_data_cached(fund, "Latest")
        except:
            pass
    
    # Preload country data
    for country in common_countries:
        try:
            fetch_country_data_cached(country)
        except:
            pass

# Session state management for better performance
def init_session_state():
    """
    Initialize session state variables to reduce recomputation.
    """
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.current_fund = None
        st.session_state.current_country = None
        st.session_state.last_update = datetime.now()

# Connection pool for better API performance
class APIConnectionPool:
    """
    Maintain a connection pool for API requests.
    """
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Connection': 'keep-alive'
        })
    
    def post(self, url, payload, timeout=10):
        """
        Make a POST request using the connection pool.
        """
        return self.session.post(url, json=payload, timeout=timeout)

# Global connection pool instance
api_pool = APIConnectionPool()

# Optimized data fetching with connection pooling
@st.cache_data(ttl=3600, show_spinner=False)
def fetch_data_optimized(endpoint, payload):
    """
    Generic optimized data fetching with connection pooling and caching.
    """
    # Create a cache key from the payload
    cache_key = hashlib.md5(json.dumps(payload, sort_keys=True).encode()).hexdigest()
    
    try:
        response = api_pool.post(endpoint, payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None