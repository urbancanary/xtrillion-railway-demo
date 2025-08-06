import streamlit as st
import pandas as pd
import sqlite3
import numpy as np
from pathlib import Path

# Page configuration - REMOVED to prevent conflict with main app
# st.set_page_config(
#     page_title="RVM Grid",
#     page_icon="📊",
#     layout="wide"
# )

# Custom CSS for dark theme and visual banding
st.markdown("""
<style>
    /* Dark theme styling to match streamkit app */
    .stApp {
        background-color: #0E1117;
    }
    
    /* Main container */
    .rvm-grid-container {
        background-color: #1E1E1E;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        border: 1px solid #333;
    }
    
    /* Grid table styling */
    .rvm-grid-table {
        width: 100%;
        border-collapse: collapse;
        font-family: 'Courier New', monospace;
        font-size: 11px;
        background-color: #1E1E1E;
        margin: 10px 0;
    }
    
    .rvm-grid-table th {
        background-color: #2D2D2D;
        color: #FFFFFF;
        padding: 8px 6px;
        text-align: center;
        border: 1px solid #555;
        font-weight: bold;
        font-size: 10px;
    }
    
    .rvm-grid-table td {
        padding: 4px 6px;
        text-align: center;
        border: 1px solid #444;
        color: #E0E0E0;
        font-size: 10px;
    }
    
    /* Rating column styling */
    .rating-cell {
        background-color: #2D2D2D !important;
        color: #FFFFFF !important;
        font-weight: bold;
        text-align: left !important;
        padding-left: 12px !important;
        min-width: 60px;
    }
    
    /* Visual banding - alternating row colors */
    .rvm-grid-table tr:nth-child(even) td:not(.rating-cell) {
        background-color: #252525;
    }
    
    .rvm-grid-table tr:nth-child(odd) td:not(.rating-cell) {
        background-color: #1A1A1A;
    }
    
    /* Hover effects */
    .rvm-grid-table tr:hover td:not(.rating-cell) {
        background-color: #333333 !important;
        transition: background-color 0.2s;
    }
    
    /* Spread value color coding */
    .spread-low { color: #4CAF50 !important; }      /* Green for low spreads */
    .spread-medium { color: #FFC107 !important; }   /* Yellow for medium spreads */
    .spread-high { color: #F44336 !important; }     /* Red for high spreads */
    
    /* Header styling */
    .main-header {
        color: #FFFFFF;
        text-align: center;
        font-size: 2.5em;
        margin-bottom: 20px;
        font-weight: 300;
    }
    
    .sub-header {
        color: #CCCCCC;
        text-align: center;
        font-size: 1.1em;
        margin-bottom: 20px;
    }
    
    /* Metrics styling */
    .metric-container {
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #333;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Note: Removed @st.cache_data decorator to avoid issues with exec() context
# @st.cache_data(ttl=300)  # Cache for 5 minutes
def load_rvm_data():
    """Load RVM grid data from database"""
    try:
        # Try multiple database locations
        db_paths = [
            "rvm_data.db",  # Current directory first
            "../rvm_data.db", 
            "/Users/andyseaman/Desktop/bond_agent/rvm_data.db",
            "/Users/andyseaman/Desktop/bond_agent/large_bonds_rvm_data.db",
            "/Users/andyseaman/Notebooks/mcp_xtrillion/rvm_grid_local.db",
            "/Volumes/BOND_AGENT/bond_agent/rvm_data.db",
            "bond_agent/rvm_data.db"
        ]
        
        conn = None
        db_path_used = None
        for db_path in db_paths:
            try:
                if Path(db_path).exists():
                    conn = sqlite3.connect(db_path)
                    db_path_used = db_path
                    break
            except:
                continue
        
        if conn is None:
            st.error("❌ Could not connect to RVM database")
            st.info("💡 Expected database locations: " + ", ".join(db_paths))
            return None, None
            
        # Query rvm_grid_wide table
        try:
            query = "SELECT * FROM rvm_grid_wide ORDER BY rating"
            df = pd.read_sql_query(query, conn)
            conn.close()
            return df, db_path_used
        except Exception:
            # If rvm_grid_wide doesn't exist, try other table names
            conn.close()
            return None, db_path_used
            
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return None, None

def get_spread_class(value):
    """Determine CSS class based on spread value"""
    if pd.isna(value) or value == "" or value is None:
        return ""
    try:
        val = float(value)
        if val < 100:
            return "spread-low"
        elif val < 300:
            return "spread-medium" 
        else:
            return "spread-high"
    except:
        return ""

def format_spread_value(value):
    """Format spread value for display"""
    if pd.isna(value) or value == "" or value is None:
        return "-"
    try:
        val = float(value)
        return f"{val:.0f}"
    except:
        return str(value) if str(value) != "nan" else "-"

def create_rvm_grid_html(df):
    """Create HTML table for RVM grid display"""
    if df is None or df.empty:
        return "<p style='color: #CCCCCC;'>No data available</p>"
    
    # Get column names (excluding 'rating' column)
    duration_cols = [col for col in df.columns if col.lower() != 'rating']
    
    # Sort duration columns logically (1Y, 2Y, 3Y, etc.)
    def sort_duration_key(col):
        import re
        match = re.search(r'(\d+)', str(col))
        if match:
            return int(match.group(1))
        return 999
    
    duration_cols = sorted(duration_cols, key=sort_duration_key)
    
    # Start building HTML table
    html = '<div class="rvm-grid-container">'
    html += '<table class="rvm-grid-table">'
    
    # Header row
    html += '<tr><th>Rating</th>'
    for col in duration_cols:
        html += f'<th>{col}</th>'
    html += '</tr>'
    
    # Data rows
    for idx, row in df.iterrows():
        html += '<tr>'
        
        # Rating cell
        rating = row.get('rating', row.get('Rating', f"Row {idx+1}"))
        html += f'<td class="rating-cell">{rating}</td>'
        
        # Spread cells
        for col in duration_cols:
            value = row.get(col)
            spread_class = get_spread_class(value)
            formatted_value = format_spread_value(value)
            html += f'<td class="{spread_class}">{formatted_value}</td>'
        
        html += '</tr>'
    
    html += '</table></div>'
    return html

def main():
    """Main RVM Grid page"""
    
    # Page header
    st.markdown('<h1 class="main-header">RVM Credit Spread Grid</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Credit Spreads by Rating and Duration (basis points)</p>', unsafe_allow_html=True)
    
    # Load data
    with st.spinner('Loading RVM grid data...'):
        df, db_path = load_rvm_data()
    
    if df is not None and not df.empty:
        # Display basic info
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-container">
                <h3 style="color: #4CAF50; margin: 0;">Total Ratings</h3>
                <p style="color: #FFFFFF; font-size: 1.5em; margin: 5px 0;">{}</p>
            </div>
            """.format(len(df)), unsafe_allow_html=True)
            
        with col2:
            duration_count = len([col for col in df.columns if col.lower() != 'rating'])
            st.markdown("""
            <div class="metric-container">
                <h3 style="color: #2196F3; margin: 0;">Duration Points</h3>
                <p style="color: #FFFFFF; font-size: 1.5em; margin: 5px 0;">{}</p>
            </div>
            """.format(duration_count), unsafe_allow_html=True)
            
        with col3:
            # Calculate average spread (excluding rating column)
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                avg_spread = df[numeric_cols].mean().mean()
                color = "#4CAF50" if avg_spread < 200 else "#FFC107" if avg_spread < 400 else "#F44336"
                st.markdown("""
                <div class="metric-container">
                    <h3 style="color: {}; margin: 0;">Avg Spread</h3>
                    <p style="color: #FFFFFF; font-size: 1.5em; margin: 5px 0;">{:.0f} bps</p>
                </div>
                """.format(color, avg_spread), unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="metric-container">
                    <h3 style="color: #666; margin: 0;">Avg Spread</h3>
                    <p style="color: #FFFFFF; font-size: 1.5em; margin: 5px 0;">N/A</p>
                </div>
                """, unsafe_allow_html=True)
                
        with col4:
            st.markdown("""
            <div class="metric-container">
                <h3 style="color: #9C27B0; margin: 0;">Data Source</h3>
                <p style="color: #FFFFFF; font-size: 0.9em; margin: 5px 0;">RVM Database</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Display the grid
        grid_html = create_rvm_grid_html(df)
        st.markdown(grid_html, unsafe_allow_html=True)
        
        # Data info
        st.markdown("---")
        with st.expander("📊 Data Information & Legend"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🎨 Spread Color Coding:**")
                st.markdown("🟢 **Low Risk**: < 100 bps")
                st.markdown("🟡 **Medium Risk**: 100-300 bps") 
                st.markdown("🔴 **High Risk**: > 300 bps")
                
            with col2:
                st.markdown("**📈 Data Details:**")
                st.markdown(f"**Shape**: {df.shape[0]} ratings × {df.shape[1]-1} durations")
                st.markdown(f"**Database**: `{Path(db_path).name if db_path else 'Unknown'}`")
                st.markdown("**Last Updated**: Real-time")
                
    else:
        st.error("❌ Unable to load RVM grid data")
        
        st.markdown("### 🔧 Troubleshooting")
        st.info("""
        **Expected database locations:**
        - `/Users/andyseaman/Desktop/bond_agent/rvm_data.db`
        - `/Users/andyseaman/Desktop/bond_agent/large_bonds_rvm_data.db`
        - Current directory: `rvm_data.db`
        
        **Expected table:** `rvm_grid_wide` with rating column + duration columns
        """)

# Run the main function directly (no need for __name__ check when using exec)
main()
