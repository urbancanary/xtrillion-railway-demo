"""
Create GGI (Guinness Global Investors) portfolio from SKEWNBF data
Each holding will have exactly 4% weight
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_ggi_portfolio():
    # Read the original data
    df = pd.read_csv('data.csv')
    
    # Filter for SKEWNBF holdings
    skewnbf_df = df[df['fund_name'] == 'Shin Kong Emerging Wealthy Nations Bond Fund'].copy()
    
    # Create GGI portfolio
    ggi_df = skewnbf_df.copy()
    
    # Update fund name
    ggi_df['fund_name'] = 'Guinness Global Investors Fund'
    
    # Set equal weights of 4% for each holding
    ggi_df['weighting'] = 4.0
    
    # Recalculate market values to match 4% weights
    # Assume total portfolio value of $10 million for realistic numbers
    total_portfolio_value = 10_000_000
    target_value_per_holding = total_portfolio_value * 0.04  # $400,000 per holding
    
    # Adjust face amounts and market values
    for idx in ggi_df.index:
        current_price = ggi_df.loc[idx, 'closing_price']
        # Calculate new face amount to achieve target market value
        new_face_amount = (target_value_per_holding / current_price) * 100
        ggi_df.loc[idx, 'face_amount'] = round(new_face_amount, 0)
        ggi_df.loc[idx, 'market_value'] = round(new_face_amount * current_price / 100, 0)
        ggi_df.loc[idx, 'total_cost'] = round(new_face_amount * current_price / 100 * 1.02, 2)  # Assume 2% premium on cost
    
    # Update trade dates to more recent dates
    ggi_df['trade_date'] = pd.to_datetime('2024-10-01')
    ggi_df['bpdate'] = pd.to_datetime('2024-10-31')
    
    # Keep existing bonds but update the portfolio context
    print(f"Created GGI portfolio with {len(ggi_df)} holdings")
    print("Each holding weight: 4%")
    print(f"Total portfolio weight: {len(ggi_df) * 4}%")
    
    return ggi_df

def create_ggi_transactions():
    """Create realistic transaction history for GGI portfolio"""
    transactions = []
    
    # Read GGI holdings
    ggi_df = create_ggi_portfolio()
    
    # Create buy transactions over the past 6 months
    start_date = datetime.now() - timedelta(days=180)
    
    for idx, row in ggi_df.iterrows():
        # Initial purchase
        buy_date = start_date + timedelta(days=np.random.randint(0, 60))
        transactions.append({
            'date': buy_date,
            'type': 'BUY',
            'isin': row['isin'],
            'name': row['name'],
            'face_amount': row['face_amount'] * 0.5,  # Initial purchase of half position
            'price': row['closing_price'] * 0.98,  # Slightly lower historical price
            'total': row['face_amount'] * 0.5 * row['closing_price'] * 0.98 / 100,
            'fund': 'Guinness Global Investors Fund'
        })
        
        # Second purchase to reach target weight
        buy_date2 = buy_date + timedelta(days=np.random.randint(30, 90))
        transactions.append({
            'date': buy_date2,
            'type': 'BUY',
            'isin': row['isin'],
            'name': row['name'],
            'face_amount': row['face_amount'] * 0.5,  # Second half
            'price': row['closing_price'] * 0.99,
            'total': row['face_amount'] * 0.5 * row['closing_price'] * 0.99 / 100,
            'fund': 'Guinness Global Investors Fund'
        })
    
    # Add some rebalancing trades
    for i in range(5):
        idx = np.random.randint(0, len(ggi_df))
        row = ggi_df.iloc[idx]
        
        # Sell
        sell_date = start_date + timedelta(days=np.random.randint(120, 150))
        transactions.append({
            'date': sell_date,
            'type': 'SELL',
            'isin': row['isin'],
            'name': row['name'],
            'face_amount': row['face_amount'] * 0.1,  # Partial sell
            'price': row['closing_price'] * 1.01,
            'total': row['face_amount'] * 0.1 * row['closing_price'] * 1.01 / 100,
            'fund': 'Guinness Global Investors Fund'
        })
        
        # Buy back
        buy_date = sell_date + timedelta(days=np.random.randint(5, 15))
        transactions.append({
            'date': buy_date,
            'type': 'BUY',
            'isin': row['isin'],
            'name': row['name'],
            'face_amount': row['face_amount'] * 0.1,
            'price': row['closing_price'],
            'total': row['face_amount'] * 0.1 * row['closing_price'] / 100,
            'fund': 'Guinness Global Investors Fund'
        })
    
    # Convert to DataFrame and sort by date
    transactions_df = pd.DataFrame(transactions)
    transactions_df = transactions_df.sort_values('date')
    transactions_df['date'] = transactions_df['date'].dt.strftime('%Y-%m-%d')
    
    return transactions_df

if __name__ == "__main__":
    # Create GGI portfolio
    ggi_portfolio = create_ggi_portfolio()
    
    # Append to existing data
    existing_df = pd.read_csv('data.csv')
    combined_df = pd.concat([existing_df, ggi_portfolio], ignore_index=True)
    combined_df.to_csv('data_with_ggi.csv', index=False)
    
    # Create transactions
    transactions = create_ggi_transactions()
    transactions.to_csv('ggi_transactions.csv', index=False)
    
    print("\nGGI Portfolio created successfully!")
    print(f"Total holdings: {len(ggi_portfolio)}")
    print("Portfolio saved to: data_with_ggi.csv")
    print("Transactions saved to: ggi_transactions.csv")
    
    # Show sample
    print("\nSample GGI holdings:")
    print(ggi_portfolio[['name', 'weighting', 'market_value', 'country']].head())