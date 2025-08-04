# user_guide.py
import streamlit as st

def display_user_guide():
    # Page title
    st.title("📖 Welcome to the Xtrillion3 Dashboard User Guide")

    # Overview section
    st.header("Overview")
    st.write("""
    The Xtrillion3 Dashboard provides a streamlined interface for accessing financial reports, country-specific data, 
    and interacting with a chatbot for assistance. This guide will help you navigate the site and utilize its features efficiently.
    """)

    # Section 1: Selecting a Report
    st.header("1. Selecting a Report")
    st.write("""
    The sidebar on the left contains a menu for selecting various reports. You can view reports for specific countries and funds. Here’s how to do it:
    """)
    st.subheader("Country Reports")
    st.write("""
    Available reports include country-specific financial data for Israel 🇮🇱, Qatar 🇶🇦, Mexico 🇲🇽, and Saudi Arabia 🇸🇦. Simply select a country from the dropdown to display its detailed report.
    """)
    st.markdown("[View the Israel Report](#)")

    st.subheader("Fund Reports")
    st.write("""
    The following two funds are available:
    - **Shin Kong Emerging Wealthy Nations Bond Fund (🟠 SKEWNBF)**: Focused on wealthy nations and emerging markets.
    - **Shin Kong Environmental Sustainability Bond Fund (🟢 SKESBF)**: Focused on green and sustainable investments.
    """)
    st.write("You can choose to view different time periods for these funds, such as 'Latest' or 'Month End,' to explore their performance over time.")
    st.markdown("[View the Emerging Wealthy Nations Fund](#)")

    # Section 2: Customizing the Dropdown
    st.header("2. Customizing the Dropdown")
    st.write("""
    You can control which reports appear in the dropdown by using the **'Select Reports to Display'** section in the sidebar. Here's how to do it:
    """)
    st.write("""
    - **Selecting Reports**: Use the checkboxes to add or remove countries and funds from the dropdown. When you check or uncheck a report, the dropdown will automatically update to reflect your selections.
    """)
    st.markdown("Example: Select **Mexico** 🇲🇽 to add it to the dropdown.")

    # Section 3: Using the Chatbot
    st.header("3. Using the Chatbot")
    st.write("""
    Our integrated chatbot is here to assist you with questions or navigation:
    - Type a question in the **'Ask me anything'** field on the sidebar.
    - The chatbot can answer inquiries about the reports, help explain data, or guide you through the site.
    """)
    st.write("Example: Type `What is the latest update for SKEWNBF?` to ask about the Shin Kong Emerging Wealthy Nations Bond Fund.")

    # Section 4: Refreshing the Data
    st.header("4. Refreshing the Data")
    st.write("""
    If you want to refresh the data, click the **'Refresh Data'** button at the bottom of the sidebar. This will clear cached information and load the most up-to-date data available.
    """)

    # Section 5: Help and Support
    st.header("5. Help and Support")
    st.write("""
    For additional support or if you encounter any issues, feel free to visit this help page. The chatbot is also available to answer any frequently asked questions and assist with your queries.
    """)

    # Add example links
    st.write("### Example Links:")
    st.markdown("[View the Israel Report](#)")
    st.markdown("[View the Emerging Wealthy Nations Fund](#)")
