import streamlit as st
import pandas as pd
from datetime import datetime

def show_debug_info():
    st.title("🔍 Deployment Debug Info")
    
    # Show deployment timestamp
    st.write(f"**Current Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.write("**Script Last Modified:** 2025-08-05")
    
    # Check data file
    try:
        df = pd.read_csv('data.csv')
        st.success(f"✓ Data file loaded: {len(df)} rows")
        
        # Check GGI portfolio
        ggi_data = df[df['fund_name'] == 'Guinness Global Investors Fund']
        st.write(f"**GGI Portfolio:** {len(ggi_data)} holdings")
        
        # Check for API data columns
        has_accrued = 'accrued_interest' in df.columns
        has_pvbp = 'pvbp' in df.columns
        has_convexity = 'convexity' in df.columns
        
        st.write("**API Data Columns:**")
        st.write(f"- Accrued Interest: {'✓' if has_accrued else '✗'}")
        st.write(f"- PVBP: {'✓' if has_pvbp else '✗'}")
        st.write(f"- Convexity: {'✓' if has_convexity else '✗'}")
        
        # Show sample bond with analytics
        if not ggi_data.empty and has_accrued:
            sample = ggi_data[ggi_data['name'] == 'US TREASURY N/B 3 15/08/52']
            if not sample.empty:
                bond = sample.iloc[0]
                st.write("\n**US Treasury 3% 2052 Analytics:**")
                st.write(f"- Yield: {bond.get('yield', 'N/A')}")
                st.write(f"- Duration: {bond.get('duration', 'N/A')}")
                st.write(f"- Accrued Interest: {bond.get('accrued_interest', 'N/A')}")
                st.write(f"- Face Amount: ${bond.get('face_amount', 0):,.0f}")
        
        # Check cash position
        cash = ggi_data[ggi_data['name'] == 'Cash']
        if not cash.empty:
            cash_val = cash.iloc[0]['market_value']
            total_val = ggi_data['market_value'].sum()
            cash_pct = (cash_val / total_val) * 100
            st.write(f"\n**Cash Position:** ${cash_val:,.0f} ({cash_pct:.2f}%)")
            
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
    
    # Show navigation status
    st.write("\n**Navigation Configuration:**")
    st.code("""
    "Tools": [
        st.Page(portfolio_valuation, title="Portfolio Valuation", icon="💰", url_path="valuation"),
        # Temporarily disabled for production prep
        # st.Page(trade_calculator, title="Trade Calculator", icon="💱", url_path="trades"),
        # st.Page(bond_calculator, title="Bond Calculator", icon="🧮", url_path="calculator"),
        # st.Page(ai_assistant, title="AI Assistant", icon="🤖", url_path="assistant"),
        st.Page(user_guide, title="User Guide", icon="📖", url_path="guide"),
    ]
    """)