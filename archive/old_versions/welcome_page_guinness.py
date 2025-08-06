"""
Guinness Global Investors - Welcome Page
"""
import streamlit as st
from pathlib import Path

def display_welcome_page():
    """Display the Guinness-branded welcome page"""
    
    # Custom CSS for Guinness branding
    st.markdown("""
    <style>
    /* Guinness Brand Colors */
    :root {
        --guinness-red: #E30613;
        --guinness-navy: #002855;
        --guinness-light-gray: #F5F5F5;
        --guinness-dark-gray: #333333;
    }
    
    /* Main container styling */
    .welcome-container {
        text-align: center;
        padding: 2rem;
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* Logo container */
    .logo-container {
        margin: 2rem auto;
        max-width: 300px;
    }
    
    /* Title styling */
    .welcome-title {
        color: var(--guinness-navy);
        font-size: 2.5rem;
        font-weight: 700;
        margin: 2rem 0 1rem 0;
        font-family: 'Arial', sans-serif;
    }
    
    /* Tagline styling */
    .welcome-tagline {
        color: var(--guinness-red);
        font-size: 1.5rem;
        font-weight: 500;
        margin-bottom: 2rem;
        font-style: italic;
    }
    
    /* Description text */
    .welcome-description {
        color: var(--guinness-dark-gray);
        font-size: 1.1rem;
        line-height: 1.6;
        margin-bottom: 2rem;
    }
    
    /* Feature cards */
    .feature-card {
        background-color: white;
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        border-color: var(--guinness-red);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .feature-title {
        color: var(--guinness-navy);
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .feature-description {
        color: var(--guinness-dark-gray);
        font-size: 1rem;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: var(--guinness-red);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 4px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #C00510;
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main welcome container
    st.markdown('<div class="welcome-container">', unsafe_allow_html=True)
    
    # Logo
    logo_path = Path("guinness_logo.png")
    if logo_path.exists():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(str(logo_path), use_column_width=True)
    
    # Title and tagline
    st.markdown('<h1 class="welcome-title">Guinness Global Investors</h1>', unsafe_allow_html=True)
    st.markdown('<p class="welcome-tagline">Positively Different</p>', unsafe_allow_html=True)
    
    # Description
    st.markdown("""
    <p class="welcome-description">
    Welcome to the Guinness Global Investors portfolio management platform. 
    Access comprehensive analytics, reports, and insights for our investment strategies.
    </p>
    """, unsafe_allow_html=True)
    
    # Feature cards in columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3 class="feature-title">📊 Portfolio Analytics</h3>
            <p class="feature-description">
            Real-time portfolio performance tracking and comprehensive risk analytics
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3 class="feature-title">📈 Fund Reports</h3>
            <p class="feature-description">
            Detailed fund performance reports with holdings analysis
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3 class="feature-title">🌍 Country Analysis</h3>
            <p class="feature-description">
            In-depth country risk assessments and market insights
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3 class="feature-title">🤖 AI Insights</h3>
            <p class="feature-description">
            Powered by advanced AI for intelligent portfolio recommendations
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Call to action
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Get Started", use_container_width=True):
            # Switch to Mexico report as default
            st.session_state.selected_report = "🇲🇽 Mexico"
            st.session_state.state["current_report"] = "🇲🇽 Mexico"
            st.rerun()
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
    © 2024 Guinness Global Investors. 100% Employee Owned.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)