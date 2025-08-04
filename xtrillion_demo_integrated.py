"""
XTrillion Demo - Integrated Cloud Version
"""
import streamlit as st
import uuid
import os
import time
from pathlib import Path

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

# Define available reports (simplified for cloud)
available_reports = {
    "Welcome": "👋 Welcome",
    "User Guide": "📚 User Guide",
    "Bond Information": "🖥️ Bond Information",
    "ChatbotPage": "💬 ChatbotPage",
    "System Status": "🔧 System Status"
}

# Initialize app state
if "state" not in st.session_state:
    st.session_state.state = {
        "selected_reports": list(available_reports.values()),
        "dropdown_reports": list(available_reports.values()),
        "report_checkboxes": {name: True for name in available_reports},
        "current_report": "👋 Welcome",
        "time_selection": "Latest",
        "mode": "auto"
    }

if "selected_report" not in st.session_state:
    st.session_state.selected_report = st.session_state.state["current_report"]

# Import modules with fallbacks
modules_status = {}

try:
    from welcome_page import display_welcome_page
    modules_status['welcome_page'] = True
except:
    modules_status['welcome_page'] = False
    def display_welcome_page():
        st.title("🌟 Welcome to XTrillion")
        st.success("✅ Successfully deployed to Railway!")
        if os.path.exists('xtrillion_splash_orange.png'):
            st.image('xtrillion_splash_orange.png', width=600)

try:
    from user_guide import display_user_guide
    modules_status['user_guide'] = True
except:
    modules_status['user_guide'] = False
    def display_user_guide():
        st.header("📚 User Guide")
        st.info("User guide module loading...")

try:
    from bond_information import create_bond_information_tab
    modules_status['bond_information'] = True
except:
    modules_status['bond_information'] = False
    def create_bond_information_tab():
        st.header("🖥️ Bond Information")
        st.info("Bond information module not available in cloud version yet")

try:
    import chatbot_demo
    modules_status['chatbot'] = True
except:
    modules_status['chatbot'] = False

try:
    from sidebar_demo import render_sidebar
    modules_status['sidebar'] = True
except:
    modules_status['sidebar'] = False
    render_sidebar = None

# CSS styling
st.markdown("""
    <style>
    .stApp {
        background-color: #1f1f1f;
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

# Main app logic
def main():
    # Render sidebar
    with st.sidebar:
        st.header("🌟 XTrillion Demo")
        st.divider()
        
        # Navigation dropdown
        selected_display = st.selectbox(
            "Select Page",
            options=list(available_reports.values()),
            index=list(available_reports.values()).index(st.session_state.selected_report)
        )
        
        # Update session state
        if selected_display != st.session_state.selected_report:
            st.session_state.selected_report = selected_display
            st.session_state.state["current_report"] = selected_display
            st.rerun()
        
        st.divider()
        
        # Module status
        with st.expander("Module Status", expanded=False):
            for module, status in modules_status.items():
                if status:
                    st.success(f"✅ {module}")
                else:
                    st.warning(f"⚠️ {module}")
        
        st.divider()
        st.caption("Cloud Version 1.0")
    
    # Main content area
    current_page = st.session_state.selected_report
    
    if current_page == "👋 Welcome":
        if modules_status['welcome_page']:
            display_welcome_page()
        else:
            st.title("🌟 Welcome to XTrillion")
            st.success("✅ Successfully deployed to Railway!")
            
    elif current_page == "📚 User Guide":
        if modules_status['user_guide']:
            display_user_guide()
        else:
            st.header("📚 User Guide")
            st.markdown("User guide will be available soon")
            
    elif current_page == "🖥️ Bond Information":
        if modules_status['bond_information']:
            create_bond_information_tab()
        else:
            st.header("🖥️ Bond Information")
            st.info("Bond analytics features coming soon")
            
    elif current_page == "💬 ChatbotPage":
        if modules_status['chatbot']:
            st.header("💬 Chatbot")
            # Add chatbot interface here
            chatbot_demo.main() if hasattr(chatbot_demo, 'main') else st.info("Chatbot loading...")
        else:
            st.header("💬 Chatbot")
            st.info("Chatbot module not available")
            
    elif current_page == "🔧 System Status":
        st.header("🔧 System Status")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Modules")
            for module, status in modules_status.items():
                if status:
                    st.success(f"✅ {module}: Loaded")
                else:
                    st.warning(f"⚠️ {module}: Not available")
        
        with col2:
            st.subheader("Environment")
            st.code(f"Platform: Railway")
            st.code(f"Python: 3.10")
            st.code(f"Streamlit: {st.__version__}")

if __name__ == "__main__":
    main()