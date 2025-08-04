import streamlit as st
from pathlib import Path
import os
import numpy as np

from bond_information import get_bond_options

def render_sidebar(available_reports, sorted_files, chatbot=None):
    with st.sidebar:
        st.title("Xtrillion Dashboard")
        st.write("Welcome to the Xtrillion Dashboard. Use the options below to navigate through different reports and features.")

        # Dropdown to select a report
        selected_report = st.selectbox(
            "Select a report to view:",
            st.session_state.state["dropdown_reports"],
            index=st.session_state.state["dropdown_reports"].index(st.session_state.state["current_report"]),
            key="report_dropdown_selection_sidebar"
        )

        # Update session state when a new report is selected
        if selected_report != st.session_state.state["current_report"]:
            st.session_state.state["current_report"] = selected_report
            st.session_state.selected_report = selected_report
            st.rerun()

        # Handle Deep Dive Radio Episodes if selected
        if st.session_state.selected_report == "📻 Deep Dive Radio":
            with st.expander("🎧 Deep Dive Radio Episodes", expanded=True):
                st.header("Episodes")
                for file in sorted_files:
                    title = file.stem.replace('_', ' ').title()
                    if st.button(title, key=f"play_{file.name}", help=f"Click to play {title}"):
                        st.session_state.selected_file = file

        # Bond selection dropdown (only show when Bond Information is selected)
        if st.session_state.selected_report == "🖥️ Bond Information":
            bond_options = get_bond_options('data.csv')

            # Convert to list if it's a NumPy array
            if isinstance(bond_options, np.ndarray):
                bond_options = bond_options.tolist()

            if len(bond_options) == 0:
                st.warning("No bond options available.")
            else:
                st.session_state.bond_selection_sidebar = st.selectbox(
                    "Select a Bond",
                    options=bond_options,
                    key="bond_dropdown_selection_sidebar"
                )

        # Add time selection dropdown for fund reports
        if st.session_state.selected_report in ["🟠 SKEWNBF", "🟢 SKESBF"]:
            st.session_state.state["time_selection"] = st.selectbox(
                "Select time period:",
                ["Latest", "Month End"],
                key="time_selection_sidebar"
            )

        # Allow users to select reports to display
        with st.expander("🔍 Select Reports to Display", expanded=False):
            for report_name, tab_name in available_reports.items():
                if tab_name == "👋 Welcome":
                    st.checkbox(
                        report_name,
                        value=True,
                        disabled=True,
                        key=f"checkbox_{tab_name}_sidebar",
                        help="This report is always displayed as the welcome page."
                    )
                    continue

                unique_key = f"checkbox_{report_name.replace(' ', '_').lower()}_{tab_name.replace(' ', '_').lower()}_sidebar"
                checked = st.checkbox(
                    report_name,
                    value=st.session_state.state["report_checkboxes"].get(report_name, True),
                    key=unique_key
                )

                # Update which reports are visible in the dropdown
                if checked and tab_name not in st.session_state.state["dropdown_reports"]:
                    st.session_state.state["dropdown_reports"].append(tab_name)
                elif not checked and tab_name in st.session_state.state["dropdown_reports"]:
                    st.session_state.state["dropdown_reports"].remove(tab_name)

                # Store checkbox state
                st.session_state.state["report_checkboxes"][report_name] = checked

        # Embedding mode selector at the bottom of the sidebar
        st.markdown("## Chat Mode")
        embedding_mode = st.selectbox(
            "Select chat mode:",
            ["🔵 auto", "🟢 andy_view", "🟠 general", "⚪ none"],
            key="embedding_mode_selector_sidebar"
        )
        st.session_state.state["mode"] = embedding_mode.split()[-1]  # Extract mode without emoji

        # Add a note about the default view
        st.info("The dashboard defaults to the Mexico Credit Report. Use the dropdown above to explore other reports and features.")