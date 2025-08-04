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

# Import necessary modules
from credit_reports import create_country_report_tab
from report_utils import create_fund_report_tab
from user_guide import display_user_guide
from bond_information import create_bond_information_tab
from welcome_page_guinness import display_welcome_page
import chatbot_demo

# Define color palette
color_palette = [
    "#FFA500",  # Bright Orange
    "#007FFF",  # Azure Blue
    "#DC143C",  # Cherry Red
    "#39FF14",  # Electric Lime Green
    "#00FFFF",  # Cyan
    "#DA70D6"   # Vivid Purple
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

# Define navigation pages
pages = {
    "Main": [
        st.Page(welcome_page, title="Welcome", icon="👋"),
        st.Page(ggi_portfolio, title="GGI Portfolio", icon="🌐"),
        st.Page(skewnbf_portfolio, title="SKEWNBF", icon="🟠"),
        st.Page(skesbf_portfolio, title="SKESBF", icon="🟢"),
    ],
    "Country Reports": [
        st.Page(israel_report, title="Israel", icon="🇮🇱"),
        st.Page(qatar_report, title="Qatar", icon="🇶🇦"),
        st.Page(mexico_report, title="Mexico", icon="🇲🇽"),
        st.Page(saudi_arabia_report, title="Saudi Arabia", icon="🇸🇦"),
    ],
    "Tools": [
        st.Page(user_guide, title="User Guide", icon="📖"),
    ]
}

# Create navigation
pg = st.navigation(pages)

# Add custom CSS
st.markdown("""
    <style>
    /* Guinness brand colors */
    .stApp {
        background-color: #1f1f1f;
        color: #ffffff;
    }
    
    /* Navigation styling - darker to match theme */
    [data-testid="stSidebarNav"] {
        background-color: #2a2a2a;
    }
    
    [data-testid="stSidebarNav"] a {
        color: #ffffff !important;
        background-color: #2a2a2a !important;
    }
    
    [data-testid="stSidebarNav"] a:hover {
        background-color: #3a3a3a !important;
    }
    
    /* Selected page styling */
    [data-testid="stSidebarNav"] a[aria-selected="true"] {
        background-color: #E30613 !important;
    }
    
    /* Sidebar background */
    section[data-testid="stSidebar"] {
        background-color: #1a1a1a;
    }
    </style>
    """, unsafe_allow_html=True)

# Add Guinness branding to sidebar
with st.sidebar:
    # Logo
    st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
        """, unsafe_allow_html=True)
    
    # Display the actual Guinness logo
    st.image("guinness_logo.png", width=150)
    
    st.markdown("""
            <p style="color: #E30613; font-style: italic; font-size: 14px; margin-top: 10px;">Positively Different</p>
        </div>
    """, unsafe_allow_html=True)

# Run the selected page
pg.run()