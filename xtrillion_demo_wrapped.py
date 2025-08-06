"""
XTrillion Demo - Cloud-ready version with graceful fallbacks
"""
import streamlit as st
import os
import sys
from datetime import datetime

# Configure the page
st.set_page_config(
    page_title="XTrillion Demo",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "XTrillion Demo Application"
    }
)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "Welcome"

# Try to import modules with fallbacks
modules_status = {}

try:
    from welcome_page import display_welcome_page
    modules_status['welcome_page'] = True
except ImportError:
    modules_status['welcome_page'] = False
    def display_welcome_page():
        st.title("🌟 Welcome to XTrillion")
        st.markdown("### Your Bond Analytics Platform")
        st.info("Welcome module not available - showing basic welcome")

try:
    from user_guide import display_user_guide
    modules_status['user_guide'] = True
except ImportError:
    modules_status['user_guide'] = False
    def display_user_guide():
        st.header("📚 User Guide")
        st.info("User guide module not available")

try:
    from sidebar_demo import render_sidebar
    modules_status['sidebar'] = True
    # Create a wrapper to match expected function name
    def sidebar_component():
        # render_sidebar expects these parameters
        available_reports = []
        sorted_files = []
        chatbot = None
        render_sidebar(available_reports, sorted_files, chatbot)
except Exception as e:
    modules_status['sidebar'] = False
    sidebar_error = str(e)
    def sidebar_component():
        with st.sidebar:
            st.header("XTrillion Demo")
            st.write("Basic sidebar active")

try:
    import chatbot_demo
    modules_status['chatbot'] = True
except ImportError:
    modules_status['chatbot'] = False

# Main app
def main():
    # Try to use sidebar component
    if modules_status['sidebar']:
        try:
            sidebar_component()
        except:
            pass
    else:
        # Basic sidebar
        with st.sidebar:
            st.header("🌟 XTrillion")
            st.divider()
            
            # Tab selection
            tabs = ["Welcome", "User Guide", "Status", "About"]
            selected_tab = st.radio("Navigate", tabs)
            st.session_state.active_tab = selected_tab
            
            st.divider()
            st.caption("Version: Cloud Demo")
            st.caption(f"Time: {datetime.now().strftime('%H:%M:%S')}")
    
    # Main content area
    tab = st.session_state.get('active_tab', 'Welcome')
    
    if tab == "Welcome":
        if modules_status['welcome_page']:
            display_welcome_page()
        else:
            st.title("🌟 Welcome to XTrillion")
            st.markdown("### Bond Analytics in the Cloud")
            st.success("✅ Successfully deployed to Railway!")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Status", "Online")
            with col2:
                st.metric("Platform", "Railway")
            with col3:
                st.metric("Version", "1.0.0")
    
    elif tab == "User Guide":
        if modules_status['user_guide']:
            display_user_guide()
        else:
            st.header("📚 User Guide")
            st.markdown("""
            ### Getting Started
            - This is the XTrillion demo application
            - Currently running in cloud mode
            - Some features may be limited
            
            ### Available Features
            - Basic navigation
            - Status monitoring
            - About information
            """)
    
    elif tab == "Status":
        st.header("🔧 System Status")
        
        st.subheader("Module Status")
        for module, status in modules_status.items():
            if status:
                st.success(f"✅ {module}: Loaded")
            else:
                st.warning(f"⚠️ {module}: Not available")
        
        st.subheader("Environment")
        st.code(f"Python: {sys.version}")
        st.code(f"Streamlit: {st.__version__}")
        st.code(f"Working Directory: {os.getcwd()}")
    
    else:  # About
        st.header("ℹ️ About XTrillion")
        st.markdown("""
        ### XTrillion Demo - Cloud Edition
        
        This is the cloud-deployed version of XTrillion, running on Railway.
        
        **Features:**
        - Bond analytics (coming soon)
        - Portfolio management (coming soon)
        - Real-time data integration (coming soon)
        
        **Current Status:**
        - Basic framework deployed
        - Modules being added incrementally
        - Full functionality coming soon
        """)

if __name__ == "__main__":
    main()