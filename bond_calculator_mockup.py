import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date
import numpy as np

def create_bond_calculator_page():
    """Create the bond calculator page with mock data"""
    
    # Create tabs for different input methods
    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 Single Bond", 
        "📊 Google Sheets Import", 
        "📁 Portfolio Analysis",
        "🔄 Bulk Processing"
    ])
    
    with tab1:
        create_single_bond_tab()
    
    with tab2:
        create_google_sheets_tab()
    
    with tab3:
        create_portfolio_analysis_tab()
    
    with tab4:
        create_bulk_processing_tab()

def create_single_bond_tab():
    """Single bond calculation interface"""
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Bond Input")
        
        # Input method selection
        input_type = st.radio(
            "Input Method:",
            ["ISIN Code", "Bond Description"],
            horizontal=True
        )
        
        if input_type == "ISIN Code":
            isin = st.text_input("ISIN Code", placeholder="US912810RG64")
        else:
            description = st.text_input("Bond Description", placeholder="T 3.5 02/15/2029")
        
        # Price and settlement inputs
        col1a, col1b = st.columns(2)
        with col1a:
            price = st.number_input("Price", min_value=0.0, max_value=200.0, value=99.5, step=0.125)
        with col1b:
            settlement = st.date_input("Settlement Date", value=date.today())
        
        # Additional parameters in expander
        with st.expander("Advanced Parameters"):
            col1c, col1d = st.columns(2)
            with col1c:
                face_value = st.number_input("Face Value", value=1000000, step=100000)
                frequency = st.selectbox("Coupon Frequency", ["Semi-Annual", "Annual", "Quarterly"])
            with col1d:
                day_count = st.selectbox("Day Count", ["30/360", "Actual/Actual", "Actual/360"])
                eom_adjust = st.checkbox("End of Month Adjustment")
        
        # Calculate button
        if st.button("🚀 Calculate Analytics", type="primary", use_container_width=True):
            with st.spinner("Calling XTrillion Bond Analytics API..."):
                # Simulate API call delay
                import time
                time.sleep(1)
                st.success("✅ Calculation complete!")
    
    with col2:
        st.markdown("### Results")
        
        # Mock results display
        metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
        
        with metrics_col1:
            st.metric("YTM", "4.567%", "+0.12%", help="Yield to Maturity")
        with metrics_col2:
            st.metric("Duration", "7.234", "-0.05", help="Modified Duration in years")
        with metrics_col3:
            st.metric("Convexity", "65.43", help="Price sensitivity to yield changes")
        with metrics_col4:
            st.metric("DV01", "$723.40", help="Dollar value of 1bp move")
        
        # Detailed results table
        st.markdown("#### Detailed Analytics")
        results_data = {
            "Metric": ["Clean Price", "Dirty Price", "Accrued Interest", "Macaulay Duration", 
                       "Modified Duration", "Effective Duration", "Spread to Treasury", "Z-Spread", 
                       "OAS", "Credit Spread"],
            "Value": ["99.500", "101.234", "1.734", "7.456", "7.234", "7.189", 
                     "127 bps", "132 bps", "118 bps", "145 bps"],
            "Change": ["-0.125", "-0.089", "+0.036", "-0.012", "-0.050", "-0.048", 
                      "+5 bps", "+7 bps", "+3 bps", "+8 bps"]
        }
        results_df = pd.DataFrame(results_data)
        
        # Style the dataframe - remove gradient since Change contains strings
        st.dataframe(
            results_df,
            use_container_width=True,
            hide_index=True
        )

def create_google_sheets_tab():
    """Google Sheets import interface"""
    st.markdown("### Import Bond Portfolio from Google Sheets")
    
    # Connection status indicator
    col1, col2 = st.columns([3, 1])
    with col1:
        sheet_url = st.text_input(
            "Google Sheets URL",
            placeholder="https://docs.google.com/spreadsheets/d/abc123..."
        )
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if sheet_url:
            st.success("✅ Connected")
        else:
            st.info("🔗 Not connected")
    
    # Mock preview of sheet data
    if sheet_url:
        st.markdown("#### Sheet Preview")
        
        # Create mock data
        mock_sheet_data = pd.DataFrame({
            "ISIN": ["US912810RG64", "US912810QZ89", "GB00B24FF097", "XS1234567890", "US91282ABC12"],
            "Description": ["T 2.5 05/15/2030", "T 3.0 08/15/2028", "UKT 4.25 12/07/2040", 
                           "AAPL 3.45 02/09/2029", "T 1.75 11/15/2029"],
            "Price": [98.5, 99.125, 112.375, 102.25, 95.875],
            "Face Amount": [1000000, 500000, 750000, 2000000, 1500000],
            "Settlement": ["2024-01-15", "2024-01-15", "2024-01-15", "2024-01-15", "2024-01-15"]
        })
        
        # Editable dataframe
        edited_df = st.data_editor(
            mock_sheet_data,
            use_container_width=True,
            num_rows="dynamic",
            column_config={
                "Price": st.column_config.NumberColumn(min_value=0, max_value=200, step=0.125),
                "Face Amount": st.column_config.NumberColumn(min_value=0, step=100000),
                "Settlement": st.column_config.DateColumn()
            }
        )
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄 Refresh from Sheet", use_container_width=True):
                st.info("Sheet refreshed!")
        with col2:
            if st.button("💾 Save to Sheet", use_container_width=True):
                st.success("Changes saved!")
        with col3:
            if st.button("🚀 Calculate All", type="primary", use_container_width=True):
                with st.spinner(f"Processing {len(edited_df)} bonds..."):
                    progress = st.progress(0)
                    for i in range(len(edited_df)):
                        progress.progress((i + 1) / len(edited_df))
                        import time
                        time.sleep(0.2)
                    st.success("All calculations complete!")
                    
                    # Show summary results
                    show_batch_results()

def show_batch_results():
    """Display batch calculation results"""
    st.markdown("### Calculation Results")
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Bonds Processed", "5", help="Total bonds calculated")
    with col2:
        st.metric("Avg YTM", "3.856%", "+0.234%", help="Portfolio average yield")
    with col3:
        st.metric("Avg Duration", "8.456", help="Portfolio average duration")
    with col4:
        st.metric("Total Market Value", "$5,234,567", help="Sum of all positions")
    
    # Results table
    results_df = pd.DataFrame({
        "ISIN": ["US912810RG64", "US912810QZ89", "GB00B24FF097", "XS1234567890", "US91282ABC12"],
        "YTM (%)": [2.567, 3.234, 4.123, 3.789, 2.345],
        "Duration": [7.234, 5.678, 12.345, 6.789, 8.234],
        "Convexity": [65.43, 45.67, 123.45, 56.78, 78.90],
        "Clean Price": [98.500, 99.125, 112.375, 102.250, 95.875],
        "Accrued": [0.234, 0.567, 1.234, 0.789, 0.345],
        "Status": ["✅ Success", "✅ Success", "✅ Success", "✅ Success", "✅ Success"]
    })
    
    # Apply styling with proper numeric columns
    styled_df = results_df.style.format({
        'YTM (%)': '{:.3f}',
        'Duration': '{:.3f}',
        'Convexity': '{:.2f}',
        'Clean Price': '{:.3f}',
        'Accrued': '{:.3f}'
    })
    
    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True
    )
    
    # Export options
    col1, col2, col3 = st.columns(3)
    with col1:
        st.download_button(
            "📥 Download CSV",
            data="mock_csv_data",
            file_name="bond_calculations.csv",
            mime="text/csv"
        )
    with col2:
        st.download_button(
            "📊 Download Excel",
            data="mock_excel_data",
            file_name="bond_calculations.xlsx"
        )
    with col3:
        st.button("📤 Update Google Sheet", use_container_width=True)

def create_portfolio_analysis_tab():
    """Portfolio-level analysis interface"""
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Select Portfolio")
        
        portfolio = st.selectbox(
            "Choose Portfolio",
            ["GGI Wealthy Nations Bond Fund", "SKEWNBF", "SKESBF", "Custom Portfolio"]
        )
        
        analysis_date = st.date_input("Analysis Date", value=date.today())
        
        st.markdown("### Analysis Options")
        
        # Analysis toggles
        calc_options = {
            "Calculate Greeks": st.checkbox("Calculate Greeks", value=True),
            "Scenario Analysis": st.checkbox("Scenario Analysis", value=True),
            "Cash Flow Projection": st.checkbox("Cash Flow Projection", value=False),
            "Risk Metrics": st.checkbox("Risk Metrics", value=True),
            "Performance Attribution": st.checkbox("Performance Attribution", value=False)
        }
        
        if st.button("🎯 Run Portfolio Analysis", type="primary", use_container_width=True):
            st.info("Analysis would run here...")
    
    with col2:
        st.markdown("### Portfolio Analytics Dashboard")
        
        # Create tabs for different views
        view1, view2, view3, view4 = st.tabs(["Overview", "Risk Analysis", "Scenario", "Cash Flows"])
        
        with view1:
            # Portfolio overview metrics
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.metric("Portfolio YTM", "4.234%", "+0.156%")
            with m2:
                st.metric("Effective Duration", "7.89", "-0.23")
            with m3:
                st.metric("Convexity", "89.45")
            with m4:
                st.metric("Spread", "156 bps", "+8 bps")
            
            # Mock yield curve
            fig = create_mock_yield_curve()
            st.plotly_chart(fig, use_container_width=True)
        
        with view2:
            # Risk metrics
            st.markdown("#### Risk Decomposition")
            
            risk_data = pd.DataFrame({
                "Risk Factor": ["Interest Rate", "Credit Spread", "Currency", "Liquidity", "Other"],
                "Contribution (%)": [45, 30, 15, 7, 3],
                "VaR ($)": [125000, 83000, 41500, 19400, 8300]
            })
            
            # Create donut chart
            fig = px.pie(risk_data, values='Contribution (%)', names='Risk Factor', hole=0.4)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(
                height=300,
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(risk_data, use_container_width=True, hide_index=True)
        
        with view3:
            # Scenario analysis
            st.markdown("#### Interest Rate Scenarios")
            
            scenarios_df = pd.DataFrame({
                "Scenario": ["Base", "-100bps", "-50bps", "+50bps", "+100bps", "+200bps"],
                "Portfolio Value": [100.00, 108.45, 104.12, 96.23, 92.78, 86.45],
                "P&L (%)": [0.00, 8.45, 4.12, -3.77, -7.22, -13.55]
            })
            
            # Create scenario chart
            fig = px.bar(scenarios_df, x="Scenario", y="P&L (%)", 
                        color="P&L (%)", color_continuous_scale="RdYlGn")
            fig.update_layout(
                height=300,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)

def create_bulk_processing_tab():
    """Bulk processing interface"""
    st.markdown("### Bulk Bond Processing")
    
    # File upload section
    upload_col1, upload_col2 = st.columns([2, 1])
    
    with upload_col1:
        uploaded_file = st.file_uploader(
            "Upload bond list (CSV, Excel, or JSON)",
            type=['csv', 'xlsx', 'json'],
            help="File should contain ISIN/Description, Price, and Settlement Date columns"
        )
        
        if uploaded_file:
            st.success(f"✅ Uploaded: {uploaded_file.name}")
            
            # Show file preview
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
                st.markdown(f"**Found {len(df)} bonds to process**")
                st.dataframe(df.head(), use_container_width=True)
    
    with upload_col2:
        st.markdown("#### Processing Options")
        
        batch_size = st.number_input("Batch Size", min_value=1, max_value=100, value=10)
        parallel = st.checkbox("Parallel Processing", value=True)
        save_results = st.checkbox("Auto-save Results", value=True)
        
        if uploaded_file:
            if st.button("⚡ Start Bulk Processing", type="primary", use_container_width=True):
                # Mock processing with progress
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i in range(100):
                    progress_bar.progress(i + 1)
                    status_text.text(f"Processing bond {i+1} of 100...")
                    import time
                    time.sleep(0.05)
                
                st.balloons()
                st.success("🎉 All bonds processed successfully!")

def create_mock_yield_curve():
    """Create a mock yield curve chart"""
    # Generate mock data
    tenors = [0.25, 0.5, 1, 2, 3, 5, 7, 10, 20, 30]
    yields = [3.2, 3.5, 3.8, 4.0, 4.1, 4.2, 4.25, 4.3, 4.4, 4.45]
    portfolio_points = [
        {"tenor": 5, "yield": 4.5, "name": "AAPL 3.45"},
        {"tenor": 7, "yield": 4.8, "name": "MSFT 4.20"},
        {"tenor": 10, "yield": 4.9, "name": "T 3.50"},
    ]
    
    fig = go.Figure()
    
    # Add yield curve
    fig.add_trace(go.Scatter(
        x=tenors,
        y=yields,
        mode='lines+markers',
        name='Treasury Curve',
        line=dict(color='#002855', width=3),
        marker=dict(size=8)
    ))
    
    # Add portfolio bonds
    for point in portfolio_points:
        fig.add_trace(go.Scatter(
            x=[point["tenor"]],
            y=[point["yield"]],
            mode='markers+text',
            name=point["name"],
            marker=dict(size=12, symbol='diamond'),
            text=[point["name"]],
            textposition="top center"
        ))
    
    fig.update_layout(
        title="Portfolio Positioning vs Treasury Curve",
        xaxis_title="Maturity (Years)",
        yaxis_title="Yield (%)",
        hovermode='x',
        height=400,
        plot_bgcolor='white',
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    
    fig.update_xaxes(gridcolor='lightgray')
    fig.update_yaxes(gridcolor='lightgray')
    
    return fig

# Add custom CSS for better styling
def add_custom_styles():
    st.markdown("""
    <style>
    /* Custom metric card styling */
    div[data-testid="metric-container"] {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
        background-color: #f0f0f0;
        border-radius: 8px 8px 0 0;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #E30613;
        color: white;
    }
    
    /* Button styling */
    .stButton > button[kind="primary"] {
        background-color: #C8102E;
        color: white;
        border: none;
        font-weight: bold;
    }
    
    .stButton > button[kind="primary"]:hover {
        background-color: #21315C;
    }
    
    /* Success/Info/Warning boxes */
    .stSuccess, .stInfo {
        padding: 0.75rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    st.set_page_config(
        page_title="Bond Calculator - Guinness Global Investors",
        page_icon="🧮",
        layout="wide"
    )
    add_custom_styles()
    create_bond_calculator_page()