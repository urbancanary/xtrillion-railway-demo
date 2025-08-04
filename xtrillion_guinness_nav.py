# xtrillion_guinness_nav.py - Guinness Global Investors Platform with st.navigation

import streamlit as st

# Check if we should start with sidebar collapsed
initial_state = "collapsed" if 'sidebar_state' not in st.session_state else st.session_state.get('sidebar_state', 'expanded')

st.set_page_config(
    page_title="Guinness Global Investors",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state=initial_state,
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "Guinness Global Investors - Portfolio Management Platform"
    }
)

# Initialize session state to prevent errors
if "state" not in st.session_state:
    st.session_state.state = {
        "current_report": "👋 Welcome",
        "time_selection": "Latest",
        "mode": "auto"
    }

# Import necessary modules
from credit_reports import create_country_report_tab
from report_utils import create_fund_report_tab
from user_guide import display_user_guide
from bond_information import create_bond_information_tab
from welcome_page_guinness_nav import display_welcome_page
from logo_utils import get_logo_base64
from bond_calculator_mockup import create_bond_calculator_page, add_custom_styles
from portfolio_valuation import create_portfolio_valuation_page, add_valuation_styles
from trade_calculator import create_trade_calculator_page, add_trade_styles
import chatbot_demo

# Official Guinness brand color palette
color_palette = [
    "#C8102E",  # Pantone 186 C - Primary Red
    "#21315C",  # Pantone 534 C - Secondary Primary Dark Blue
    "#236192",  # Pantone 647 C - Secondary Blue
    "#9DB9D5",  # Pantone 644 C - Secondary Light Blue
    "#6BBBAE",  # Pantone 536 C - Secondary Teal
    "#D6D2C4",  # Pantone 7527 C - Secondary Beige
    "#808285",  # Black 60% - Grey
]

# Page functions
def welcome_page():
    display_welcome_page()

def ggi_portfolio():
    create_fund_report_tab(
        "GGI Wealthy Nations Bond Fund",
        color_palette,
        "Latest"
    )

def skewnbf_portfolio():
    create_fund_report_tab(
        "Shin Kong Emerging Wealthy Nations Bond Fund",
        color_palette,
        "Latest"
    )

def skesbf_portfolio():
    create_fund_report_tab(
        "Shin Kong Environmental Sustainability Bond Fund",
        color_palette,
        "Latest"
    )

def israel_report():
    create_country_report_tab("Israel", color_palette)

def qatar_report():
    create_country_report_tab("Qatar", color_palette)

def mexico_report():
    create_country_report_tab("Mexico", color_palette)

def saudi_arabia_report():
    create_country_report_tab("Saudi Arabia", color_palette)

def bond_info():
    create_bond_information_tab()

def user_guide():
    display_user_guide()

def chatbot():
    st.title("Xtrillion Chatbot")
    st.write("Welcome to the Xtrillion Chatbot! Ask me anything about our reports and data.")
    chatbot_demo.main()

def bond_calculator():
    add_custom_styles()
    create_bond_calculator_page()

def portfolio_valuation():
    add_valuation_styles()
    create_portfolio_valuation_page()

def trade_calculator():
    add_trade_styles()
    create_trade_calculator_page()

# Define navigation pages with correct path handling
pages = {
    "Main": [
        st.Page(welcome_page, title="Welcome", icon="👋", url_path="welcome"),
        st.Page(ggi_portfolio, title="GGI Portfolio", icon="🌐", url_path="ggi"),
        st.Page(skewnbf_portfolio, title="SKEWNBF", icon="🟠", url_path="skewnbf"),
        st.Page(skesbf_portfolio, title="SKESBF", icon="🟢", url_path="skesbf"),
    ],
    "Country Reports": [
        st.Page(israel_report, title="Israel", icon="🇮🇱", url_path="israel"),
        st.Page(qatar_report, title="Qatar", icon="🇶🇦", url_path="qatar"),
        st.Page(mexico_report, title="Mexico", icon="🇲🇽", url_path="mexico"),
        st.Page(saudi_arabia_report, title="Saudi Arabia", icon="🇸🇦", url_path="saudi-arabia"),
    ],
    "Tools": [
        st.Page(portfolio_valuation, title="Portfolio Valuation", icon="💰", url_path="valuation"),
        st.Page(trade_calculator, title="Trade Calculator", icon="💱", url_path="trades"),
        st.Page(bond_calculator, title="Bond Calculator", icon="🧮", url_path="calculator"),
        st.Page(user_guide, title="User Guide", icon="📖", url_path="guide"),
    ]
}

# Add logo to sidebar FIRST
with st.sidebar:
    logo_base64 = get_logo_base64()
    if logo_base64:
        st.markdown(f"""
            <div style="text-align: center; padding: 1rem 0 2rem 0;">
                <div style="width: 80px; height: 80px; background-color: #ffffff; 
                            border-radius: 50%; margin: 0 auto; display: flex; 
                            align-items: center; justify-content: center; 
                            box-shadow: 0 4px 6px rgba(0,0,0,0.3); overflow: hidden;">
                    <img src="data:image/png;base64,{logo_base64}" 
                         style="width: 70%; height: auto; object-fit: contain;">
                </div>
                <p style="color: #C8102E; font-style: italic; font-size: 14px; margin-top: 10px; margin-bottom: 0;">
                    Positively Different
                </p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="text-align: center; padding: 1rem 0 2rem 0;">
                <div style="width: 80px; height: 80px; background-color: #ffffff; 
                            border-radius: 50%; margin: 0 auto; display: flex; 
                            align-items: center; justify-content: center; 
                            box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                    <span style="color: #C8102E; font-size: 36px; font-weight: bold;">G</span>
                </div>
                <p style="color: #C8102E; font-style: italic; font-size: 14px; margin-top: 10px; margin-bottom: 0;">
                    Positively Different
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    # Add a separator
    st.markdown("---")

# Check if we need to navigate to a specific page
if 'navigate_to' in st.session_state:
    # Map navigation targets to page functions
    nav_map = {
        'ggi': ggi_portfolio,
        'skewnbf': skewnbf_portfolio,
        'skesbf': skesbf_portfolio,
        'israel': israel_report,
        'qatar': qatar_report,
        'mexico': mexico_report,
        'saudi-arabia': saudi_arabia_report,
        'calculator': bond_calculator,
        'valuation': portfolio_valuation
    }
    
    # Get the target page function
    target = st.session_state.navigate_to
    if target in nav_map:
        # Clear the navigation flag
        del st.session_state.navigate_to
        # Set the default page
        default_page = nav_map[target]
    else:
        default_page = welcome_page
else:
    default_page = welcome_page

# Create navigation with optional default
pg = st.navigation(pages, position="sidebar")

st.markdown("""
    <style>
    /* Guinness brand colors */
    .stApp {
        background-color: #1f1f1f;
        color: #ffffff;
    }
    
    /* Sidebar background - match navigation background */
    section[data-testid="stSidebar"] {
        background-color: #2a2a2a !important;
    }
    
    section[data-testid="stSidebar"] > div {
        background-color: #2a2a2a !important;
    }
    
    /* Navigation styling - same color as sidebar */
    [data-testid="stSidebarNav"] {
        background-color: #2a2a2a;
        border-radius: 8px;
        padding: 0.5rem;
        margin-top: 0;
    }
    
    [data-testid="stSidebarNav"] a {
        color: #ffffff !important;
        background-color: transparent !important;
        border-radius: 4px;
        margin-bottom: 0.25rem;
        transition: all 0.2s ease;
    }
    
    [data-testid="stSidebarNav"] a:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
        transform: translateX(5px);
    }
    
    /* Selected page styling */
    [data-testid="stSidebarNav"] a[aria-selected="true"] {
        background-color: #C8102E !important;
        font-weight: bold;
    }
    
    /* Ensure navigation sections have proper spacing */
    [data-testid="stSidebarNav"] > ul > li {
        margin-bottom: 1rem;
    }
    
    /* Section headers styling */
    [data-testid="stSidebarNav"] > ul > li > span {
        color: #888;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    </style>
    """, unsafe_allow_html=True)

# Run the selected page
pg.run()