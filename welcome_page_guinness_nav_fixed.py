import streamlit as st
from logo_utils import get_logo_base64

def display_welcome_page():
    """Display the Guinness-branded welcome page"""
    
    # Custom CSS for centering and styling
    st.markdown("""
    <style>
        .welcome-container {
            text-align: left;
            max-width: 1000px;
            margin: 0 auto;
            padding: 2rem;
        }
        .brand-title {
            color: #C8102E;
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
            line-height: 1.2;
        }
        .brand-subtitle {
            color: #ffffff;
            font-size: 1.8rem;
            margin-bottom: 0.5rem;
        }
        .brand-tagline {
            color: #6BBBAE;
            font-style: italic;
            font-size: 1.2rem;
            margin-bottom: 2rem;
        }
        .welcome-text {
            color: #cccccc;
            font-size: 1.1rem;
            line-height: 1.6;
            margin-bottom: 2rem;
        }
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }
        .feature-card {
            background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%);
            border-radius: 10px;
            padding: 1.5rem;
            border: 1px solid #3a3a3a;
            transition: all 0.3s ease;
            height: 100%;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            border-color: #C8102E;
        }
        .feature-emoji {
            font-size: 3.5rem;
            margin-bottom: 1rem;
            display: block;
            text-align: left;
        }
        .feature-title {
            color: #C8102E;
            font-size: 1.4rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
            text-align: left;
        }
        .feature-description {
            color: #9DB9D5;
            font-size: 1rem;
            line-height: 1.4;
            text-align: left;
        }
        .getting-started {
            background: #2a2a2a;
            border-radius: 10px;
            padding: 2rem;
            margin-top: 2rem;
            border: 1px solid #3a3a3a;
        }
        .logo-title-container {
            display: flex;
            align-items: center;
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        
        .logo-button {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background-color: #2a2a2a;
            border: 2px solid #3a3a3a;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
            cursor: pointer;
            flex-shrink: 0;
        }
        
        .logo-button:hover {
            transform: scale(1.05);
            border-color: #C8102E;
            box-shadow: 0 0 20px rgba(200, 16, 46, 0.3);
        }
        
        .logo-button img {
            width: 50px;
            height: 50px;
            object-fit: contain;
        }
        
        .title-section {
            flex-grow: 1;
        }
        
        /* Modern card styling with glass morphism effect */
        .feature-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, rgba(200,16,46,0.1) 0%, transparent 50%);
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        .feature-card:hover::before {
            opacity: 1;
        }
        
        /* Remove button styling to make entire card clickable */
        .feature-card button {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: transparent;
            border: none;
            cursor: pointer;
            opacity: 0;
        }
        
        
        /* Interactive elements highlight */
        .highlight-box {
            background: rgba(200,16,46,0.1);
            border: 1px solid #C8102E;
            border-radius: 5px;
            padding: 1rem;
            margin: 1rem 0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Main welcome container
    st.markdown('<div class="welcome-container">', unsafe_allow_html=True)
    
    # Logo and title section - circular logo button next to title
    logo_base64 = get_logo_base64()
    
    st.markdown(f"""
        <div class="logo-title-container">
            <div class="logo-button">
                <img src="data:image/png;base64,{logo_base64}" alt="Guinness Logo">
            </div>
            <div class="title-section">
                <h1 class="brand-title">Guinness Global Investors</h1>
                <h2 class="brand-subtitle">Fixed Income Portfolio Analytics Platform</h2>
                <p class="brand-tagline">Institutional-grade bond analytics powered by advanced quantitative models</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Welcome text
    st.markdown("""
        <div class="welcome-text">
            Welcome to the Guinness Global Investors portfolio management platform. 
            Access comprehensive analytics, real-time valuations, and sophisticated risk metrics 
            for your fixed income portfolios.
        </div>
    """, unsafe_allow_html=True)
    
    # Quick stats - if we have data
    try:
        import pandas as pd
        fund_data = pd.read_csv('data_with_ggi.csv')
        ggi_data = fund_data[fund_data['fund_name'] == 'Guinness Global Investors Fund']
        if not ggi_data.empty:
            total_value = ggi_data['market_value'].sum()
            num_holdings = len(ggi_data[ggi_data['name'] != 'Cash'])
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Portfolio Value", f"${total_value:,.0f}")
            with col2:
                st.metric("Holdings", num_holdings)
            with col3:
                st.metric("Avg Yield", f"{ggi_data['yield'].astype(float).mean():.2f}%")
            with col4:
                st.metric("Avg Duration", f"{ggi_data['duration'].astype(float).mean():.1f}y")
    except:
        pass
    
    # Feature cards grid with proper navigation
    st.markdown('<div class="feature-grid">', unsafe_allow_html=True)
    
    # Portfolio Analytics Card
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-emoji">🌐</span>
            <div class="feature-title">Portfolio Analytics</div>
            <div class="feature-description">
                Deep dive into GGI, SKEWNBF, and SKESBF portfolios with comprehensive metrics, 
                performance attribution, and risk analysis
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Use a link button instead of navigation
        if st.button(
            "View GGI Portfolio →",
            key="ggi_link",
            use_container_width=True,
            help="Click to view GGI Portfolio"
        ):
            st.session_state.sidebar_state = "expanded"
            st.info("👈 Please select 'GGI Portfolio' from the sidebar menu")
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-emoji">🌍</span>
            <div class="feature-title">Country Analysis</div>
            <div class="feature-description">
                In-depth sovereign and corporate bond analysis for Israel, Qatar, Mexico, 
                and Saudi Arabia with market insights
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(
            "View Country Reports →",
            key="country_link",
            use_container_width=True,
            help="Click to view Country Analysis"
        ):
            st.session_state.sidebar_state = "expanded"
            st.info("👈 Please select a country from the sidebar menu")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-emoji">📊</span>
            <div class="feature-title">Fund Reports</div>
            <div class="feature-description">
                Comprehensive fund analysis with performance metrics, holdings breakdown, 
                and comparative benchmarking
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(
            "View Fund Reports →",
            key="fund_link",
            use_container_width=True,
            help="Click to view Fund Reports"
        ):
            st.session_state.sidebar_state = "expanded"
            st.info("👈 Please select a fund from the sidebar menu")
    
    with col4:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-emoji">💰</span>
            <div class="feature-title">Portfolio Tools</div>
            <div class="feature-description">
                Portfolio valuation with P&L analysis, risk metrics, and comprehensive 
                user guide for all platform features
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(
            "Open Portfolio Valuation →",
            key="valuation_link",
            use_container_width=True,
            help="Click to use Portfolio Valuation"
        ):
            st.session_state.sidebar_state = "expanded"
            st.info("👈 Please select 'Portfolio Valuation' from the sidebar menu")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Getting started section
    st.markdown("""
        <div class="getting-started">
            <h3 style="color: #C8102E; margin-bottom: 1rem;">🚀 Getting Started</h3>
            <ol style="color: #cccccc; line-height: 1.8;">
                <li><strong>Select a Portfolio:</strong> Choose from GGI, SKEWNBF, or SKESBF funds in the sidebar</li>
                <li><strong>Explore Analytics:</strong> View detailed holdings, performance metrics, and risk analysis</li>
                <li><strong>Use Tools:</strong> Access portfolio valuation and view the comprehensive user guide</li>
                <li><strong>Export Data:</strong> Download reports and data in multiple formats</li>
            </ol>
        </div>
    """, unsafe_allow_html=True)
    
    # Platform features
    with st.expander("📋 Platform Features", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Portfolio Management**
            - Real-time portfolio valuation
            - P&L analysis and attribution
            - Risk metrics and stress testing
            - Holdings breakdown and analytics
            
            **Coming Soon**
            - Bond calculator with YTM analysis
            - Trade simulator for what-if scenarios
            - AI-powered portfolio assistant
            - Advanced risk analytics
            """)
        
        with col2:
            st.markdown("""
            **Data & Reporting**
            - Interactive data tables with search
            - Export to Excel, CSV, and PDF
            - Customizable chart visualizations
            - Historical performance tracking
            
            **Available Tools**
            - Portfolio Valuation with P&L
            - Country-specific bond reports
            - Fund performance analytics
            - Comprehensive user guide
            """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; color: #666; font-size: 0.9rem;">
            <p>© 2024 Guinness Global Investors. Professional fixed income analytics platform.</p>
            <p>Powered by XTrillion Core Analytics Engine | Data as of latest market close</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)