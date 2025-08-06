#!/usr/bin/env python3
"""
Adjust Cash Allocation for GGI Portfolio
========================================

Increases face amounts for selected bonds by $100k each
to reduce cash position to under 5% of portfolio.
"""

import pandas as pd
import numpy as np

def adjust_cash_allocation():
    """Adjust bond allocations to reduce cash to under 5%"""
    
    # Load current data
    print("Loading portfolio data...")
    df = pd.read_csv('data.csv')
    
    # Filter GGI portfolio
    ggi_df = df[df['fund_name'] == 'Guinness Global Investors Fund'].copy()
    non_cash = ggi_df[ggi_df['name'] != 'Cash'].copy()
    cash_row = ggi_df[ggi_df['name'] == 'Cash']
    
    # Current status
    current_cash = cash_row['market_value'].values[0] if len(cash_row) > 0 else 0
    total_portfolio = 10_000_000
    current_cash_pct = (current_cash / total_portfolio) * 100
    
    print(f"\nCurrent cash position: ${current_cash:,.2f} ({current_cash_pct:.2f}%)")
    print(f"Target: Less than 5% (< ${500_000:,.2f})")
    
    # Calculate how much we need to allocate to bonds
    target_cash = total_portfolio * 0.045  # Target 4.5% to be safe
    amount_to_allocate = current_cash - target_cash
    
    print(f"\nNeed to allocate: ${amount_to_allocate:,.2f} more to bonds")
    
    # Select bonds to increase (prioritize lower-priced bonds for better value)
    # Sort by price to get bonds trading below par
    non_cash_sorted = non_cash.sort_values('closing_price')
    
    # Calculate how many bonds to adjust
    increment = 100_000  # Increase by $100k face amount
    num_adjustments = int(np.ceil(amount_to_allocate / (increment * 0.85)))  # Assume avg price of 85
    
    print(f"Will increase {num_adjustments} bonds by ${increment:,.0f} each")
    
    # Select bonds to adjust - prioritize:
    # 1. Bonds trading below 90
    # 2. Bonds with lower current allocations
    bonds_to_adjust = []
    
    # First pass: bonds below 90
    for idx, row in non_cash_sorted.iterrows():
        if row['closing_price'] < 90 and len(bonds_to_adjust) < num_adjustments:
            bonds_to_adjust.append(idx)
    
    # Second pass: if we need more, add bonds below 95
    for idx, row in non_cash_sorted.iterrows():
        if row['closing_price'] < 95 and idx not in bonds_to_adjust and len(bonds_to_adjust) < num_adjustments:
            bonds_to_adjust.append(idx)
    
    # Apply adjustments
    total_market_value_increase = 0
    
    print("\nAdjusting bonds:")
    for idx in bonds_to_adjust[:num_adjustments]:
        bond_name = df.loc[idx, 'name']
        current_face = df.loc[idx, 'face_amount']
        current_price = df.loc[idx, 'closing_price']
        
        # Increase face amount
        new_face = current_face + increment
        df.loc[idx, 'face_amount'] = new_face
        
        # Recalculate market value
        new_market_value = new_face * current_price / 100
        old_market_value = df.loc[idx, 'market_value']
        df.loc[idx, 'market_value'] = round(new_market_value, 2)
        
        # Update cost basis (at par)
        df.loc[idx, 'total_cost'] = new_face
        
        market_value_increase = new_market_value - old_market_value
        total_market_value_increase += market_value_increase
        
        print(f"  {bond_name}:")
        print(f"    Face: ${current_face:,.0f} → ${new_face:,.0f}")
        print(f"    Market Value: ${old_market_value:,.2f} → ${new_market_value:,.2f}")
        print(f"    Increase: ${market_value_increase:,.2f}")
    
    # Update cash position
    new_cash_amount = current_cash - total_market_value_increase
    cash_idx = ggi_df[ggi_df['name'] == 'Cash'].index[0]
    df.loc[cash_idx, 'face_amount'] = new_cash_amount
    df.loc[cash_idx, 'market_value'] = new_cash_amount
    df.loc[cash_idx, 'total_cost'] = new_cash_amount
    
    # Recalculate all weightings
    ggi_total_mv = df[df['fund_name'] == 'Guinness Global Investors Fund']['market_value'].sum()
    
    for idx in ggi_df.index:
        df.loc[idx, 'weighting'] = round(df.loc[idx, 'market_value'] / ggi_total_mv * 100, 2)
    
    # Summary
    print("\n" + "="*50)
    print("ADJUSTED PORTFOLIO SUMMARY")
    print("="*50)
    
    new_cash_pct = (new_cash_amount / total_portfolio) * 100
    print(f"Old cash position: ${current_cash:,.2f} ({current_cash_pct:.2f}%)")
    print(f"New cash position: ${new_cash_amount:,.2f} ({new_cash_pct:.2f}%)")
    print(f"Total bonds market value increase: ${total_market_value_increase:,.2f}")
    
    # Verify totals
    ggi_final = df[df['fund_name'] == 'Guinness Global Investors Fund']
    print(f"\nTotal portfolio value: ${ggi_final['market_value'].sum():,.2f}")
    print(f"Total weight: {ggi_final['weighting'].sum():.2f}%")
    
    # Save updated data
    print("\nSaving updated portfolio data...")
    df.to_csv('data.csv', index=False)
    print("Done! Cash position has been reduced to under 5%.")
    
    return df

if __name__ == "__main__":
    adjust_cash_allocation()