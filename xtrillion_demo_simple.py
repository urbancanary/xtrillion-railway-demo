import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="XTrillion Demo",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("🌟 XTrillion Demo")
st.markdown("### Bond Analytics & Portfolio Management")

# Sidebar
with st.sidebar:
    st.header("Navigation")
    page = st.radio("Select Page", ["Dashboard", "Bond Analysis", "Portfolio", "About"])
    
    st.divider()
    st.info("**Deployment Status**")
    st.success("✅ Deployed on Railway")
    st.caption(f"Version: 1.0.0")
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d')}")

# Main content
if page == "Dashboard":
    st.header("📊 Dashboard")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Bonds", "1,247", "+12")
    with col2:
        st.metric("Portfolio Value", "$12.5M", "+2.3%")
    with col3:
        st.metric("Average Yield", "4.82%", "+0.15%")
    
    # Sample chart
    st.subheader("Yield Curve")
    terms = [1, 2, 3, 5, 7, 10, 20, 30]
    yields = [4.2, 4.3, 4.4, 4.6, 4.7, 4.8, 4.9, 5.0]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=terms, y=yields, mode='lines+markers', name='US Treasury'))
    fig.update_layout(
        title="US Treasury Yield Curve",
        xaxis_title="Term (Years)",
        yaxis_title="Yield (%)",
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)

elif page == "Bond Analysis":
    st.header("🔍 Bond Analysis")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        bond_input = st.text_input("Enter Bond Description or ISIN", "T 4.1 02/15/28")
        analyze_btn = st.button("Analyze Bond", type="primary")
    
    with col2:
        price = st.number_input("Price", value=99.5, min_value=0.0, max_value=200.0)
        settlement = st.date_input("Settlement Date")
    
    if analyze_btn:
        st.success("Bond analysis complete!")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Yield to Maturity", "4.15%")
        with col2:
            st.metric("Duration", "3.82")
        with col3:
            st.metric("Convexity", "18.4")
        with col4:
            st.metric("Accrued Interest", "$1.23")

elif page == "Portfolio":
    st.header("💼 Portfolio Analysis")
    
    # Sample portfolio data
    portfolio_data = pd.DataFrame({
        'Bond': ['T 3.5 2028', 'T 4.0 2032', 'AAPL 3.85 2029', 'MSFT 3.3 2027'],
        'Weight': [25, 30, 20, 25],
        'Yield': [3.8, 4.2, 4.1, 3.9],
        'Duration': [3.2, 5.8, 4.1, 2.9]
    })
    
    st.dataframe(portfolio_data, use_container_width=True)
    
    # Portfolio metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Portfolio Yield", "3.98%")
    with col2:
        st.metric("Portfolio Duration", "4.12")
    with col3:
        st.metric("Portfolio Convexity", "21.3")

else:  # About page
    st.header("ℹ️ About XTrillion")
    st.markdown("""
    ### XTrillion Demo Application
    
    This is a demonstration of the XTrillion bond analytics platform, featuring:
    
    - **Bond Analysis**: Calculate yield, duration, convexity and other metrics
    - **Portfolio Management**: Analyze portfolio-level metrics
    - **Real-time Data**: Integration with market data providers
    - **Dark Mode**: Professional interface with dark theme
    
    **Deployment Details:**
    - Platform: Railway
    - Container: Podman (838MB)
    - Framework: Streamlit
    - Analytics: XTrillion Core Engine
    
    **Next Steps:**
    - Connect to live data feeds
    - Add more analytics features
    - Integrate with trading systems
    """)

# Footer
st.divider()
st.caption("XTrillion Demo | Deployed on Railway | Powered by Streamlit")