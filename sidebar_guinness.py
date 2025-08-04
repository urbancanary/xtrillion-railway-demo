import streamlit as st
from pathlib import Path
import os
import numpy as np

def render_sidebar(available_reports, sorted_files=None, chatbot=None):
    with st.sidebar:
        # Guinness branding
        st.markdown("""
        <style>
        .sidebar-title {
            color: #002855;
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        .sidebar-subtitle {
            color: #E30613;
            font-size: 1.1rem;
            font-style: italic;
            margin-bottom: 1rem;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<h1 class="sidebar-title">Guinness Global Investors</h1>', unsafe_allow_html=True)
        st.markdown('<p class="sidebar-subtitle">Positively Different</p>', unsafe_allow_html=True)
        
        st.write("Portfolio management and analytics platform")
        
        st.divider()

        # Dropdown to select a report
        selected_report = st.selectbox(
            "📊 Select Report:",
            st.session_state.state["dropdown_reports"],
            index=st.session_state.state["dropdown_reports"].index(st.session_state.state["current_report"]),
            key="report_dropdown_selection_sidebar"
        )

        # Update session state when a new report is selected
        if selected_report != st.session_state.state["current_report"]:
            st.session_state.state["current_report"] = selected_report
            st.session_state.selected_report = selected_report
            st.rerun()

        # Add time selection dropdown for fund reports
        if st.session_state.selected_report in ["🟠 SKEWNBF", "🟢 SKESBF"]:
            st.session_state.state["time_selection"] = st.selectbox(
                "📅 Time Period:",
                ["Latest", "Month End"],
                key="time_selection_sidebar"
            )

        # Chat mode selector
        st.divider()
        st.markdown("### 🤖 AI Assistant")
        embedding_mode = st.selectbox(
            "Select mode:",
            ["🔵 Auto", "🟢 Detailed", "🟠 Concise", "⚪ Disabled"],
            key="embedding_mode_selector_sidebar"
        )
        # Extract mode without emoji and convert to lowercase
        mode_map = {
            "🔵 Auto": "auto",
            "🟢 Detailed": "andy_view", 
            "🟠 Concise": "general",
            "⚪ Disabled": "none"
        }
        st.session_state.state["mode"] = mode_map.get(embedding_mode, "auto")

        # Footer
        st.divider()
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0; color: #666; font-size: 0.8rem;">
        © 2024 Guinness Global Investors<br>
        100% Employee Owned
        </div>
        """, unsafe_allow_html=True)