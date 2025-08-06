import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

def create_trade_calculator_page():
    """Create the trade calculator page for simulating portfolio changes"""
    
    st.markdown("## 💱 Trade Calculator")
    st.markdown("Simulate the impact of selling bonds from your portfolio")
    
    # Load portfolio data
    try:
        fund_data = pd.read_csv('data.csv')
        ggi_data = fund_data[fund_data['fund_name'] == 'Guinness Global Investors Fund'].copy()
        
        if ggi_data.empty:
            st.error("No portfolio data found")
            return
            
        # Initialize session state for trades
        if 'pending_trades' not in st.session_state:
            st.session_state.pending_trades = []
        
        if 'trade_history' not in st.session_state:
            st.session_state.trade_history = []
            
        # Create tabs
        tab1, tab2, tab3 = st.tabs(["📉 Sell Bonds", "📊 Impact Analysis", "📜 Trade History"])
        
        with tab1:
            create_sell_interface(ggi_data)
            
        with tab2:
            show_impact_analysis(ggi_data)
            
        with tab3:
            show_trade_history()
            
    except Exception as e:
        st.error(f"Error loading portfolio data: {str(e)}")

def create_sell_interface(portfolio_data):
    """Interface for selecting and selling bonds"""
    
    st.markdown("### Select Bonds to Sell")
    
    # Filter out cash from sellable bonds
    sellable_bonds = portfolio_data[portfolio_data['name'] != 'Cash'].copy()
    
    # Create selection interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Bond selector
        selected_bond = st.selectbox(
            "Choose Bond to Sell",
            options=sellable_bonds['name'].tolist(),
            format_func=lambda x: f"{x} ({sellable_bonds[sellable_bonds['name']==x]['isin'].iloc[0]})",
            key="bond_selector"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("ℹ️ Bond Details", use_container_width=True):
            st.session_state.show_bond_details = True
    
    # Get selected bond details
    if selected_bond:
        bond_details = sellable_bonds[sellable_bonds['name'] == selected_bond].iloc[0]
        
        # Show bond information
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Current Price", f"{bond_details['closing_price']:.3f}")
        with col2:
            st.metric("Face Amount", f"${bond_details['face_amount']:,.0f}")
        with col3:
            st.metric("Weight %", f"{bond_details['weighting']:.2f}%")
        with col4:
            st.metric("YTM", f"{bond_details['yield']}")
        
        # Sell amount interface
        st.markdown("### Specify Sale Amount")
        
        col1, col2 = st.columns(2)
        
        with col1:
            sale_method = st.radio(
                "Sale Method",
                ["By Face Amount", "By Percentage", "Sell All"],
                horizontal=True
            )
        
        with col2:
            if sale_method == "By Face Amount":
                max_face = bond_details['face_amount']
                sale_amount = st.number_input(
                    "Face Amount to Sell",
                    min_value=0,
                    max_value=int(max_face),
                    value=int(max_face * 0.5),
                    step=100000,
                    format="%d"
                )
                sale_percentage = (sale_amount / max_face) * 100
            elif sale_method == "By Percentage":
                sale_percentage = st.slider(
                    "Percentage to Sell",
                    min_value=0,
                    max_value=100,
                    value=50,
                    step=5,
                    format="%d%%"
                )
                sale_amount = bond_details['face_amount'] * (sale_percentage / 100)
            else:  # Sell All
                sale_amount = bond_details['face_amount']
                sale_percentage = 100
                st.info("Selling entire position")
        
        # Calculate proceeds
        sale_price = st.number_input(
            "Sale Price (per 100 face)",
            min_value=50.0,
            max_value=150.0,
            value=float(bond_details['closing_price']),
            step=0.125,
            help="Default is current market price"
        )
        
        # Calculate sale details
        proceeds = (sale_amount / 100) * sale_price
        market_value_sold = (sale_amount / bond_details['face_amount']) * bond_details['market_value']
        cost_basis_sold = (sale_amount / bond_details['face_amount']) * bond_details['total_cost']
        realized_pnl = proceeds - cost_basis_sold
        pnl_percentage = (realized_pnl / cost_basis_sold * 100) if cost_basis_sold > 0 else 0
        
        # Display sale summary
        st.markdown("### Sale Summary")
        
        summary_col1, summary_col2, summary_col3 = st.columns(3)
        
        with summary_col1:
            st.markdown(f"""
            <div style="background-color: #2a2a2a; padding: 1.5rem; border-radius: 10px;">
                <h5 style="color: #9DB9D5; margin: 0;">Sale Details</h5>
                <p style="margin: 0.5rem 0;"><strong>Face Amount:</strong> ${sale_amount:,.0f}</p>
                <p style="margin: 0.5rem 0;"><strong>Sale Price:</strong> {sale_price:.3f}</p>
                <p style="margin: 0.5rem 0;"><strong>Portion Sold:</strong> {sale_percentage:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        with summary_col2:
            st.markdown(f"""
            <div style="background-color: #2a2a2a; padding: 1.5rem; border-radius: 10px;">
                <h5 style="color: #9DB9D5; margin: 0;">Financial Impact</h5>
                <p style="margin: 0.5rem 0;"><strong>Gross Proceeds:</strong> ${proceeds:,.0f}</p>
                <p style="margin: 0.5rem 0;"><strong>Cost Basis:</strong> ${cost_basis_sold:,.0f}</p>
                <p style="margin: 0.5rem 0;"><strong>Market Value:</strong> ${market_value_sold:,.0f}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with summary_col3:
            pnl_color = "#66CC66" if realized_pnl >= 0 else "#CC3333"
            arrow = "↑" if realized_pnl >= 0 else "↓"
            st.markdown(f"""
            <div style="background-color: #2a2a2a; padding: 1.5rem; border-radius: 10px;">
                <h5 style="color: {pnl_color}; margin: 0;">Realized P&L</h5>
                <p style="margin: 0.5rem 0; color: {pnl_color}; font-size: 1.5rem; font-weight: bold;">
                    ${realized_pnl:,.0f}
                </p>
                <p style="margin: 0.5rem 0; color: {pnl_color};">
                    {arrow} {pnl_percentage:.2f}%
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Trade actions
        st.markdown("---")
        action_col1, action_col2, action_col3 = st.columns([2, 1, 1])
        
        with action_col1:
            trade_notes = st.text_input("Trade Notes (optional)", placeholder="Reason for sale...")
        
        with action_col2:
            if st.button("🔍 Preview Impact", type="secondary", use_container_width=True):
                # Add to pending trades
                trade = {
                    'timestamp': datetime.now(),
                    'bond_name': selected_bond,
                    'isin': bond_details['isin'],
                    'action': 'SELL',
                    'face_amount': sale_amount,
                    'price': sale_price,
                    'proceeds': proceeds,
                    'cost_basis': cost_basis_sold,
                    'realized_pnl': realized_pnl,
                    'pnl_percentage': pnl_percentage,
                    'notes': trade_notes,
                    'status': 'PENDING'
                }
                st.session_state.pending_trades.append(trade)
                st.success("Trade added to preview")
                st.rerun()
        
        with action_col3:
            if st.button("💾 Execute Trade", type="primary", use_container_width=True):
                # Execute the trade
                trade = {
                    'timestamp': datetime.now(),
                    'bond_name': selected_bond,
                    'isin': bond_details['isin'],
                    'action': 'SELL',
                    'face_amount': sale_amount,
                    'price': sale_price,
                    'proceeds': proceeds,
                    'cost_basis': cost_basis_sold,
                    'realized_pnl': realized_pnl,
                    'pnl_percentage': pnl_percentage,
                    'notes': trade_notes,
                    'status': 'EXECUTED'
                }
                st.session_state.trade_history.append(trade)
                st.balloons()
                st.success(f"✅ Trade executed! Sold ${sale_amount:,.0f} of {selected_bond}")

def show_impact_analysis(portfolio_data):
    """Show the impact of pending trades on the portfolio"""
    
    st.markdown("### Portfolio Impact Analysis")
    
    if not st.session_state.pending_trades:
        st.info("No pending trades. Use the 'Sell Bonds' tab to create trades.")
        return
    
    # Calculate current portfolio metrics
    current_metrics = calculate_portfolio_metrics(portfolio_data)
    
    # Apply pending trades to get new portfolio
    modified_portfolio = apply_pending_trades(portfolio_data.copy())
    new_metrics = calculate_portfolio_metrics(modified_portfolio)
    
    # Display comparison
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown("#### Current Portfolio")
        display_portfolio_metrics(current_metrics, "current")
    
    with col2:
        st.markdown("#### After Trades")
        display_portfolio_metrics(new_metrics, "new")
    
    with col3:
        st.markdown("#### Change")
        display_metric_changes(current_metrics, new_metrics)
    
    # Pending trades table
    st.markdown("### Pending Trades")
    
    trades_df = pd.DataFrame(st.session_state.pending_trades)
    if not trades_df.empty:
        display_df = trades_df[['bond_name', 'action', 'face_amount', 'price', 'proceeds', 'realized_pnl']].copy()
        display_df.columns = ['Bond', 'Action', 'Face Amount', 'Price', 'Proceeds', 'P&L']
        
        # Style the dataframe
        styled_df = display_df.style.format({
            'Face Amount': '${:,.0f}',
            'Price': '{:.3f}',
            'Proceeds': '${:,.0f}',
            'P&L': '${:,.0f}'
        }).applymap(
            lambda x: 'color: #66CC66' if isinstance(x, (int, float)) and x > 0 
            else 'color: #CC3333' if isinstance(x, (int, float)) and x < 0 
            else '', 
            subset=['P&L']
        )
        
        st.dataframe(styled_df, use_container_width=True)
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("❌ Clear All", use_container_width=True):
                st.session_state.pending_trades = []
                st.rerun()
        
        with col2:
            if st.button("💾 Execute All", type="primary", use_container_width=True):
                # Move all pending to executed
                for trade in st.session_state.pending_trades:
                    trade['status'] = 'EXECUTED'
                    trade['execution_time'] = datetime.now()
                    st.session_state.trade_history.append(trade)
                
                st.session_state.pending_trades = []
                st.success("All trades executed successfully!")
                st.balloons()
                st.rerun()
        
        with col3:
            total_pnl = sum(t['realized_pnl'] for t in st.session_state.pending_trades)
            pnl_color = "#66CC66" if total_pnl >= 0 else "#CC3333"
            st.markdown(f"""
            <div style="text-align: center; padding: 0.5rem;">
                <strong>Total P&L:</strong>
                <span style="color: {pnl_color}; font-size: 1.2rem;">
                    ${total_pnl:,.0f}
                </span>
            </div>
            """, unsafe_allow_html=True)
    
    # Visual comparison charts
    st.markdown("### Visual Impact")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # Weight comparison
        fig_weights = create_weight_comparison_chart(portfolio_data, modified_portfolio)
        st.plotly_chart(fig_weights, use_container_width=True)
    
    with chart_col2:
        # Metrics comparison
        fig_metrics = create_metrics_comparison_chart(current_metrics, new_metrics)
        st.plotly_chart(fig_metrics, use_container_width=True)

def show_trade_history():
    """Display historical trades"""
    
    st.markdown("### Trade History")
    
    if not st.session_state.trade_history:
        st.info("No trades executed yet.")
        return
    
    # Convert to dataframe
    history_df = pd.DataFrame(st.session_state.trade_history)
    
    # Summary statistics
    col1, col2, col3, col4 = st.columns(4)
    
    total_trades = len(history_df)
    total_realized_pnl = history_df['realized_pnl'].sum()
    winning_trades = len(history_df[history_df['realized_pnl'] > 0])
    avg_pnl = history_df['realized_pnl'].mean()
    
    with col1:
        st.metric("Total Trades", total_trades)
    
    with col2:
        pnl_color = "#66CC66" if total_realized_pnl >= 0 else "#CC3333"
        st.markdown(f"""
        <div style="text-align: center;">
            <p style="margin: 0; color: #888;">Total Realized P&L</p>
            <p style="margin: 0; color: {pnl_color}; font-size: 1.5rem; font-weight: bold;">
                ${total_realized_pnl:,.0f}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        st.metric("Win Rate", f"{win_rate:.1f}%")
    
    with col4:
        st.metric("Avg P&L", f"${avg_pnl:,.0f}")
    
    # Detailed history table
    st.markdown("### Detailed History")
    
    # Prepare display dataframe
    display_history = history_df[['timestamp', 'bond_name', 'action', 'face_amount', 
                                  'price', 'proceeds', 'realized_pnl', 'notes']].copy()
    display_history['timestamp'] = pd.to_datetime(display_history['timestamp']).dt.strftime('%Y-%m-%d %H:%M')
    display_history.columns = ['Time', 'Bond', 'Action', 'Face Amount', 'Price', 'Proceeds', 'P&L', 'Notes']
    
    # Style the dataframe
    styled_history = display_history.style.format({
        'Face Amount': '${:,.0f}',
        'Price': '{:.3f}',
        'Proceeds': '${:,.0f}',
        'P&L': '${:,.0f}'
    }).applymap(
        lambda x: 'color: #66CC66' if isinstance(x, (int, float)) and x > 0 
        else 'color: #CC3333' if isinstance(x, (int, float)) and x < 0 
        else '', 
        subset=['P&L']
    )
    
    st.dataframe(styled_history, use_container_width=True, height=400)
    
    # Export option
    if st.button("📥 Export Trade History", use_container_width=True):
        csv = history_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"trade_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

def calculate_portfolio_metrics(portfolio_data):
    """Calculate key portfolio metrics"""
    
    non_cash = portfolio_data[portfolio_data['name'] != 'Cash'].copy()
    
    # Ensure numeric types
    non_cash['yield_numeric'] = pd.to_numeric(non_cash['yield'], errors='coerce')
    non_cash['duration_numeric'] = pd.to_numeric(non_cash['duration'], errors='coerce')
    
    total_weight = non_cash['weighting'].sum()
    
    metrics = {
        'total_market_value': portfolio_data['market_value'].sum(),
        'total_holdings': len(non_cash),
        'cash_weight': 100 - total_weight,
        'weighted_yield': (non_cash['yield_numeric'] * non_cash['weighting'] / total_weight).sum() if total_weight > 0 else 0,
        'weighted_duration': (non_cash['duration_numeric'] * non_cash['weighting'] / total_weight).sum() if total_weight > 0 else 0,
        'total_weight': total_weight
    }
    
    return metrics

def apply_pending_trades(portfolio_data):
    """Apply pending trades to portfolio data"""
    
    for trade in st.session_state.pending_trades:
        if trade['action'] == 'SELL':
            # Find the bond
            mask = portfolio_data['name'] == trade['bond_name']
            if mask.any():
                idx = portfolio_data[mask].index[0]
                current_face = portfolio_data.loc[idx, 'face_amount']
                
                # Calculate remaining position
                remaining_face = current_face - trade['face_amount']
                
                if remaining_face <= 0:
                    # Remove the position entirely
                    portfolio_data = portfolio_data.drop(idx)
                else:
                    # Update the position
                    reduction_factor = remaining_face / current_face
                    portfolio_data.loc[idx, 'face_amount'] = remaining_face
                    portfolio_data.loc[idx, 'market_value'] *= reduction_factor
                    portfolio_data.loc[idx, 'total_cost'] *= reduction_factor
                    portfolio_data.loc[idx, 'weighting'] *= reduction_factor
    
    # Recalculate weights to sum to 100
    total_weight = portfolio_data['weighting'].sum()
    if total_weight > 0 and total_weight != 100:
        portfolio_data['weighting'] = portfolio_data['weighting'] * (100 / total_weight)
    
    return portfolio_data

def display_portfolio_metrics(metrics, label):
    """Display portfolio metrics in a formatted way"""
    
    st.markdown(f"""
    <div style="background-color: #2a2a2a; padding: 1rem; border-radius: 8px;">
        <p><strong>Market Value:</strong> ${metrics['total_market_value']:,.0f}</p>
        <p><strong>Holdings:</strong> {metrics['total_holdings']}</p>
        <p><strong>Cash:</strong> {metrics['cash_weight']:.1f}%</p>
        <p><strong>Avg Yield:</strong> {metrics['weighted_yield']:.3f}%</p>
        <p><strong>Avg Duration:</strong> {metrics['weighted_duration']:.2f}</p>
    </div>
    """, unsafe_allow_html=True)

def display_metric_changes(current, new):
    """Display changes in metrics"""
    
    mv_change = new['total_market_value'] - current['total_market_value']
    mv_pct = (mv_change / current['total_market_value'] * 100) if current['total_market_value'] > 0 else 0
    
    holdings_change = new['total_holdings'] - current['total_holdings']
    cash_change = new['cash_weight'] - current['cash_weight']
    yield_change = new['weighted_yield'] - current['weighted_yield']
    duration_change = new['weighted_duration'] - current['weighted_duration']
    
    def format_change(value, suffix="", decimals=0):
        color = "#66CC66" if value > 0 else "#CC3333" if value < 0 else "#888"
        arrow = "↑" if value > 0 else "↓" if value < 0 else "→"
        format_str = f"{{:+.{decimals}f}}"
        return f'<span style="color: {color}">{arrow} {format_str.format(value)}{suffix}</span>'
    
    st.markdown(f"""
    <div style="background-color: #2a2a2a; padding: 1rem; border-radius: 8px;">
        <p><strong>Market Value:</strong> {format_change(mv_pct, '%', 2)}</p>
        <p><strong>Holdings:</strong> {format_change(holdings_change)}</p>
        <p><strong>Cash:</strong> {format_change(cash_change, '%', 1)}</p>
        <p><strong>Avg Yield:</strong> {format_change(yield_change, '%', 3)}</p>
        <p><strong>Avg Duration:</strong> {format_change(duration_change, '', 2)}</p>
    </div>
    """, unsafe_allow_html=True)

def create_weight_comparison_chart(current_portfolio, new_portfolio):
    """Create a chart comparing portfolio weights before and after trades"""
    
    # Get top holdings for comparison
    current_top = current_portfolio.nlargest(10, 'weighting')[['name', 'weighting']]
    current_top.columns = ['Bond', 'Current']
    
    new_top = new_portfolio.nlargest(10, 'weighting')[['name', 'weighting']]
    new_top.columns = ['Bond', 'After Trades']
    
    # Merge the data
    comparison = pd.merge(current_top, new_top, on='Bond', how='outer').fillna(0)
    
    # Create grouped bar chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Current',
        x=comparison['Bond'],
        y=comparison['Current'],
        marker_color='#236192'
    ))
    
    fig.add_trace(go.Bar(
        name='After Trades',
        x=comparison['Bond'],
        y=comparison['After Trades'],
        marker_color='#C8102E'
    ))
    
    fig.update_layout(
        title="Top Holdings Weight Comparison",
        xaxis_title="Bond",
        yaxis_title="Weight (%)",
        barmode='group',
        height=400,
        plot_bgcolor='#1f1f1f',
        paper_bgcolor='#1f1f1f',
        font=dict(color='white'),
        xaxis=dict(tickangle=-45)
    )
    
    return fig

def create_metrics_comparison_chart(current_metrics, new_metrics):
    """Create a radar chart comparing portfolio metrics"""
    
    categories = ['Yield', 'Duration', 'Holdings', 'Diversification']
    
    # Normalize metrics for comparison
    current_values = [
        current_metrics['weighted_yield'],
        current_metrics['weighted_duration'],
        current_metrics['total_holdings'] / 30 * 10,  # Normalize to 0-10 scale
        (100 - current_metrics['cash_weight']) / 10  # Diversification proxy
    ]
    
    new_values = [
        new_metrics['weighted_yield'],
        new_metrics['weighted_duration'],
        new_metrics['total_holdings'] / 30 * 10,
        (100 - new_metrics['cash_weight']) / 10
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=current_values,
        theta=categories,
        fill='toself',
        name='Current',
        line_color='#236192'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=new_values,
        theta=categories,
        fill='toself',
        name='After Trades',
        line_color='#C8102E'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            ),
            bgcolor='#1f1f1f'
        ),
        title="Portfolio Characteristics",
        height=400,
        plot_bgcolor='#1f1f1f',
        paper_bgcolor='#1f1f1f',
        font=dict(color='white'),
        showlegend=True
    )
    
    return fig

# Add custom CSS for the trade calculator
def add_trade_styles():
    st.markdown("""
    <style>
    /* Trade calculator specific styles */
    .trade-card {
        background-color: #2a2a2a;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #C8102E;
    }
    
    .trade-summary {
        background-color: #2a2a2a;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
    
    .pnl-positive {
        color: #66CC66;
        font-weight: bold;
    }
    
    .pnl-negative {
        color: #CC3333;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    st.set_page_config(
        page_title="Trade Calculator - GGI",
        page_icon="💱",
        layout="wide"
    )
    add_trade_styles()
    create_trade_calculator_page()