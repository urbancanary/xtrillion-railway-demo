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
            white-space: nowrap;
        }
        .brand-subtitle {
            color: #ffffff;
            font-size: 1.8rem;
            margin-bottom: 0.5rem;
        }
        .brand-tagline {
            color: #C8102E;
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
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .feature-card:hover {
            transform: translateY(-5px);
            border-color: #C8102E;
            background: linear-gradient(135deg, #3a3a3a 0%, #2a2a2a 100%);
            box-shadow: 0 6px 12px rgba(227, 6, 19, 0.2);
        }
        .feature-icon {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }
        .feature-title {
            color: #C8102E;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        .feature-desc {
            color: #cccccc;
            font-size: 0.9rem;
        }
        .nav-hint {
            background-color: #2a2a2a;
            border-left: 4px solid #C8102E;
            padding: 1rem;
            margin: 2rem 0;
            border-radius: 5px;
        }
        .nav-hint-text {
            color: #ffffff;
            font-size: 1.1rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Main container
    st.markdown('<div class="welcome-container">', unsafe_allow_html=True)
    
    # Header with logo and company name aligned
    # Get base64 encoded logo
    logo_base64 = get_logo_base64()
    
    if logo_base64:
        # Logo and brand text in horizontal layout - left aligned
        st.markdown(f"""
        <div style="display: flex; align-items: center; justify-content: flex-start; margin-bottom: 2rem;">
            <div style="width: 120px; height: 120px; background-color: #ffffff; 
                        border-radius: 50%; display: flex; 
                        align-items: center; justify-content: center; 
                        box-shadow: 0 4px 6px rgba(0,0,0,0.3); overflow: hidden; 
                        margin-right: 2rem;">
                <img src="data:image/png;base64,{logo_base64}" 
                     style="width: 70%; height: auto; object-fit: contain;">
            </div>
            <div style="text-align: left;">
                <h1 style="color: #C8102E; font-size: 2.5rem; font-weight: bold; 
                           margin: 0; line-height: 1.2; white-space: nowrap;">
                    Guinness Global Investors
                </h1>
                <p style="color: #C8102E; font-style: italic; font-size: 1.2rem; 
                          margin: 0.5rem 0 0 0;">
                    Positively Different
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Fallback with G placeholder - left aligned
        st.markdown("""
        <div style="display: flex; align-items: center; justify-content: flex-start; margin-bottom: 2rem;">
            <div style="width: 120px; height: 120px; background-color: #ffffff; 
                        border-radius: 50%; display: flex; 
                        align-items: center; justify-content: center; 
                        box-shadow: 0 4px 6px rgba(0,0,0,0.3); margin-right: 2rem;">
                <span style="color: #C8102E; font-size: 48px; font-weight: bold;">G</span>
            </div>
            <div style="text-align: left;">
                <h1 style="color: #C8102E; font-size: 2.5rem; font-weight: bold; 
                           margin: 0; line-height: 1.2; white-space: nowrap;">
                    Guinness Global Investors
                </h1>
                <p style="color: #C8102E; font-style: italic; font-size: 1.2rem; 
                          margin: 0.5rem 0 0 0;">
                    Positively Different
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Welcome message
    st.markdown("""
    <div class="welcome-text">
    Welcome to the Guinness Global Investors portfolio management platform. 
    Access comprehensive fund reports, country analyses, and investment insights 
    all in one place.
    </div>
    """, unsafe_allow_html=True)
    
    # Feature cards - styled as clickable cards
    st.markdown("""
    <style>
        .stButton > button {
            height: 150px;
            width: 100%;
            background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%);
            border: 1px solid #3a3a3a;
            border-radius: 10px;
            transition: all 0.3s ease;
            padding: 1.5rem;
            text-align: left;
        }
        .stButton > button:hover {
            transform: translateY(-5px);
            border-color: #C8102E;
            background: linear-gradient(135deg, #3a3a3a 0%, #2a2a2a 100%);
            box-shadow: 0 6px 12px rgba(227, 6, 19, 0.2);
        }
        .stButton > button > div {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            gap: 0.5rem;
        }
        .card-icon {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }
        .card-title {
            color: #C8102E;
            font-weight: bold;
            font-size: 1.1rem;
            margin-bottom: 0.5rem;
        }
        .card-desc {
            color: #cccccc;
            font-size: 0.9rem;
            line-height: 1.4;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Create clickable cards that open sidebar
    col1, col2 = st.columns(2)
    
    with col1:
        # GGI Portfolio Card
        ggi_clicked = st.button(
            "🌐\n\n**GGI Portfolio**\n\nOur flagship Wealthy Nations Bond Fund with diversified holdings",
            key="ggi_card",
            use_container_width=True
        )
        if ggi_clicked:
            st.session_state.sidebar_state = "expanded"
            st.session_state.navigate_to = "ggi"
            st.rerun()
        
        # Country Analysis Card
        country_clicked = st.button(
            "🌍\n\n**Country Analysis**\n\nIn-depth reports on Israel, Qatar, Mexico, and Saudi Arabia",
            key="country_card",
            use_container_width=True
        )
        if country_clicked:
            st.session_state.sidebar_state = "expanded"
            st.session_state.navigate_to = "israel"
            st.rerun()
    
    with col2:
        # Fund Reports Card
        fund_clicked = st.button(
            "📊\n\n**Fund Reports**\n\nDetailed analysis of SKEWNBF and SKESBF funds",
            key="fund_card",
            use_container_width=True
        )
        if fund_clicked:
            st.session_state.sidebar_state = "expanded"
            st.session_state.navigate_to = "skewnbf"
            st.rerun()
        
        # Bond Calculator Card
        calc_clicked = st.button(
            "🧮\n\n**Bond Calculator**\n\nAdvanced bond analytics and portfolio calculations",
            key="calc_card",
            use_container_width=True
        )
        if calc_clicked:
            st.session_state.sidebar_state = "expanded"
            st.session_state.navigate_to = "calculator"
            st.rerun()
    
    # Navigation hint
    st.markdown("""
    <div class="nav-hint">
        <div class="nav-hint-text">
        👆 Click any card above to explore our reports and tools. 
        The navigation menu will open automatically to show all available options.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem; margin-top: 3rem;">
    © 2024 Guinness Global Investors. 100% Employee Owned.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)