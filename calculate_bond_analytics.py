#!/usr/bin/env python3
"""
Calculate Bond Analytics for GGI Portfolio
==========================================

Uses the Google Analysis 10 API to calculate:
- Accrued Interest
- Yield to Maturity (YTM)
- Duration
- Spread

For each bond in the GGI portfolio.
"""

import pandas as pd
import requests
import json
from datetime import datetime
import time

# API Configuration
API_BASE_URL = "https://future-footing-414610.uc.r.appspot.com"
API_KEY = "xtrillion-ga9-key-2024"  # From the docs

def call_bond_api(bond_description, price, settlement_date=None):
    """Call the GA10 API to get bond analytics"""
    
    url = f"{API_BASE_URL}/api/v1/bond/analysis"
    
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }
    
    # Build request payload
    payload = {
        "description": bond_description,
        "price": price
    }
    
    if settlement_date:
        payload["settlement_date"] = settlement_date
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                return data.get("analytics", {})
            else:
                print(f"API error for {bond_description}: {data.get('message', 'Unknown error')}")
                return None
        else:
            print(f"HTTP error {response.status_code} for {bond_description}")
            return None
            
    except Exception as e:
        print(f"Request failed for {bond_description}: {str(e)}")
        return None

def update_portfolio_analytics():
    """Update GGI portfolio with calculated analytics"""
    
    print("Loading portfolio data...")
    df = pd.read_csv('data.csv')
    
    # Filter GGI portfolio bonds (exclude cash)
    ggi_bonds = df[(df['fund_name'] == 'Guinness Global Investors Fund') & 
                   (df['name'] != 'Cash')].copy()
    
    print(f"Found {len(ggi_bonds)} bonds to analyze")
    
    # Settlement date (use today for now)
    settlement_date = datetime.now().strftime("%Y-%m-%d")
    print(f"Using settlement date: {settlement_date}")
    
    # Process each bond
    analytics_results = []
    
    for idx, bond in ggi_bonds.iterrows():
        bond_name = bond['name']
        price = bond['closing_price']
        
        print(f"\nProcessing: {bond_name}")
        print(f"  Price: {price}")
        
        # Call API
        analytics = call_bond_api(bond_name, price, settlement_date)
        
        if analytics:
            # Extract key metrics
            result = {
                'index': idx,
                'name': bond_name,
                'ytm': analytics.get('ytm', 0),
                'duration': analytics.get('duration', 0),
                'accrued_interest': analytics.get('accrued_interest', 0),
                'spread': analytics.get('spread', 0) if analytics.get('spread') is not None else 0,
                'clean_price': analytics.get('clean_price', price),
                'dirty_price': analytics.get('dirty_price', price),
                'pvbp': analytics.get('pvbp', 0),
                'convexity': analytics.get('convexity', 0),
                'macaulay_duration': analytics.get('macaulay_duration', 0)
            }
            
            analytics_results.append(result)
            
            print(f"  ✓ YTM: {result['ytm']:.3f}%")
            print(f"  ✓ Duration: {result['duration']:.2f} years")
            print(f"  ✓ Accrued: {result['accrued_interest']:.3f}%")
            
            # Update dataframe
            df.loc[idx, 'yield'] = f"{result['ytm']:.3f}"
            df.loc[idx, 'duration'] = f"{result['duration']:.2f}"
            df.loc[idx, 'accrued_interest'] = result['accrued_interest']
            
            # Add additional analytics columns if they don't exist
            if 'pvbp' not in df.columns:
                df['pvbp'] = 0.0
            if 'convexity' not in df.columns:
                df['convexity'] = 0.0
            if 'spread' not in df.columns:
                df['spread'] = 0.0
                
            df.loc[idx, 'pvbp'] = result['pvbp']
            df.loc[idx, 'convexity'] = result['convexity']
            df.loc[idx, 'spread'] = result['spread']
            
        else:
            print(f"  ✗ Failed to get analytics")
            
        # Small delay to avoid overwhelming the API
        time.sleep(0.1)
    
    # Calculate portfolio-level metrics
    print("\n" + "="*50)
    print("PORTFOLIO ANALYTICS SUMMARY")
    print("="*50)
    
    # Create results dataframe for analysis
    results_df = pd.DataFrame(analytics_results)
    
    if not results_df.empty:
        # Get weights for weighted calculations
        weights = []
        for idx in results_df['index']:
            weights.append(df.loc[idx, 'weighting'] / 100.0)
        
        results_df['weight'] = weights
        
        # Calculate weighted averages
        portfolio_ytm = (results_df['ytm'] * results_df['weight']).sum()
        portfolio_duration = (results_df['duration'] * results_df['weight']).sum()
        portfolio_convexity = (results_df['convexity'] * results_df['weight']).sum()
        
        # Calculate total accrued interest in dollars
        total_accrued = 0
        for idx, result in results_df.iterrows():
            face_amount = df.loc[result['index'], 'face_amount']
            accrued_dollars = face_amount * result['accrued_interest'] / 100
            total_accrued += accrued_dollars
            df.loc[result['index'], 'accrued_dollars'] = accrued_dollars
        
        print(f"Portfolio YTM: {portfolio_ytm:.3f}%")
        print(f"Portfolio Duration: {portfolio_duration:.2f} years")
        print(f"Portfolio Convexity: {portfolio_convexity:.2f}")
        print(f"Total Accrued Interest: ${total_accrued:,.2f}")
        
        # Save summary to portfolio
        portfolio_summary = {
            'portfolio_ytm': portfolio_ytm,
            'portfolio_duration': portfolio_duration,
            'portfolio_convexity': portfolio_convexity,
            'total_accrued': total_accrued,
            'calculation_date': settlement_date
        }
        
        # Add summary as metadata (could be saved separately)
        print(f"\nSuccessfully analyzed {len(results_df)} bonds")
    
    # Save updated data
    print("\nSaving updated portfolio data...")
    df.to_csv('data.csv', index=False)
    
    # Also save analytics results separately
    if analytics_results:
        analytics_df = pd.DataFrame(analytics_results)
        analytics_df.to_csv('ggi_analytics.csv', index=False)
        print("Analytics saved to ggi_analytics.csv")
    
    print("Done!")
    
    return df, portfolio_summary if 'portfolio_summary' in locals() else None

def test_single_bond():
    """Test API with a single bond"""
    
    print("Testing API with US Treasury...")
    
    # Test with a known US Treasury
    analytics = call_bond_api("T 3 15/08/52", 71.66)
    
    if analytics:
        print("API Test Successful!")
        print(f"YTM: {analytics.get('ytm', 'N/A')}")
        print(f"Duration: {analytics.get('duration', 'N/A')}")
        print(f"Accrued: {analytics.get('accrued_interest', 'N/A')}")
        return True
    else:
        print("API Test Failed!")
        return False

if __name__ == "__main__":
    # Test API first
    print("Testing API connection...")
    if test_single_bond():
        print("\nProceeding with portfolio analysis...")
        update_portfolio_analytics()
    else:
        print("\nAPI test failed. Please check the API endpoint and try again.")