#!/usr/bin/env python3
"""
Fix cost calculation in data.csv
Cost = Face Amount * (Price + Accrued Interest) / 100
"""

import pandas as pd

# Read the CSV
df = pd.read_csv('data.csv')

# Fix cost calculation for GGI portfolio bonds (not cash)
ggi_mask = (df['fund_name'] == 'Guinness Global Investors Fund') & (df['name'] != 'Cash')

for idx in df[ggi_mask].index:
    face_amount = df.loc[idx, 'face_amount']
    price = df.loc[idx, 'closing_price']
    accrued_pct = df.loc[idx, 'accrued_interest']
    
    # Calculate correct cost: face * (price + accrued) / 100
    correct_cost = face_amount * (price + accrued_pct) / 100
    
    df.loc[idx, 'total_cost'] = correct_cost
    
    print(f"{df.loc[idx, 'name'][:30]:30s} Face: ${face_amount:,.0f} Price: {price:.3f} Accrued: {accrued_pct:.3f}% Cost: ${correct_cost:,.2f}")

# Recalculate P&L for verification
print("\nP&L Summary:")
total_cost = df[ggi_mask]['total_cost'].sum()
total_market_value = df[ggi_mask]['market_value'].sum()
total_pnl = total_market_value - total_cost
print(f"Total Cost: ${total_cost:,.2f}")
print(f"Total Market Value: ${total_market_value:,.2f}")
print(f"Total P&L: ${total_pnl:,.2f} ({(total_pnl/total_cost)*100:.2f}%)")

# Save the corrected data
df.to_csv('data.csv', index=False)
print("\ndata.csv has been updated with correct cost calculations.")