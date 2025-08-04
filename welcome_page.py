# welcome_page.py

import streamlit as st

def display_welcome_page(): 

# Custom CSS to remove padding and make image full-screen
    st.markdown(
        """
        <style>
        /* Remove padding and margins from the main container */
        .block-container {
            padding-left: 0rem;
            padding-right: 0rem;
        }
        /* Make the image take the full width of the screen */
        img {
            width: 100%;
            height: auto;
        }
        </style>
        """, unsafe_allow_html=True
    )

    st.markdown(
    """
    <style>
    /* Centering the logo */
    .centered-logo {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh; /* Full viewport height */
    }

    /* Make the image responsive */
    .centered-logo img {
        max-width: 100%;
        height: auto;
    }

    </style>
    """, unsafe_allow_html=True
)
    try:
        st.image("xtrillion_splash_orange.png", use_column_width=True)  # Make sure file exists and has correct extension
    except Exception as e:
        st.error(f"Error displaying image: {e}")

    
    st.write("""
    Welcome to the Xtrillion Dashboard, your comprehensive tool for financial analysis and insights.
    
    Use the sidebar to navigate between different reports and tools:
    - Bond Information
    - Country Reports
    - Fund Reports
    - AI Assistant
    
    Get started by selecting a report from the sidebar menu.
    
    """)
    
    st.markdown("---")
    st.write("© 2023 Xtrillion. All rights reserved.")