import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
import plotly.graph_objects as go
import colorsys
from io import StringIO
import json
from fetch_data import fetch_fund_data  # Import the function from fetch_data.py
from datetime import datetime

# Financial term tooltips
FINANCIAL_TERMS = {
    "YTM": "Yield to Maturity - The total expected return if a bond is held until maturity",
    "Duration": "A measure of a bond's price sensitivity to interest rate changes",
    "ESG": "Environmental, Social, and Governance rating",
    "NFA": "National Financial Authority rating",
    "Spread": "The difference between the bond yield and a benchmark rate",
    "Accrued Interest": "Interest earned but not yet paid since the last coupon payment"
}

def add_tooltip(term, definition):
    """Add a tooltip icon next to a term"""
    return f'{term} <span title="{definition}" style="cursor: help; color: #888;">ⓘ</span>'

# Guinness brand color palette
color_palette = [
    "#E30613",  # Guinness Red (Primary)
    "#002855",  # Guinness Navy Blue
    "#8B0000",  # Dark Red
    "#FF6B6B",  # Light Red
    "#4A5568",  # Charcoal Grey
    "#CBD5E0"   # Light Grey
]

# Apply custom CSS for consistent styling across the app
def apply_custom_css():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #1f1f1f;
        }
        .reportColumn, .chartColumn {
            background-color: #1f1f1f;
            color: #f5f5f5;
        }
        .reportColumn h3, .reportColumn p, .reportColumn th, .reportColumn td {
            color: #f5f5f5;
        }
        .data-table th {
            color: white;
            background-color: #000000;  /* Black background for table header */
        }
        .data-table td {
            color: #1f1f1f;
            background-color: #f5f5f5;
        }
        /* Print-friendly styles */
        @media print {
            .stApp {
                background-color: white !important;
                color: black !important;
            }
            .reportColumn, .chartColumn {
                background-color: white !important;
                color: black !important;
            }
            .data-table th {
                background-color: #f0f0f0 !important;
                color: black !important;
            }
            .stButton, .stDownloadButton {
                display: none !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def fetch_country_data(entity_name, db_name="credit_research.db", table_name="FullReport"):
    url = "https://my-combined-app-44056503414.us-central1.run.app/process_json"
    payload = {
        "sample_key": f'{{"db_path": "{db_name}", "table": "{table_name}", "filters": {{"Country": "{entity_name}"}}, "fields": "*", "page": 1, "page_size": 100}}'
    }
    st.session_state.state["payload"] = json.dumps(payload, indent=2)
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        st.session_state.state["api_response"] = json.dumps(data, indent=2)
        return data
    else:
        st.session_state.state["api_response"] = f"Error: {response.status_code}"
        return None
    
# Function to fetch country data from the API and create a country report tab

def create_country_report_tab(entity_name, color_palette, db_name="credit_research.db", table_name="FullReport"):
    apply_custom_css()
    st.write(f"### {entity_name} Report")
    
    with st.spinner(f'Loading {entity_name} country report...'):
        data = fetch_country_data(entity_name, db_name, table_name)
    
    if data and len(data) > 0:
        report = data[0]

        col1, col2 = st.columns([6, 4])

        with col1:
            st.markdown('<div class="reportColumn">', unsafe_allow_html=True)
            st.markdown(f'<h1 class="reportText">{report.get("Title", "Credit Research Report")}</h1>', unsafe_allow_html=True)
            st.markdown('<h2 class="reportText">Country Information</h2>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText"><strong>Country:</strong> {report.get("Country", "N/A")}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText"><strong>Ownership:</strong> {report.get("Ownership", "N/A")}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText"><strong>NFA Rating:</strong> {report.get("NFARating", "N/A")}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText"><strong>ESG Rating:</strong> {report.get("ESGRating", "N/A")}</p>', unsafe_allow_html=True)
            st.markdown('<h2 class="reportText">Overview</h2>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText">{report.get("Overview", "No overview available.")}</p>', unsafe_allow_html=True)
            st.markdown('<h2 class="reportText">Politics</h2>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText">{report.get("PoliticalNews", "No political news available.")}</p>', unsafe_allow_html=True)
            st.markdown('<h2 class="reportText">Strengths</h2>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText">{report.get("Strengths", "No strengths information available.")}</p>', unsafe_allow_html=True)
            st.markdown('<h2 class="reportText">Weaknesses</h2>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText">{report.get("Weaknesses", "No weaknesses information available.")}</p>', unsafe_allow_html=True)
            st.markdown('<h2 class="reportText">Opportunities</h2>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText">{report.get("Opportunities", "No opportunities information available.")}</p>', unsafe_allow_html=True)
            st.markdown('<h2 class="reportText">Threats</h2>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText">{report.get("Threats", "No threats information available.")}</p>', unsafe_allow_html=True)
            st.markdown('<h2 class="reportText">Recent News</h2>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText">{report.get("RecentNews", "No recent news available.")}</p>', unsafe_allow_html=True)
            st.markdown('<h2 class="reportText">Ratings and Comments from Credit Rating Agencies</h2>', unsafe_allow_html=True)
            st.markdown('<h3 class="reportText">Moody\'s:</h3>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText">{report.get("MoodysRating", "N/A")}</p>', unsafe_allow_html=True)
            st.markdown('<h3 class="reportText">S&P Global Ratings:</h3>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText">{report.get("SPGlobalRating", "N/A")}</p>', unsafe_allow_html=True)
            st.markdown('<h3 class="reportText">Fitch Ratings:</h3>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText">{report.get("FitchRating", "N/A")}</p>', unsafe_allow_html=True)
            st.markdown('<h2 class="reportText">Conclusion</h2>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText">{report.get("Conclusion", "No conclusion available.")}</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="chartColumn">', unsafe_allow_html=True)
            st.header("Economic Data (2024 Onwards)")

            charts_data = [
                ("GDP Growth (%)", [report.get(f'GDPGrowthRateYear{i}', 0) for i in range(1, 7)], color_palette[0]),
                ("Inflation Rate (%)", [report.get(f'InflationYear{i}', 0) for i in range(1, 7)], color_palette[1]),
                ("Unemployment Rate (%)", [report.get(f'UnemploymentRateYear{i}', 0) for i in range(1, 7)], color_palette[2]),
                ("Population (millions)", [report.get(f'PopulationYear{i}', 0) for i in range(1, 7)], color_palette[3]),
                ("Government Budget Balance (% of GDP)", [report.get(f'GovernmentFinancesYear{i}', 0) for i in range(1, 7)], color_palette[4]),
                ("Current Account Balance (% of GDP)", [report.get(f'CurrentAccountBalanceYear{i}', 0) for i in range(1, 7)], color_palette[5])
            ]

            years = [2024, 2025, 2026, 2027, 2028, 2029]

            for metric, values, color in charts_data:
                df = pd.DataFrame({
                    "Year": years,
                    metric: values
                })

                st.plotly_chart(plot_chart(df, metric, metric, color), use_container_width=True)
                st.markdown(create_data_table(df, metric), unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error(f"No data found for {entity_name}.")

def filter_dataframe(df: pd.DataFrame, identifier: str = "", filter_columns: list = None) -> pd.DataFrame:
    if filter_columns is None:
        filter_columns = []

    filtered_df = df.copy()

    for idx, col in enumerate(filter_columns):
        if col not in df.columns:
            continue

        unique_values = sorted(df[col].dropna().astype(str).unique())

        if pd.api.types.is_numeric_dtype(df[col]):
            numeric_values = df[col].dropna()
            default_value = [float(numeric_values.min()), float(numeric_values.max())]
            selected_values = st.slider(
                f"Filter {col} ({identifier})",
                min_value=default_value[0],
                max_value=default_value[1],
                value=default_value,
                step=(default_value[1] - default_value[0]) / 100,
                key=f"filter_{col}_{identifier}_{idx}"
            )
            filtered_df = filtered_df[
                (filtered_df[col] >= selected_values[0]) &
                (filtered_df[col] <= selected_values[1])
            ]
        else:
            selected_values = st.multiselect(
                f"Filter {col} ({identifier})",
                options=unique_values,
                default=unique_values,
                key=f"filter_{col}_{identifier}_{idx}"
            )
            filtered_df = filtered_df[filtered_df[col].astype(str).isin(selected_values)]

    return filtered_df

def create_pie_chart(data, names, values, title, legend_position='right'):
    colors = color_palette[:len(data[names].unique())]
    
    fig = go.Figure(data=[go.Pie(
        labels=data[names],
        values=data[values],
        hole=0.4,
        marker=dict(colors=colors),
        textposition='outside',
        textinfo='value+label',
        texttemplate='%{value:.1f}<br>%{label}',
        hovertemplate='%{label}<br>Value: %{value:.2f}<extra></extra>',  # Add <extra></extra>
    )])
    
    fig.update_traces(
        textfont=dict(color='white', size=12),
        outsidetextfont=dict(color='white', size=12),
    )
    
    legend_x = 0.01 if legend_position == 'left' else 1.02
    legend_y = 1.1
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=20)
        ),
        paper_bgcolor='#1f1f1f',
        plot_bgcolor='#1f1f1f',
        font=dict(color='white', size=16),
        height=500,
        width=None,  # Will be set by container
        transition_duration=500,
        legend=dict(
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(0,0,0,0)',
            font=dict(color='white', size=14),
            x=legend_x,
            y=legend_y,
            xanchor='left',
            yanchor='top'
        ),
        showlegend=True,
    )
    return fig

def create_portfolio_summary_cards(fund_data):
    """Create summary metric cards for the portfolio"""
    # Calculate metrics
    total_holdings = len(fund_data[fund_data['name'] != 'Cash'])
    total_weight = fund_data['weighting'].sum()  # Include Cash in total weight to show 100%
    
    # Calculate average yield and duration (excluding Cash and NaN values)
    non_cash_data = fund_data[fund_data['name'] != 'Cash'].copy()
    avg_yield = non_cash_data['yield'].replace('Cash', np.nan).astype(float).mean()
    avg_duration = non_cash_data['duration'].replace('Cash', np.nan).astype(float).mean()
    
    # Create four columns for the metric cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="background-color: #2a2a2a; padding: 1.5rem; border-radius: 10px; text-align: center; border-left: 4px solid #E30613;">
            <h4 style="color: #E30613; margin: 0; font-size: 0.9rem;">HOLDINGS</h4>
            <h2 style="color: white; margin: 0.5rem 0; font-size: 2rem;">{}</h2>
            <p style="color: #888; margin: 0; font-size: 0.8rem;">Securities</p>
        </div>
        """.format(total_holdings), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: #2a2a2a; padding: 1.5rem; border-radius: 10px; text-align: center; border-left: 4px solid #002855;">
            <h4 style="color: #002855; margin: 0; font-size: 0.9rem;">PORTFOLIO WEIGHT</h4>
            <h2 style="color: white; margin: 0.5rem 0; font-size: 2rem;">{:.1f}%</h2>
            <p style="color: #888; margin: 0; font-size: 0.8rem;">Allocated</p>
        </div>
        """.format(total_weight), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background-color: #2a2a2a; padding: 1.5rem; border-radius: 10px; text-align: center; border-left: 4px solid #8B0000;">
            <h4 style="color: #8B0000; margin: 0; font-size: 0.9rem;">AVG YIELD</h4>
            <h2 style="color: white; margin: 0.5rem 0; font-size: 2rem;">{:.2f}%</h2>
            <p style="color: #888; margin: 0; font-size: 0.8rem;" title="Yield to Maturity - The total expected return if held until maturity">YTM ⓘ</p>
        </div>
        """.format(avg_yield if not np.isnan(avg_yield) else 0), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background-color: #2a2a2a; padding: 1.5rem; border-radius: 10px; text-align: center; border-left: 4px solid #4A5568;">
            <h4 style="color: #4A5568; margin: 0; font-size: 0.9rem;">AVG DURATION</h4>
            <h2 style="color: white; margin: 0.5rem 0; font-size: 2rem;">{:.1f}</h2>
            <p style="color: #888; margin: 0; font-size: 0.8rem;" title="A measure of bond price sensitivity to interest rate changes">Years ⓘ</p>
        </div>
        """.format(avg_duration if not np.isnan(avg_duration) else 0), unsafe_allow_html=True)
    
    # Add spacing after cards
    st.markdown("<br>", unsafe_allow_html=True)

def create_pie_charts_and_table(fund_data):
    if fund_data is not None:
        # Add loading indicator
        with st.spinner('Loading portfolio analytics...'):
            # Convert 'weighting' to numeric, replacing any non-numeric values with NaN
            fund_data['weighting'] = pd.to_numeric(fund_data['weighting'], errors='coerce')
        
        # Remove any rows where 'weighting' is NaN
        fund_data = fund_data.dropna(subset=['weighting'])
        
        # Calculate total weight
        total_weight = fund_data['weighting'].sum()
        
        # If total weight is less than 100, add a Cash row
        if total_weight < 100:
            cash_weight = 100 - total_weight
            cash_row = pd.DataFrame({
                'name': ['Cash'],
                'weighting': [cash_weight],
                'yield': ['Cash'],
                'duration': ['Cash'],
                'region': ['Cash'],
                'nfa_star_rating': ['Cash'] if 'nfa_star_rating' in fund_data.columns else None,
                'nfa': ['Cash'] if 'nfa' in fund_data.columns else None,
                'esg': ['Cash'] if 'esg' in fund_data.columns else None,
                'esg_country_star_rating': ['Cash'] if 'esg_country_star_rating' in fund_data.columns else None
            })
            # Remove None columns
            cash_row = cash_row.dropna(axis=1)
            # Add all other columns from fund_data with 'Cash' as value
            for col in fund_data.columns:
                if col not in cash_row.columns:
                    cash_row[col] = 'Cash'
            
            # Append cash row to fund_data
            fund_data = pd.concat([fund_data, cash_row], ignore_index=True)
        
        # Check if 'nfa_star_rating' column exists
        nfa_column = next((col for col in ['nfa_star_rating', 'nfa'] if col in fund_data.columns), None)
        if nfa_column:
            # Add "Cash" for missing NFA ratings
            fund_data[nfa_column] = fund_data[nfa_column].fillna('Cash')
            fig_nfa = create_pie_chart(fund_data, nfa_column, 'weighting', "NFA Star Rating Distribution", legend_position='right')
            fig_nfa.update_traces(
                hoverinfo="label+percent", 
                textinfo='percent', 
                textfont=dict(size=12),
                hovertemplate='<b>%{label}</b><br>Weight: %{percent}<br><i>NFA: National Financial Authority rating</i><br>Higher stars indicate stronger financial fundamentals<extra></extra>'
            )
        else:
            st.warning("NFA Star Rating data not available.")

        # Check if 'esg' column exists
        esg_column = next((col for col in ['esg', 'esg_country_star_rating'] if col in fund_data.columns), None)
        if esg_column:
            # Add "Cash" for missing ESG ratings
            fund_data[esg_column] = fund_data[esg_column].fillna('Cash')

            # Convert 'esg' ratings to numeric where possible, and keep non-numeric as is
            fund_data['esg_numeric'] = pd.to_numeric(fund_data[esg_column], errors='coerce')

            # Create the ESG pie chart using the esg column and set hover and label settings
            fig_esg = create_pie_chart(fund_data, esg_column, 'weighting', "ESG Rating Distribution", legend_position='right')
            fig_esg.update_traces(
                hoverinfo="label+percent", 
                textinfo='percent', 
                textfont=dict(size=12), 
                rotation=90,
                hovertemplate='<b>%{label}</b><br>Weight: %{percent}<br><i>ESG: Environmental, Social & Governance rating</i><br>Higher ratings indicate better sustainability practices<extra></extra>'
            )
        else:
            st.warning("ESG Rating data not available.")

        # Create a new column to categorize ESG ratings into 'ESG >= 6' or 'ESG < 6 or Cash'
        if esg_column:
            fund_data['esg_6_or_more'] = fund_data['esg_numeric'].apply(
                lambda x: 'ESG >= 6' if pd.notna(x) and x >= 6 else 'ESG < 6 or Cash'
            )

            # Create the pie chart for ESG ratings with a rating of 6 or more and set hover and label settings
            fig_esg_6 = create_pie_chart(fund_data, 'esg_6_or_more', 'weighting', "ESG Ratings 6 or More", legend_position='right')
            fig_esg_6.update_traces(hoverinfo="label+percent", textinfo='percent', textfont=dict(size=12), rotation=90)
        
        # Check if 'region' column exists
        if 'region' in fund_data.columns:
            # Create a Region pie chart and set hover and label settings
            fig_region = create_pie_chart(fund_data, 'region', 'weighting', "Region Distribution", legend_position='right')
            fig_region.update_traces(hoverinfo="label+percent", textinfo='percent', textfont=dict(size=12), rotation=90)
        else:
            st.warning("Region data not available.")
        
        # Create tabs for better chart display
        chart_tabs = []
        chart_contents = []
        
        if 'region' in fund_data.columns:
            chart_tabs.append("🌍 Region Distribution")
            chart_contents.append(("region", fig_region))
        
        if nfa_column:
            chart_tabs.append("⭐ NFA Star Rating")
            chart_contents.append(("nfa", fig_nfa))
        
        if esg_column:
            chart_tabs.append("🌱 ESG Rating")
            chart_contents.append(("esg", fig_esg))
            chart_tabs.append("📊 ESG 6+ Analysis")
            chart_contents.append(("esg6", fig_esg_6))
        
        if chart_tabs:
            tabs = st.tabs(chart_tabs)
            
            for i, (tab, (chart_type, fig)) in enumerate(zip(tabs, chart_contents)):
                with tab:
                    # Update figure size for better display in tabs
                    fig.update_layout(
                        height=550,
                        width=None,  # Use full width
                        margin=dict(l=20, r=20, t=40, b=20)
                    )
                    
                    # Create columns for chart and export button
                    chart_col, export_col = st.columns([5, 1])
                    with chart_col:
                        st.plotly_chart(fig, use_container_width=True, key=f"chart_{i}")
                    with export_col:
                        # Add export button
                        if st.download_button(
                            label="📥 Export",
                            data=fig.to_html(include_plotlyjs='cdn'),
                            file_name=f"{chart_type}_chart.html",
                            mime="text/html",
                            key=f"export_{i}"
                        ):
                            st.success("Chart exported successfully!", icon="✅")
        
        # Add summary cards after charts
        create_portfolio_summary_cards(fund_data)

        # Apply the filters to the table data
        filtered_data = filter_dataframe(fund_data)
        
        # Add search functionality
        search_col1, search_col2 = st.columns([2, 3])
        with search_col1:
            search_term = st.text_input("🔍 Search holdings", placeholder="Type to search...", key="search_holdings")
        
        # Apply search filter if term is entered
        if search_term:
            # Search across multiple columns
            mask = filtered_data.apply(lambda row: row.astype(str).str.contains(search_term, case=False, na=False).any(), axis=1)
            filtered_data = filtered_data[mask]
            if len(filtered_data) == 0:
                st.warning(f"No results found for '{search_term}'")
        
        # Holdings Data Section with export button
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("### 📋 Holdings Data")
        with col2:
            # Export to CSV button
            csv = convert_df_to_csv(filtered_data)
            st.download_button(
                label="📊 Export CSV",
                data=csv,
                file_name=f"portfolio_holdings_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="export_csv"
            )
        st.markdown("---")

        # Style the DataFrame using Styler with hover effects
        styled_df = filtered_data.style.map(lambda _: 'color: white') \
            .set_table_styles([
                {'selector': 'th', 'props': [
                    ('background-color', '#2f2f2f'),  # Header color
                    ('color', 'white'),
                    ('font-weight', 'bold'),
                    ('padding', '10px'),
                    ('text-align', 'left'),
                    ('position', 'sticky'),
                    ('top', '0'),
                    ('z-index', '10')
                ]},
                {'selector': 'td', 'props': [
                    ('padding', '10px'), 
                    ('color', 'white'), 
                    ('white-space', 'nowrap'),  # Ensure text doesn't wrap
                    ('overflow', 'hidden'), 
                    ('text-overflow', 'ellipsis'),  # Handle overflow with ellipsis if needed
                    ('text-align', 'left'),
                    ('background-color', '#1e1e1e'),
                    ('max-width', '300px'),
                    ('transition', 'background-color 0.2s ease')
                ]},
                {'selector': '.row_heading, .col_heading', 'props': [
                    ('background-color', '#1e1e1e'),  # Row header color
                    ('color', 'white')
                ]},
                {'selector': 'tbody tr:nth-child(even)', 'props': [
                    ('background-color', '#252525')  # Even row background color
                ]},
                {'selector': 'tbody tr:hover', 'props': [
                    ('background-color', '#3a3a3a !important'),  # Hover color
                    ('cursor', 'pointer')
                ]},
                {'selector': 'tbody tr:hover td', 'props': [
                    ('background-color', '#3a3a3a !important')  # Ensure all cells in row highlight
                ]}
            ])

        # Display the styled dataframe
        st.dataframe(styled_df, use_container_width=True, height=600)
        
        # Add help text for table columns
        with st.expander("📖 Column Definitions", expanded=False):
            st.markdown("""
            **Financial Terms Guide:**
            - **Yield (YTM)**: Yield to Maturity - The total expected return if a bond is held until maturity
            - **Duration**: A measure of a bond's price sensitivity to interest rate changes (in years)
            - **Spread**: The difference between the bond yield and a benchmark rate (in basis points)
            - **Accrued Interest**: Interest earned but not yet paid since the last coupon payment
            - **ESG Rating**: Environmental, Social, and Governance score (higher is better)
            - **NFA Rating**: National Financial Authority rating (more stars indicate stronger fundamentals)
            - **Weighting**: Percentage of the portfolio allocated to this holding
            """)

    else:
        st.error("No fund data available to display.")

def convert_df_to_csv(df):
    # Convert dataframe to CSV
    return df.to_csv(index=False).encode('utf-8')

@st.cache_data(show_spinner=True, ttl=3600)
def _fetch_fund_data_cached(fund_name, time_selection):
    """
    Cached wrapper for fetch_fund_data() to cache data in Streamlit.
    """
    return fetch_fund_data(fund_name, time_selection)

def fetch_fund_data_with_cache(fund_name, time_selection):
    """
    Fetches fund data with Streamlit caching.
    """
    return _fetch_fund_data_cached(fund_name, time_selection)
    
def create_fund_report_tab(fund_name, color_palette, time_selection="Latest"):
    apply_custom_css()
    # Avoid redundant "Fund" in title
    if "Fund" in fund_name:
        st.markdown(f"<h3 style='margin-top: 0; padding-top: 0;'>{fund_name} Report ({time_selection})</h3>", unsafe_allow_html=True)
    else:
        st.markdown(f"<h3 style='margin-top: 0; padding-top: 0;'>{fund_name} Fund Report ({time_selection})</h3>", unsafe_allow_html=True)
    
    # Special handling for GGI Wealthy Nations Bond Fund - use local data
    if fund_name == "GGI Wealthy Nations Bond Fund":
        try:
            # Load local data
            fund_data = pd.read_csv('data.csv')
            # Filter for GGI fund only (still uses old name in data)
            fund_data = fund_data[fund_data['fund_name'] == 'Guinness Global Investors Fund']
            
            if not fund_data.empty:
                # Pass all data including any existing Cash row
                create_pie_charts_and_table(fund_data)
            else:
                st.error(f"No data found for {fund_name} in local data.")
        except Exception as e:
            st.error(f"Error loading local data for {fund_name}: {str(e)}")
    else:
        # Use API for other funds
        fund_data = fetch_fund_data(fund_name, time_selection)
        
        if fund_data is not None and not fund_data.empty:
            create_pie_charts_and_table(fund_data)
        else:
            st.error(f"No data found for {fund_name}.")

# Function to plot charts (for both country and fund reports)
def plot_chart(df, y_column, title, color):
    fig = px.bar(df, x='Year', y=y_column,
                 title=title,
                 color_discrete_sequence=[color],
                 height=375)
    fig.update_layout(
        plot_bgcolor='#1f1f1f', 
        paper_bgcolor='#1f1f1f',
        font=dict(color='white'),
        margin=dict(l=20, r=20, t=60, b=40)
    )
    return fig

# Function to create data tables
def create_data_table(df, y_column):
    table_html = "<table class='data-table'>"
    table_html += "<tr><th style='width: 80px;'>Year</th>" + "".join([f"<th>{year}</th>" for year in df['Year']]) + "</tr>"
    table_html += f"<tr><td>{y_column}</td>"
    for value in df[y_column]:
        if value is not None:
            table_html += f"<td>{value:.2f}</td>"  # Format as a float with 2 decimal places
        else:
            table_html += "<td>N/A</td>"  # Use "N/A" for None values
    table_html += "</tr></table>"
    return table_html

# The code is now organized into separate functions, and duplications have been removed.
# You can call create_country_report_tab() or create_fund_report_tab() in your main app to generate the reports.
