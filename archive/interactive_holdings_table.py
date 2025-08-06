import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
import plotly.graph_objects as go
import plotly.express as px

def create_interactive_holdings_table(fund_data):
    """Create an interactive AG-Grid table with click-to-view bond details"""
    
    # Prepare data for display
    display_data = fund_data.copy()
    
    # Add ID column for tracking
    display_data['id'] = range(len(display_data))
    
    # Configure AG-Grid
    gb = GridOptionsBuilder.from_dataframe(display_data)
    
    # Configure columns
    gb.configure_column("name", header_name="Security", pinned='left', width=250)
    gb.configure_column("isin", header_name="ISIN", width=150)
    gb.configure_column("weighting", header_name="Weight %", width=100, 
                       valueFormatter="data.weighting.toFixed(2) + '%'")
    gb.configure_column("yield", header_name="YTM", width=100)
    gb.configure_column("duration", header_name="Duration", width=100)
    gb.configure_column("region", header_name="Region", width=120)
    gb.configure_column("closing_price", header_name="Price", width=100,
                       valueFormatter="data.closing_price.toFixed(3)")
    gb.configure_column("accrued_interest", header_name="Accrued", width=100,
                       valueFormatter="data.accrued_interest.toFixed(3)")
    
    # Hide ID column
    gb.configure_column("id", hide=True)
    
    # Configure selection
    gb.configure_selection(selection_mode='single', use_checkbox=False)
    
    # Configure grid options
    gb.configure_grid_options(
        domLayout='normal',
        enableCellTextSelection=True,
        ensureDomOrder=True,
        rowHeight=40,
        headerHeight=45,
        suppressMenuHide=True,
        animateRows=True
    )
    
    # Add custom CSS styling
    custom_css = {
        ".ag-theme-streamlit": {
            "--ag-background-color": "#1f1f1f",
            "--ag-foreground-color": "#ffffff",
            "--ag-header-background-color": "#2f2f2f",
            "--ag-header-foreground-color": "#ffffff",
            "--ag-odd-row-background-color": "#252525",
            "--ag-row-hover-color": "#3a3a3a",
            "--ag-selected-row-background-color": "#6BBBAE",
            "--ag-font-size": "14px",
            "--ag-row-height": "40px",
        }
    }
    
    # Build grid options
    grid_options = gb.build()
    
    # Display the grid
    st.markdown("### 📋 Interactive Holdings Table")
    st.markdown("*Click on any bond to view detailed analytics*")
    
    grid_response = AgGrid(
        display_data,
        gridOptions=grid_options,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        enable_enterprise_modules=False,
        height=400,
        theme='streamlit',
        custom_css=custom_css,
        allow_unsafe_jscode=True
    )
    
    # Handle row selection
    selected = grid_response['selected_rows']
    
    if selected is not None and len(selected) > 0:
        selected_bond = selected[0]
        display_bond_details(selected_bond)

def display_bond_details(bond_data):
    """Display detailed information for selected bond"""
    
    st.markdown("---")
    st.markdown(f"## 📊 Bond Details: {bond_data['name']}")
    
    # Create columns for bond details
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        st.markdown("### Basic Information")
        st.markdown(f"""
        <div style="background-color: #2a2a2a; padding: 1.5rem; border-radius: 10px;">
            <p><strong>Security Name:</strong> {bond_data['name']}</p>
            <p><strong>ISIN:</strong> {bond_data['isin']}</p>
            <p><strong>Region:</strong> {bond_data['region']}</p>
            <p><strong>Currency:</strong> {bond_data.get('currency', 'USD')}</p>
            <p><strong>Face Amount:</strong> ${bond_data.get('face_amount', 0):,.0f}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Pricing Information")
        st.markdown(f"""
        <div style="background-color: #2a2a2a; padding: 1.5rem; border-radius: 10px;">
            <p><strong>Current Price:</strong> {bond_data['closing_price']:.3f}</p>
            <p><strong>Accrued Interest:</strong> {bond_data['accrued_interest']:.3f}</p>
            <p><strong>Clean Price:</strong> {bond_data.get('clean_price', bond_data['closing_price']):.3f}</p>
            <p><strong>Dirty Price:</strong> {(bond_data['closing_price'] + bond_data['accrued_interest']):.3f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Analytics")
        
        # Key metrics
        metrics = {
            "Yield to Maturity": f"{float(bond_data['yield']):.3f}%",
            "Modified Duration": f"{float(bond_data['duration']):.2f} years",
            "Convexity": f"{bond_data.get('convexity', 'N/A')}",
            "Spread": f"{bond_data.get('spread', 'N/A')} bps",
            "DV01": f"${bond_data.get('dv01', 'N/A')}",
        }
        
        st.markdown("""
        <div style="background-color: #2a2a2a; padding: 1.5rem; border-radius: 10px;">
        """, unsafe_allow_html=True)
        
        for metric, value in metrics.items():
            st.markdown(f"<p><strong>{metric}:</strong> {value}</p>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("### Ratings")
        st.markdown(f"""
        <div style="background-color: #2a2a2a; padding: 1.5rem; border-radius: 10px;">
            <p><strong>NFA Rating:</strong> {bond_data.get('nfa_star_rating', 'N/A')} ⭐</p>
            <p><strong>ESG Score:</strong> {bond_data.get('esg', 'N/A')}</p>
            <p><strong>Credit Rating:</strong> {bond_data.get('credit_rating', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Portfolio weight visualization
        st.markdown("### Portfolio Weight")
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=float(bond_data['weighting']),
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Weight %"},
            gauge={
                'axis': {'range': [None, 10], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "#6BBBAE"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 2.5], 'color': '#9DB9D5'},
                    {'range': [2.5, 5], 'color': '#236192'},
                    {'range': [5, 7.5], 'color': '#21315C'},
                    {'range': [7.5, 10], 'color': '#6BBBAE'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 4
                }
            }
        ))
        
        fig.update_layout(
            height=250,
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            font={'color': "white", 'family': "Arial"}
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Historical price chart (mock data)
    st.markdown("### Price History (Last 12 Months)")
    
    # Generate mock historical data
    dates = pd.date_range(end=pd.Timestamp.now(), periods=252, freq='D')
    base_price = float(bond_data['closing_price'])
    price_volatility = 0.02  # 2% volatility
    prices = base_price + np.cumsum(np.random.randn(252) * price_volatility)
    
    price_df = pd.DataFrame({
        'Date': dates,
        'Price': prices
    })
    
    fig_price = px.line(price_df, x='Date', y='Price', 
                       title=f"{bond_data['name']} - Historical Price")
    
    fig_price.update_layout(
        height=300,
        plot_bgcolor='#1f1f1f',
        paper_bgcolor='#1f1f1f',
        font=dict(color='white'),
        xaxis=dict(gridcolor='#3a3a3a'),
        yaxis=dict(gridcolor='#3a3a3a')
    )
    
    st.plotly_chart(fig_price, use_container_width=True)
    
    # Additional analytics in expandable section
    with st.expander("📈 Advanced Analytics", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Scenario Analysis")
            scenarios = pd.DataFrame({
                'Rate Change': ['-100bp', '-50bp', 'Base', '+50bp', '+100bp'],
                'Price Impact': [
                    base_price * (1 + float(bond_data['duration']) * 0.01),
                    base_price * (1 + float(bond_data['duration']) * 0.005),
                    base_price,
                    base_price * (1 - float(bond_data['duration']) * 0.005),
                    base_price * (1 - float(bond_data['duration']) * 0.01)
                ]
            })
            
            fig_scenario = px.bar(scenarios, x='Rate Change', y='Price Impact',
                                 color='Price Impact', color_continuous_scale='RdYlGn')
            fig_scenario.update_layout(
                height=250,
                plot_bgcolor='#1f1f1f',
                paper_bgcolor='#1f1f1f',
                font=dict(color='white')
            )
            st.plotly_chart(fig_scenario, use_container_width=True)
        
        with col2:
            st.markdown("#### Cash Flow Schedule")
            # Mock cash flow data
            st.markdown("""
            <div style="background-color: #2a2a2a; padding: 1rem; border-radius: 8px;">
                <p><strong>Next Coupon:</strong> 2025-08-15</p>
                <p><strong>Coupon Rate:</strong> 3.5%</p>
                <p><strong>Frequency:</strong> Semi-Annual</p>
                <p><strong>Maturity:</strong> 2030-08-15</p>
                <p><strong>Years to Maturity:</strong> 5.6</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Action buttons
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 Full Analysis", type="primary", use_container_width=True):
            st.info("Would open detailed bond analysis...")
    
    with col2:
        if st.button("📈 Compare Bonds", use_container_width=True):
            st.info("Would open bond comparison tool...")
    
    with col3:
        if st.button("🔄 Trade History", use_container_width=True):
            st.info("Would show trade history...")
    
    with col4:
        if st.button("📥 Export Details", use_container_width=True):
            st.success("Bond details exported!")

# Example usage in report_utils.py
def create_enhanced_holdings_view(fund_data):
    """Enhanced holdings view with AG-Grid"""
    
    # Tab selection for view type
    view_tab1, view_tab2 = st.tabs(["📊 Interactive Table", "📋 Standard View"])
    
    with view_tab1:
        create_interactive_holdings_table(fund_data)
    
    with view_tab2:
        # Existing standard table view code
        st.markdown("### Standard Holdings Table")
        st.dataframe(fund_data, use_container_width=True)