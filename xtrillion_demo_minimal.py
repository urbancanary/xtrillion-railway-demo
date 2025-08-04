import streamlit as st
import time
from datetime import datetime

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

# Simple welcome page
st.title("🌟 XTrillion Demo")
st.markdown("### Successfully Deployed to Railway!")

# Status info
col1, col2, col3 = st.columns(3)
with col1:
    st.info("🚀 **Status**: Running")
with col2:
    st.success("☁️ **Platform**: Railway") 
with col3:
    st.warning(f"🕐 **Time**: {datetime.now().strftime('%H:%M:%S')}")

st.divider()

# Basic functionality test
st.subheader("Basic Functionality Test")

# Text input
name = st.text_input("Enter your name:", "User")
st.write(f"Hello, {name}! 👋")

# Button test
if st.button("Click me!"):
    with st.spinner("Processing..."):
        time.sleep(1)
    st.balloons()
    st.success("Button works! 🎉")

# Sidebar
with st.sidebar:
    st.header("XTrillion Demo")
    st.write("This is a minimal deployment test")
    
    st.divider()
    
    st.caption("Next steps:")
    st.caption("- Add authentication")
    st.caption("- Connect to APIs")
    st.caption("- Add bond analytics")
    
    st.divider()
    st.caption("Version: 0.1.0-minimal")