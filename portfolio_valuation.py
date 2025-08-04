import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date, timedelta

def create_portfolio_valuation_page():
    """Create portfolio valuation page for GGI portfolio"""
    
    # Page header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #002855 0%, #4A5568 100%); 
                padding: 2rem; border-radius: 10px; margin-bottom: 2rem;">
        <h1 style="color: white; margin: 0;">💰 Portfolio Valuation</h1>
        <p style="color: #f0f0f0; margin: 0.5rem 0 0 0;">
        GGI Wealthy Nations Bond Fund - Full mark-to-market valuation with analytics
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load GGI portfolio data
    try:
        fund_data = pd.read_csv('data.csv')
        ggi_data = fund_data[fund_data['fund_name'] == 'Guinness Global Investors Fund'].copy()
        
        if ggi_data.empty:
            st.error("No GGI portfolio data found")
            return
            
        # Create valuation display
        create_valuation_summary(ggi_data)
        
        # Create tabs for different views
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Position Details", 
            "📈 P&L Analysis", 
            "🎯 Yield Analysis",
            "⏱️ Duration & Risk",
            "💹 Market Scenarios"
        ])
        
        with tab1:
            show_position_details(ggi_data)
        
        with tab2:
            show_pnl_analysis(ggi_data)
            
        with tab3:
            show_yield_analysis(ggi_data)
            
        with tab4:
            show_duration_risk(ggi_data)
            
        with tab5:
            show_scenario_analysis(ggi_data)
            
    except Exception as e:
        st.error(f"Error loading portfolio data: {str(e)}")

def create_valuation_summary(data):
    """Create top-level valuation summary"""
    
    # Calculate key metrics
    total_face = data['face_amount'].sum()
    total_market_value = data['market_value'].sum()
    total_cost = data['total_cost'].sum()
    total_pnl = total_market_value - total_cost
    pnl_pct = (total_pnl / total_cost) * 100 if total_cost > 0 else 0
    
    # Weighted averages (excluding cash)
    non_cash = data[data['name'] != 'Cash'].copy()
    non_cash['yield_numeric'] = pd.to_numeric(non_cash['yield'], errors='coerce')
    non_cash['duration_numeric'] = pd.to_numeric(non_cash['duration'], errors='coerce')
    
    # Calculate weighted metrics
    total_weight = non_cash['weighting'].sum()
    weighted_yield = (non_cash['yield_numeric'] * non_cash['weighting'] / total_weight).sum()
    weighted_duration = (non_cash['duration_numeric'] * non_cash['weighting'] / total_weight).sum()
    
    # Display summary cards
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div style="background-color: #2a2a2a; padding: 1.5rem; border-radius: 10px; text-align: center; border-left: 4px solid #E30613;">
            <h4 style="color: #E30613; margin: 0; font-size: 0.9rem;">TOTAL MARKET VALUE</h4>
            <h2 style="color: white; margin: 0.5rem 0; font-size: 1.8rem;">${total_market_value:,.0f}</h2>
            <p style="color: #888; margin: 0; font-size: 0.8rem;">Current portfolio value</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        color = "#66CC66" if total_pnl >= 0 else "#CC3333"
        arrow = "↑" if total_pnl >= 0 else "↓"
        st.markdown(f"""
        <div style="background-color: #2a2a2a; padding: 1.5rem; border-radius: 10px; text-align: center; border-left: 4px solid {color};">
            <h4 style="color: {color}; margin: 0; font-size: 0.9rem;">TOTAL P&L</h4>
            <h2 style="color: white; margin: 0.5rem 0; font-size: 1.8rem;">${total_pnl:,.0f}</h2>
            <p style="color: {color}; margin: 0; font-size: 0.9rem;">{arrow} {pnl_pct:.2f}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background-color: #2a2a2a; padding: 1.5rem; border-radius: 10px; text-align: center; border-left: 4px solid #002855;">
            <h4 style="color: #002855; margin: 0; font-size: 0.9rem;">PORTFOLIO YTM</h4>
            <h2 style="color: white; margin: 0.5rem 0; font-size: 1.8rem;">{weighted_yield:.3f}%</h2>
            <p style="color: #888; margin: 0; font-size: 0.8rem;">Weighted average</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style="background-color: #2a2a2a; padding: 1.5rem; border-radius: 10px; text-align: center; border-left: 4px solid #8B0000;">
            <h4 style="color: #8B0000; margin: 0; font-size: 0.9rem;">DURATION</h4>
            <h2 style="color: white; margin: 0.5rem 0; font-size: 1.8rem;">{weighted_duration:.2f}</h2>
            <p style="color: #888; margin: 0; font-size: 0.8rem;">Years (modified)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div style="background-color: #2a2a2a; padding: 1.5rem; border-radius: 10px; text-align: center; border-left: 4px solid #4A5568;">
            <h4 style="color: #4A5568; margin: 0; font-size: 0.9rem;">POSITIONS</h4>
            <h2 style="color: white; margin: 0.5rem 0; font-size: 1.8rem;">{len(non_cash)}</h2>
            <p style="color: #888; margin: 0; font-size: 0.8rem;">Active holdings</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Add spacing
    st.markdown("<br>", unsafe_allow_html=True)

def show_position_details(data):
    """Show detailed position-level valuation"""
    
    st.markdown("### Position-Level Valuation")
    
    # Prepare data for display
    display_data = data.copy()
    display_data['p&l'] = display_data['market_value'] - display_data['total_cost']
    display_data['p&l_pct'] = (display_data['p&l'] / display_data['total_cost'] * 100).round(2)
    
    # Select columns to display
    columns_to_show = [
        'name', 'isin', 'face_amount', 'closing_price', 
        'total_cost', 'market_value', 'p&l', 'p&l_pct',
        'yield', 'duration', 'weighting'
    ]
    
    # Format the dataframe
    formatted_df = display_data[columns_to_show].copy()
    formatted_df.columns = [
        'Security', 'ISIN', 'Face Amount', 'Price', 
        'Cost Basis', 'Market Value', 'P&L', 'P&L %',
        'YTM', 'Duration', 'Weight %'
    ]
    
    # Style the dataframe
    def color_pnl(val):
        if isinstance(val, (int, float)):
            color = '#66CC66' if val >= 0 else '#CC3333'
            return f'color: {color}'
        return ''
    
    styled_df = formatted_df.style.format({
        'Face Amount': '${:,.0f}',
        'Price': '{:.3f}',
        'Cost Basis': '${:,.0f}',
        'Market Value': '${:,.0f}',
        'P&L': '${:,.0f}',
        'P&L %': '{:.2f}%',
        'Weight %': '{:.2f}%'
    }).applymap(color_pnl, subset=['P&L', 'P&L %'])
    
    # Add filters
    col1, col2, col3 = st.columns(3)
    with col1:
        min_weight = st.slider("Min Weight %", 0.0, 10.0, 0.0)
    with col2:
        pnl_filter = st.selectbox("P&L Filter", ["All", "Profit", "Loss"])
    with col3:
        sort_by = st.selectbox("Sort By", ["Weight %", "P&L", "Market Value", "YTM"])
    
    # Apply filters
    filtered_df = formatted_df.copy()
    if min_weight > 0:
        filtered_df = filtered_df[filtered_df['Weight %'] >= min_weight]
    if pnl_filter == "Profit":
        filtered_df = filtered_df[filtered_df['P&L'] > 0]
    elif pnl_filter == "Loss":
        filtered_df = filtered_df[filtered_df['P&L'] < 0]
    
    # Sort
    filtered_df = filtered_df.sort_values(sort_by, ascending=False)
    
    # Display
    st.dataframe(
        filtered_df.style.format({
            'Face Amount': '${:,.0f}',
            'Price': '{:.3f}',
            'Cost Basis': '${:,.0f}',
            'Market Value': '${:,.0f}',
            'P&L': '${:,.0f}',
            'P&L %': '{:.2f}%',
            'Weight %': '{:.2f}%'
        }).applymap(color_pnl, subset=['P&L', 'P&L %']),
        use_container_width=True,
        height=400
    )
    
    # Summary stats
    st.markdown("#### Position Summary")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        profit_count = len(filtered_df[filtered_df['P&L'] > 0])
        st.metric("Profitable Positions", profit_count)
    with col2:
        loss_count = len(filtered_df[filtered_df['P&L'] < 0])
        st.metric("Loss Positions", loss_count)
    with col3:
        avg_pnl = filtered_df['P&L %'].mean()
        st.metric("Average P&L %", f"{avg_pnl:.2f}%")
    with col4:
        total_pnl = filtered_df['P&L'].sum()
        st.metric("Total P&L", f"${total_pnl:,.0f}")

def show_pnl_analysis(data):
    """Show P&L analysis and attribution"""
    
    st.markdown("### P&L Analysis & Attribution")
    
    # Calculate P&L
    data['p&l'] = data['market_value'] - data['total_cost']
    data['p&l_pct'] = (data['p&l'] / data['total_cost'] * 100)
    
    # Create P&L waterfall chart
    fig_waterfall = go.Figure(go.Waterfall(
        name="P&L",
        orientation="v",
        measure=["absolute", "relative", "relative", "relative", "relative", "total"],
        x=["Starting Value", "Price Change", "FX Impact", "Accrued Interest", "Other", "Current Value"],
        textposition="outside",
        text=[f"${data['total_cost'].sum():,.0f}", 
              f"${data['p&l'].sum() * 0.7:,.0f}",  # Mock attribution
              f"${data['p&l'].sum() * 0.1:,.0f}",
              f"${data['accrued_interest'].sum():,.0f}",
              f"${data['p&l'].sum() * 0.2 - data['accrued_interest'].sum():,.0f}",
              f"${data['market_value'].sum():,.0f}"],
        y=[data['total_cost'].sum(), 
           data['p&l'].sum() * 0.7,
           data['p&l'].sum() * 0.1,
           data['accrued_interest'].sum(),
           data['p&l'].sum() * 0.2 - data['accrued_interest'].sum(),
           data['market_value'].sum()],
        connector={"line": {"color": "rgb(63, 63, 63)"}},
    ))
    
    fig_waterfall.update_layout(
        title="P&L Attribution Waterfall",
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig_waterfall, use_container_width=True)
    
    # P&L by region
    col1, col2 = st.columns(2)
    
    with col1:
        # P&L by region pie chart
        region_pnl = data.groupby('region')['p&l'].sum().reset_index()
        region_pnl = region_pnl[region_pnl['p&l'] != 0]
        
        fig_region = px.pie(
            region_pnl, 
            values='p&l', 
            names='region',
            title="P&L by Region",
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        st.plotly_chart(fig_region, use_container_width=True)
    
    with col2:
        # Top movers table
        st.markdown("#### Top Movers")
        top_gainers = data.nlargest(5, 'p&l')[['name', 'p&l', 'p&l_pct']]
        top_losers = data.nsmallest(5, 'p&l')[['name', 'p&l', 'p&l_pct']]
        
        st.markdown("**Top Gainers**")
        st.dataframe(
            top_gainers.style.format({
                'p&l': '${:,.0f}',
                'p&l_pct': '{:.2f}%'
            }).applymap(lambda x: 'color: #66CC66; font-weight: bold' if isinstance(x, (int, float)) else '', subset=['p&l_pct']),
            use_container_width=True,
            hide_index=True
        )
        
        st.markdown("**Top Losers**")
        st.dataframe(
            top_losers.style.format({
                'p&l': '${:,.0f}',
                'p&l_pct': '{:.2f}%'
            }).applymap(lambda x: 'color: #CC3333; font-weight: bold' if isinstance(x, (int, float)) else '', subset=['p&l_pct']),
            use_container_width=True,
            hide_index=True
        )

def show_yield_analysis(data):
    """Show yield analysis and distribution"""
    
    st.markdown("### Yield Analysis")
    
    # Clean yield data
    non_cash = data[data['name'] != 'Cash'].copy()
    non_cash['yield_numeric'] = pd.to_numeric(non_cash['yield'], errors='coerce')
    
    # Yield distribution histogram
    fig_hist = px.histogram(
        non_cash,
        x='yield_numeric',
        nbins=20,
        title="Yield Distribution",
        labels={'yield_numeric': 'Yield to Maturity (%)', 'count': 'Number of Bonds'},
        color_discrete_sequence=['#E30613']
    )
    fig_hist.update_layout(height=400)
    st.plotly_chart(fig_hist, use_container_width=True)
    
    # Yield vs Duration scatter
    fig_scatter = px.scatter(
        non_cash,
        x='duration',
        y='yield_numeric',
        size='weighting',
        color='region',
        title="Yield vs Duration by Region",
        labels={'yield_numeric': 'Yield (%)', 'duration': 'Duration (years)'},
        hover_data=['name', 'weighting']
    )
    fig_scatter.update_layout(height=400)
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Yield statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Min Yield", f"{non_cash['yield_numeric'].min():.3f}%")
    with col2:
        st.metric("Max Yield", f"{non_cash['yield_numeric'].max():.3f}%")
    with col3:
        st.metric("Median Yield", f"{non_cash['yield_numeric'].median():.3f}%")
    with col4:
        st.metric("Std Dev", f"{non_cash['yield_numeric'].std():.3f}%")
    
    # Yield buckets
    st.markdown("#### Yield Buckets")
    bins = [0, 3, 4, 5, 6, 7, 100]
    labels = ['< 3%', '3-4%', '4-5%', '5-6%', '6-7%', '> 7%']
    non_cash['yield_bucket'] = pd.cut(non_cash['yield_numeric'], bins=bins, labels=labels)
    
    bucket_summary = non_cash.groupby('yield_bucket').agg({
        'weighting': 'sum',
        'market_value': 'sum',
        'name': 'count'
    }).reset_index()
    bucket_summary.columns = ['Yield Range', 'Weight %', 'Market Value', 'Count']
    
    st.dataframe(
        bucket_summary.style.format({
            'Weight %': '{:.2f}%',
            'Market Value': '${:,.0f}'
        }),
        use_container_width=True,
        hide_index=True
    )

def show_duration_risk(data):
    """Show duration and risk analysis"""
    
    st.markdown("### Duration & Risk Analysis")
    
    # Clean data
    non_cash = data[data['name'] != 'Cash'].copy()
    non_cash['duration_numeric'] = pd.to_numeric(non_cash['duration'], errors='coerce')
    
    # Duration distribution
    col1, col2 = st.columns(2)
    
    with col1:
        # Duration buckets pie chart
        bins = [0, 3, 5, 7, 10, 15, 100]
        labels = ['0-3Y', '3-5Y', '5-7Y', '7-10Y', '10-15Y', '>15Y']
        non_cash['duration_bucket'] = pd.cut(non_cash['duration_numeric'], bins=bins, labels=labels)
        
        duration_dist = non_cash.groupby('duration_bucket')['weighting'].sum().reset_index()
        
        fig_duration = px.pie(
            duration_dist,
            values='weighting',
            names='duration_bucket',
            title="Duration Distribution",
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
        st.plotly_chart(fig_duration, use_container_width=True)
    
    with col2:
        # Key rate duration ladder
        st.markdown("#### Key Rate Exposures")
        
        # Mock key rate durations
        key_rates = pd.DataFrame({
            'Tenor': ['2Y', '5Y', '7Y', '10Y', '20Y', '30Y'],
            'Duration Contribution': [0.5, 1.2, 1.8, 2.1, 1.1, 0.3]
        })
        
        fig_bar = px.bar(
            key_rates,
            x='Tenor',
            y='Duration Contribution',
            title="Duration Contribution by Tenor",
            color='Duration Contribution',
            color_continuous_scale='RdBu'
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Risk metrics
    st.markdown("#### Risk Metrics")
    
    # Calculate portfolio risk metrics
    total_duration = (non_cash['duration_numeric'] * non_cash['weighting'] / non_cash['weighting'].sum()).sum()
    
    # DV01 calculation (simplified)
    portfolio_value = data['market_value'].sum()
    dv01 = portfolio_value * total_duration * 0.0001  # 1bp move
    
    # Convexity (mock)
    total_convexity = 89.5  # Mock value
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div style="background-color: #2a2a2a; padding: 1rem; border-radius: 8px;">
            <h5 style="color: #E30613; margin: 0;">DV01</h5>
            <h3 style="color: white; margin: 0.5rem 0;">${:,.0f}</h3>
            <p style="color: #888; margin: 0; font-size: 0.9rem;">Per 1bp move</p>
        </div>
        """.format(dv01), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: #2a2a2a; padding: 1rem; border-radius: 8px;">
            <h5 style="color: #002855; margin: 0;">Convexity</h5>
            <h3 style="color: white; margin: 0.5rem 0;">{:.1f}</h3>
            <p style="color: #888; margin: 0; font-size: 0.9rem;">Portfolio convexity</p>
        </div>
        """.format(total_convexity), unsafe_allow_html=True)
    
    with col3:
        spread_duration = total_duration * 0.85  # Mock adjustment
        st.markdown("""
        <div style="background-color: #2a2a2a; padding: 1rem; border-radius: 8px;">
            <h5 style="color: #8B0000; margin: 0;">Spread Duration</h5>
            <h3 style="color: white; margin: 0.5rem 0;">{:.2f}</h3>
            <p style="color: #888; margin: 0; font-size: 0.9rem;">Credit sensitivity</p>
        </div>
        """.format(spread_duration), unsafe_allow_html=True)
    
    with col4:
        var_95 = portfolio_value * 0.025  # Mock 95% VaR
        st.markdown("""
        <div style="background-color: #2a2a2a; padding: 1rem; border-radius: 8px;">
            <h5 style="color: #4A5568; margin: 0;">VaR (95%)</h5>
            <h3 style="color: white; margin: 0.5rem 0;">${:,.0f}</h3>
            <p style="color: #888; margin: 0; font-size: 0.9rem;">1-day VaR</p>
        </div>
        """.format(var_95), unsafe_allow_html=True)

def show_scenario_analysis(data):
    """Show scenario analysis"""
    
    st.markdown("### Market Scenario Analysis")
    
    # Calculate base metrics
    portfolio_value = data['market_value'].sum()
    non_cash = data[data['name'] != 'Cash'].copy()
    non_cash['duration_numeric'] = pd.to_numeric(non_cash['duration'], errors='coerce')
    total_duration = (non_cash['duration_numeric'] * non_cash['weighting'] / non_cash['weighting'].sum()).sum()
    
    # Define scenarios
    scenarios = {
        'Severe Recession': {'rates': -200, 'spreads': 150, 'fx': -5},
        'Mild Recession': {'rates': -100, 'spreads': 50, 'fx': -2},
        'Base Case': {'rates': 0, 'spreads': 0, 'fx': 0},
        'Gradual Tightening': {'rates': 50, 'spreads': -25, 'fx': 1},
        'Aggressive Tightening': {'rates': 150, 'spreads': 75, 'fx': 3},
        'Inflation Shock': {'rates': 250, 'spreads': 100, 'fx': 5}
    }
    
    # Calculate scenario impacts
    scenario_results = []
    for scenario_name, params in scenarios.items():
        # Simplified calculation
        rate_impact = -total_duration * params['rates'] / 100
        spread_impact = -total_duration * 0.85 * params['spreads'] / 10000
        fx_impact = params['fx'] / 100
        
        total_impact = rate_impact + spread_impact + fx_impact
        new_value = portfolio_value * (1 + total_impact)
        pnl = new_value - portfolio_value
        
        scenario_results.append({
            'Scenario': scenario_name,
            'Rate Change': f"{params['rates']:+d} bps",
            'Spread Change': f"{params['spreads']:+d} bps",
            'FX Impact': f"{params['fx']:+.1f}%",
            'Portfolio Value': new_value,
            'P&L': pnl,
            'P&L %': total_impact * 100
        })
    
    scenario_df = pd.DataFrame(scenario_results)
    
    # Create scenario chart
    fig_scenarios = go.Figure()
    
    # Add bar chart
    colors = ['#CC3333' if x < 0 else '#66CC66' for x in scenario_df['P&L %']]
    fig_scenarios.add_trace(go.Bar(
        x=scenario_df['Scenario'],
        y=scenario_df['P&L %'],
        text=[f"{x:.2f}%" for x in scenario_df['P&L %']],
        textposition='outside',
        marker_color=colors
    ))
    
    fig_scenarios.update_layout(
        title="Portfolio Impact by Scenario",
        yaxis_title="Portfolio Return (%)",
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig_scenarios, use_container_width=True)
    
    # Scenario details table
    st.markdown("#### Scenario Details")
    
    # Format and display scenario table
    st.dataframe(
        scenario_df.style.format({
            'Portfolio Value': '${:,.0f}',
            'P&L': '${:,.0f}',
            'P&L %': '{:.2f}%'
        }).applymap(
            lambda x: 'color: #66CC66' if isinstance(x, (int, float)) and x > 0 
            else 'color: #CC3333' if isinstance(x, (int, float)) and x < 0 
            else '', 
            subset=['P&L', 'P&L %']
        ),
        use_container_width=True,
        hide_index=True
    )
    
    # Stress test matrix
    st.markdown("#### Interest Rate Sensitivity Matrix")
    
    # Create rate/spread matrix
    rate_changes = [-200, -100, -50, 0, 50, 100, 200]
    spread_changes = [-50, 0, 50, 100, 150]
    
    matrix_data = []
    for spread in spread_changes:
        row = []
        for rate in rate_changes:
            impact = -total_duration * rate / 100 - total_duration * 0.85 * spread / 10000
            row.append(impact * 100)
        matrix_data.append(row)
    
    matrix_df = pd.DataFrame(
        matrix_data,
        columns=[f"{r:+d}bp" for r in rate_changes],
        index=[f"{s:+d}bp" for s in spread_changes]
    )
    
    # Create heatmap
    fig_heatmap = px.imshow(
        matrix_df,
        labels=dict(x="Rate Change", y="Spread Change", color="P&L %"),
        color_continuous_scale="RdBu",
        color_continuous_midpoint=0,
        title="P&L Impact Matrix (%)"
    )
    fig_heatmap.update_layout(height=400)
    st.plotly_chart(fig_heatmap, use_container_width=True)

# CSS for additional styling
def add_valuation_styles():
    st.markdown("""
    <style>
    /* Valuation page specific styles */
    .stMetric {
        background-color: #2a2a2a;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #E30613;
    }
    
    /* Custom number formatting */
    .positive-value {
        color: #66CC66;
    }
    
    .negative-value {
        color: #CC3333;
    }
    </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    st.set_page_config(
        page_title="Portfolio Valuation - GGI",
        page_icon="💰",
        layout="wide"
    )
    add_valuation_styles()
    create_portfolio_valuation_page()