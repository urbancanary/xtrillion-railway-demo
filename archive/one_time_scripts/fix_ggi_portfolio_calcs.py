#!/usr/bin/env python3
"""
Fix GGI Portfolio Calculations
==============================

Fixes:
1. Round face amounts down to nearest $100k
2. Adjust market values based on corrected face amounts
3. Calculate cost basis appropriately
4. Set cash as difference between $10m and total cost
5. Prepare for accrued interest calculations
"""

import pandas as pd
import numpy as np

def fix_portfolio_calculations():
    """Fix GGI portfolio calculations with proper rounding and cash allocation"""
    
    # Load current data
    print("Loading portfolio data...")
    df = pd.read_csv('data.csv')
    
    # Filter GGI portfolio
    ggi_df = df[df['fund_name'] == 'Guinness Global Investors Fund'].copy()
    non_cash = ggi_df[ggi_df['name'] != 'Cash'].copy()
    
    # Portfolio parameters
    TOTAL_PORTFOLIO_VALUE = 10_000_000  # $10 million
    ROUNDING_AMOUNT = 100_000  # Round to nearest $100k
    
    print("\nPortfolio parameters:")
    print(f"Total portfolio value: ${TOTAL_PORTFOLIO_VALUE:,.0f}")
    print(f"Number of holdings (ex-cash): {len(non_cash)}")
    
    # Calculate equal weights for non-cash holdings
    num_holdings = len(non_cash)
    equal_weight = 100.0 / num_holdings  # Percentage weight per holding
    target_value_per_holding = TOTAL_PORTFOLIO_VALUE / num_holdings
    
    print(f"Equal weight per holding: {equal_weight:.2f}%")
    print(f"Target value per holding: ${target_value_per_holding:,.0f}")
    
    # Fix calculations for each holding
    total_cost = 0
    
    for idx in non_cash.index:
        # Get current price (as percentage of par)
        current_price = non_cash.loc[idx, 'closing_price']
        
        # Calculate face amount needed for target value
        # Market value = Face amount * Price / 100
        required_face = (target_value_per_holding / current_price) * 100
        
        # Round DOWN to nearest 100k
        rounded_face = np.floor(required_face / ROUNDING_AMOUNT) * ROUNDING_AMOUNT
        
        # Update face amount
        df.loc[idx, 'face_amount'] = rounded_face
        
        # Calculate actual market value with rounded face amount
        market_value = rounded_face * current_price / 100
        df.loc[idx, 'market_value'] = round(market_value, 2)
        
        # Calculate cost basis (assume purchased at par for simplicity)
        # This can be adjusted based on actual purchase prices
        cost_basis = rounded_face  # Purchased at 100
        df.loc[idx, 'total_cost'] = round(cost_basis, 2)
        
        # Update weighting based on actual market value
        # Will recalculate after we know total
        
        total_cost += cost_basis
        
        print(f"\n{df.loc[idx, 'name']}:")
        print(f"  Price: {current_price:.3f}")
        print(f"  Required face: ${required_face:,.0f}")
        print(f"  Rounded face: ${rounded_face:,.0f}")
        print(f"  Market value: ${market_value:,.2f}")
        print(f"  Cost basis: ${cost_basis:,.2f}")
    
    # Calculate total market value of bonds
    total_bonds_market_value = 0
    for idx in non_cash.index:
        total_bonds_market_value += df.loc[idx, 'market_value']
    
    # Calculate cash position as difference between portfolio value and bonds market value
    cash_amount = TOTAL_PORTFOLIO_VALUE - total_bonds_market_value
    
    # Find cash row
    cash_idx = ggi_df[ggi_df['name'] == 'Cash'].index
    if len(cash_idx) > 0:
        cash_idx = cash_idx[0]
        df.loc[cash_idx, 'face_amount'] = cash_amount
        df.loc[cash_idx, 'market_value'] = cash_amount
        df.loc[cash_idx, 'total_cost'] = cash_amount
        df.loc[cash_idx, 'closing_price'] = 100.0
        
        print("\nCash position:")
        print(f"  Bonds market value: ${total_bonds_market_value:,.2f}")
        print(f"  Cash amount: ${cash_amount:,.2f}")
        print(f"  Percentage: {(cash_amount / TOTAL_PORTFOLIO_VALUE * 100):.2f}%")
    
    # Update total cost to equal total portfolio value
    total_cost = total_bonds_market_value + cash_amount
    
    # Recalculate all weightings based on actual market values
    ggi_total_mv = df[df['fund_name'] == 'Guinness Global Investors Fund']['market_value'].sum()
    
    for idx in ggi_df.index:
        df.loc[idx, 'weighting'] = round(df.loc[idx, 'market_value'] / ggi_total_mv * 100, 2)
    
    # Add accrued interest placeholder (will be calculated in next step)
    if 'accrued_interest' not in df.columns:
        df['accrued_interest'] = 0.0
    
    # Summary statistics
    print("\n" + "="*50)
    print("PORTFOLIO SUMMARY")
    print("="*50)
    
    ggi_final = df[df['fund_name'] == 'Guinness Global Investors Fund']
    print(f"Total face amount: ${ggi_final['face_amount'].sum():,.0f}")
    print(f"Total market value: ${ggi_final['market_value'].sum():,.2f}")
    print(f"Total cost basis: ${ggi_final['total_cost'].sum():,.2f}")
    print(f"Total P&L: ${(ggi_final['market_value'].sum() - ggi_final['total_cost'].sum()):,.2f}")
    
    print("\nWeighting check:")
    print(f"Total weight: {ggi_final['weighting'].sum():.2f}%")
    
    # Save updated data
    print("\nSaving updated portfolio data...")
    df.to_csv('data.csv', index=False)
    print("Done! Portfolio calculations have been fixed.")
    
    # Create a summary report
    summary = ggi_final[['name', 'face_amount', 'closing_price', 'market_value', 'total_cost', 'weighting']].copy()
    summary['p&l'] = summary['market_value'] - summary['total_cost']
    summary = summary.sort_values('weighting', ascending=False)
    
    print("\nDetailed holdings:")
    print(summary.to_string(index=False))
    
    return df

if __name__ == "__main__":
    fix_portfolio_calculations()