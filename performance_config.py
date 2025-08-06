# performance_config.py - Performance optimization settings

import streamlit as st

def apply_performance_settings():
    """
    Apply performance optimizations to the Streamlit app.
    """
    # Reduce reconnection issues
    st.set_option('server.enableWebsocketCompression', True)
    
    # Session state initialization for better state management
    if 'performance_initialized' not in st.session_state:
        st.session_state.performance_initialized = True
        st.session_state.page_load_count = 0
        st.session_state.last_page = None
    
    # Track page changes
    current_page = st.session_state.get('current_page', 'welcome')
    if current_page != st.session_state.last_page:
        st.session_state.page_load_count += 1
        st.session_state.last_page = current_page

def optimize_sidebar():
    """
    Optimize sidebar rendering to reduce reconnections.
    """
    # Use container for sidebar content to prevent re-rendering
    if 'sidebar_container' not in st.session_state:
        st.session_state.sidebar_container = True
    
    # Minimize sidebar updates
    with st.sidebar:
        # Static content that doesn't change
        if st.session_state.sidebar_container:
            return True
    return False

def preload_common_data():
    """
    Preload commonly accessed data to improve performance.
    """
    if 'data_preloaded' not in st.session_state:
        st.session_state.data_preloaded = False
    
    if not st.session_state.data_preloaded:
        try:
            # Import optimized fetch functions
            from fetch_data import fetch_fund_data
            
            # Preload common funds in background
            common_funds = [
                "GGI Wealthy Nations Bond Fund",
                "Shin Kong Emerging Wealthy Nations Bond Fund"
            ]
            
            for fund in common_funds:
                try:
                    # This will cache the data
                    fetch_fund_data(fund, "Latest")
                except:
                    pass
            
            st.session_state.data_preloaded = True
        except:
            pass

def use_container_pattern():
    """
    Use container pattern to reduce re-rendering.
    Returns containers for consistent element placement.
    """
    if 'containers' not in st.session_state:
        st.session_state.containers = {
            'header': st.container(),
            'main': st.container(),
            'footer': st.container()
        }
    
    return st.session_state.containers

def optimize_charts():
    """
    Chart optimization settings.
    """
    return {
        'config': {
            'displayModeBar': False,  # Hide plotly toolbar
            'staticPlot': False,      # Keep interactivity
            'responsive': True
        },
        'layout_args': {
            'transition_duration': 0,  # Disable animations
            'autosize': True,
            'margin': dict(l=20, r=20, t=40, b=20)
        }
    }

def batch_api_calls(requests_list):
    """
    Batch multiple API calls to reduce latency.
    """
    import concurrent.futures
    import requests
    
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_to_request = {
            executor.submit(
                requests.post,
                req['url'],
                json=req['payload'],
                headers=req.get('headers', {}),
                timeout=req.get('timeout', 10)
            ): req for req in requests_list
        }
        
        for future in concurrent.futures.as_completed(future_to_request):
            req = future_to_request[future]
            try:
                response = future.result()
                results.append({
                    'request': req,
                    'response': response.json() if response.status_code == 200 else None,
                    'status': response.status_code
                })
            except Exception as e:
                results.append({
                    'request': req,
                    'response': None,
                    'error': str(e)
                })
    
    return results

def minimize_reruns():
    """
    Strategies to minimize Streamlit reruns.
    """
    # Use session state for form data
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {}
    
    # Use callbacks instead of direct value checks
    def update_callback(key):
        st.session_state.form_data[key] = st.session_state[key]
    
    return update_callback

# CSS to improve perceived performance
def inject_performance_css():
    """
    CSS optimizations for better performance perception.
    """
    st.markdown("""
    <style>
    /* Reduce layout shift */
    .stApp {
        overflow-x: hidden;
    }
    
    /* Optimize animations */
    * {
        animation-duration: 0.3s !important;
        transition-duration: 0.3s !important;
    }
    
    /* Preload spinner optimization */
    .stSpinner > div {
        animation-duration: 0.8s !important;
    }
    
    /* Reduce reflow on data updates */
    .dataframe {
        contain: layout style;
    }
    
    /* Optimize chart containers */
    .plotly-graph-div {
        contain: layout style;
    }
    
    /* Hide reconnecting message initially */
    .stConnectionStatus {
        opacity: 0;
        transition: opacity 0.3s ease-in-out;
    }
    
    .stConnectionStatus[data-testid="stConnectionStatus"] {
        opacity: 1;
    }
    </style>
    """, unsafe_allow_html=True)