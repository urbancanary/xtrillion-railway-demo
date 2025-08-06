# navigation_debug.py - Debug navigation issues

import streamlit as st

def debug_navigation():
    """Add navigation debugging to the app"""
    
    # Show current URL and query params
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔍 Navigation Debug")
    
    # Get query params
    params = st.query_params
    if params:
        st.sidebar.write("**Query Params:**")
        for key, value in params.items():
            st.sidebar.write(f"- {key}: {value}")
    else:
        st.sidebar.write("No query params")
    
    # Show session state
    if 'current_page' in st.session_state:
        st.sidebar.write(f"**Current Page:** {st.session_state.current_page}")
    
    # Show page navigation status
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        ctx = get_script_run_ctx()
        if ctx:
            st.sidebar.write(f"**Page ID:** {ctx.page_script_hash}")
    except:
        pass
    
    # Check if navigation is working
    st.sidebar.markdown("---")
    if st.sidebar.button("Test Navigation"):
        st.sidebar.success("Navigation is responsive!")
    
    # Show Streamlit version
    st.sidebar.write(f"**Streamlit:** {st.__version__}")

def add_navigation_tracking():
    """Add tracking to monitor page changes"""
    
    # Initialize tracking
    if 'page_history' not in st.session_state:
        st.session_state.page_history = []
    
    # Get current page from URL
    current_url = st.get_option("browser.serverAddress")
    
    # Track page change
    if len(st.session_state.page_history) == 0 or st.session_state.page_history[-1] != current_url:
        st.session_state.page_history.append(current_url)
        
        # Keep only last 10 entries
        if len(st.session_state.page_history) > 10:
            st.session_state.page_history = st.session_state.page_history[-10:]
    
    return st.session_state.page_history