# xtrillion_guinness_nav.py - Guinness Global Investors Platform with st.navigation

import streamlit as st

st.set_page_config(
    page_title="Guinness Global Investors",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
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
import chatbot_demo

# Define Guinness brand color palette
color_palette = [
    "#E30613",  # Guinness Red (Primary)
    "#002855",  # Guinness Navy Blue
    "#8B0000",  # Dark Red
    "#FF6B6B",  # Light Red
    "#4A5568",  # Charcoal Grey
    "#CBD5E0"   # Light Grey
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
        st.Page(bond_calculator, title="Bond Calculator", icon="🧮", url_path="calculator"),
        st.Page(user_guide, title="User Guide", icon="📖", url_path="guide"),
    ]
}

# Add Guinness branding to sidebar FIRST
with st.sidebar:
    # Get base64 encoded logo
    logo_base64 = get_logo_base64()
    
    if logo_base64:
        # Logo with actual image in circle
        st.markdown(f"""
            <div style="text-align: center; padding: 20px 0;">
                <div style="width: 120px; height: 120px; background-color: #ffffff; 
                            border-radius: 50%; margin: 0 auto; display: flex; 
                            align-items: center; justify-content: center; 
                            box-shadow: 0 4px 6px rgba(0,0,0,0.3); overflow: hidden;">
                    <img src="data:image/png;base64,{logo_base64}" 
                         style="width: 70%; height: auto; object-fit: contain;">
                </div>
                <p style="color: #E30613; font-style: italic; font-size: 14px; margin-top: 10px;">Positively Different</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Fallback to G placeholder
        st.markdown("""
            <div style="text-align: center; padding: 20px 0;">
                <div style="width: 120px; height: 120px; background-color: #ffffff; 
                            border-radius: 50%; margin: 0 auto; display: flex; 
                            align-items: center; justify-content: center; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                    <span style="color: #E30613; font-size: 48px; font-weight: bold;">G</span>
                </div>
                <p style="color: #E30613; font-style: italic; font-size: 14px; margin-top: 10px;">Positively Different</p>
            </div>
        """, unsafe_allow_html=True)

# Create navigation AFTER sidebar content
pg = st.navigation(pages, position="sidebar")

# Add custom CSS
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
        margin-bottom: 1rem;
    }
    
    [data-testid="stSidebarNav"] a {
        color: #ffffff !important;
        background-color: transparent !important;
        border-radius: 4px;
        margin-bottom: 0.25rem;
    }
    
    [data-testid="stSidebarNav"] a:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Selected page styling */
    [data-testid="stSidebarNav"] a[aria-selected="true"] {
        background-color: #E30613 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Run the selected page
pg.run()