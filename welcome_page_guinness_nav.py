import streamlit as st

def display_welcome_page():
    """Display the Guinness-branded welcome page"""
    
    # Custom CSS for centering and styling
    st.markdown("""
    <style>
        .welcome-container {
            text-align: center;
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
        }
        .brand-title {
            color: #E30613;
            font-size: 3.5rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        .brand-subtitle {
            color: #ffffff;
            font-size: 1.8rem;
            margin-bottom: 0.5rem;
        }
        .brand-tagline {
            color: #E30613;
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
            background-color: #2a2a2a;
            border-radius: 10px;
            padding: 1.5rem;
            border: 1px solid #3a3a3a;
            transition: transform 0.2s;
        }
        .feature-card:hover {
            transform: translateY(-5px);
            border-color: #E30613;
        }
        .feature-icon {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }
        .feature-title {
            color: #E30613;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        .feature-desc {
            color: #cccccc;
            font-size: 0.9rem;
        }
        .nav-hint {
            background-color: #2a2a2a;
            border-left: 4px solid #E30613;
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
    
    # Logo in circular frame
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Create a container with circular background
        st.markdown("""
        <style>
        .logo-circle {
            background-color: #E30613;
            border-radius: 50%;
            width: 150px;
            height: 150px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 1rem auto;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            padding: 25px;
        }
        .logo-circle img {
            max-width: 100%;
            max-height: 100%;
            filter: brightness(0) invert(1);
        }
        </style>
        <div class="logo-circle">
        """, unsafe_allow_html=True)
        
        # Display the logo
        st.image("guinness_logo.png", width=100)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Brand text
    st.markdown('<h1 class="brand-title">Guinness</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="brand-subtitle">Global Investors</h2>', unsafe_allow_html=True)
    st.markdown('<p class="brand-tagline">Positively Different</p>', unsafe_allow_html=True)
    
    # Welcome message
    st.markdown("""
    <div class="welcome-text">
    Welcome to the Guinness Global Investors portfolio management platform. 
    Access comprehensive fund reports, country analyses, and investment insights 
    all in one place.
    </div>
    """, unsafe_allow_html=True)
    
    # Feature cards
    st.markdown("""
    <div class="feature-grid">
        <div class="feature-card">
            <div class="feature-icon">🌐</div>
            <div class="feature-title">GGI Portfolio</div>
            <div class="feature-desc">Our flagship Wealthy Nations Bond Fund with diversified holdings</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Fund Reports</div>
            <div class="feature-desc">Detailed analysis of SKEWNBF and SKESBF funds</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🌍</div>
            <div class="feature-title">Country Analysis</div>
            <div class="feature-desc">In-depth reports on Israel, Qatar, Mexico, and Saudi Arabia</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">📈</div>
            <div class="feature-title">Real-time Data</div>
            <div class="feature-desc">Latest market data and portfolio performance metrics</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation hint
    st.markdown("""
    <div class="nav-hint">
        <div class="nav-hint-text">
        👈 Use the navigation menu on the left to explore our reports and tools.
        Start with <strong>GGI Portfolio</strong> to see our flagship fund.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
    © 2024 Guinness Global Investors. 100% Employee Owned.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)