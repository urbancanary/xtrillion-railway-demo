import streamlit as st
import plotly.express as px
import pandas as pd
import requests

# Main function to encapsulate the app logic
def main():
    # Set the page configuration
    st.set_page_config(layout="wide")

    # Custom CSS
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #1f1f1f;
            color: #ffffff;
            max-width: 2000px;
            margin: auto;
            padding-left: 4rem;
            padding-right: 4rem;
            display: flex;
            flex-direction: column;
            height: 100vh;
        }
        .reportColumn {
            width: 60% !important;
        }
        .chartColumn {
            width: 40% !important;
        }
        .data-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
            margin-top: 10px;
            margin-bottom: 30px;
        }
        .data-table th, .data-table td {
            border: 1px solid #ddd;
            padding: 4px;
            text-align: center;
        }
        .data-table th {
            background-color: #1f1f1f;
            color: white;
        }
        .data-table td {
            color: black;
            background-color: white;
        }
        .reportText {
            word-wrap: break-word;
            white-space: normal;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Custom color palette
    color_palette = [
        "#333333",  # Dark Gray/Black
        "#1F1F1F",  # Very Dark Gray
        "#F5F5F5",  # Light Gray
        "#005EB8",  # Corporate Blue
        "#66CC66",  # Soft Green (Positive Indicators)
        "#CC3333",  # Soft Red (Negative Indicators)
        "#FF9933",  # Orange Highlight
        "#FFCC00",  # Yellow Highlight
        "#FFFFFF"   # White (Text)
    ]


    # Custom color palette
    color_palette2 = [
        "#FFA500",  # Bright Orange
        "#007FFF",  # Azure Blue
        "#DC143C",  # Cherry Red
        "#39FF14",  # Electric Lime Green
        "#00FFFF",  # Cyan
        "#DA70D6"   # Vivid Purple
    ]

    # Create tabs for each country
    tabs = st.tabs(["Israel", "Qatar", "Mexico", "Saudi Arabia"])

    # Display the report in each tab
    with tabs[0]:
        display_report_for_country("Israel", color_palette)

    with tabs[1]:
        display_report_for_country("Qatar", color_palette)

    with tabs[2]:
        display_report_for_country("Mexico", color_palette)

    with tabs[3]:
        display_report_for_country("Saudi Arabia", color_palette)

# Function to fetch data from your API
@st.cache_data(persist="disk")
def fetch_data_for_country(country):
    url = "https://my-combined-app-vpljqiia2a-uc.a.run.app/process_json"
    payload = {
        "sample_key": f'{{"db_path": "credit_research.db", "table": "FullReport", "filters": {{"Country": "{country}"}}, "fields": "*", "page": 1, "page_size": 10}}'
    }

    all_data = []
    for page in range(1, 3):
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            all_data.extend(response.json())
        else:
            st.error(f"Failed to retrieve data for {country} (page {page})")
            return None
    
    if all_data:
        return all_data[0]
    else:
        return None

# Function to plot charts
def plot_chart(df, y_column, title, color):
    y_min = df[y_column].min()
    y_max = df[y_column].max()

    if y_min == y_max:
        y_range = [y_min - 1, y_max + 1]
    else:
        y_range = [y_min - 0.05 * abs(y_min), y_max + 0.05 * abs(y_max)]

    fig = px.bar(df, x='Year', y=y_column,
                 title=title,
                 color_discrete_sequence=[color],
                 height=375)
    fig.update_traces(marker_line_width=0)
    fig.update_layout(
        yaxis=dict(range=y_range),
        plot_bgcolor='#1f1f1f',
        paper_bgcolor='#1f1f1f',
        font=dict(color='white'),
        margin=dict(l=20, r=20, t=60, b=40),
        autosize=True
    )
    return fig

# Function to create data tables
@st.cache_data(persist="disk")
def create_data_table(df, y_column):
    table_html = "<table class='data-table'>"
    table_html += "<tr><th>Year</th>" + "".join([f"<th>{year}</th>" for year in df['Year']]) + "</tr>"
    table_html += f"<tr><td>{y_column}</td>"
    for value in df[y_column]:
        if value is not None:
            table_html += f"<td>{value:.2f}</td>"  # Format as a float with 2 decimal places
        else:
            table_html += "<td>N/A</td>"  # Use "N/A" for None values
    table_html += "</tr></table>"
    return table_html

# Function to display the report and charts
@st.cache_data(persist="disk")
def display_report_for_country(country, color_palette):
    report = fetch_data_for_country(country)

    if report:
        col1, col2 = st.columns([6, 4])

        with col1:
            st.markdown('<div class="reportColumn">', unsafe_allow_html=True)
            st.markdown(f'<h1 class="reportText">{report.get("Title", "Credit Research Report")}</h1>', unsafe_allow_html=True)
            st.markdown('<h2 class="reportText">Country Information</h2>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText"><strong>Country:</strong> {report.get("Country", "N/A")}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText"><strong>Ownership:</strong> {report.get("Ownership", "N/A")}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText"><strong>NFA Rating:</strong> {report.get("NFARating", "N/A")}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText"><strong>ESG Rating:</strong> {report.get("ESGRating", "N/A")}</p>', unsafe_allow_html=True)
            st.markdown('<h2 class="reportText">Overview</h2>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText">{report.get("Overview", "No overview available.")}</p>', unsafe_allow_html=True)
            st.markdown('<h2 class="reportText">Politics</h2>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText">{report.get("PoliticalNews", "No political news available.")}</p>', unsafe_allow_html=True)
            st.markdown('<h2 class="reportText">Strengths</h2>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText">{report.get("Strengths", "No strengths information available.")}</p>', unsafe_allow_html=True)
            st.markdown('<h2 class="reportText">Weaknesses</h2>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText">{report.get("Weaknesses", "No weaknesses information available.")}</p>', unsafe_allow_html=True)
            st.markdown('<h2 class="reportText">Opportunities</h2>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText">{report.get("Opportunities", "No opportunities information available.")}</p>', unsafe_allow_html=True)
            st.markdown('<h2 class="reportText">Threats</h2>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText">{report.get("Threats", "No threats information available.")}</p>', unsafe_allow_html=True)
            st.markdown('<h2 class="reportText">Recent News</h2>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText">{report.get("RecentNews", "No recent news available.")}</p>', unsafe_allow_html=True)
            st.markdown('<h2 class="reportText">Ratings and Comments from Credit Rating Agencies</h2>', unsafe_allow_html=True)
            st.markdown('<h3 class="reportText">Moody\'s:</h3>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText">{report.get("MoodysRating", "N/A")}</p>', unsafe_allow_html=True)
            st.markdown('<h3 class="reportText">S&P Global Ratings:</h3>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText">{report.get("SPGlobalRating", "N/A")}</p>', unsafe_allow_html=True)
            st.markdown('<h3 class="reportText">Fitch Ratings:</h3>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText">{report.get("FitchRating", "N/A")}</p>', unsafe_allow_html=True)
            st.markdown('<h2 class="reportText">Conclusion</h2>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText">{report.get("Conclusion", "No conclusion available.")}</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="chartColumn">', unsafe_allow_html=True)
            st.header("Economic Data (2024 Onwards)")

            charts_data = [
                ("GDP Growth (%)", [report.get(f'GDPGrowthRateYear{i}', 0) for i in range(1, 7)], color_palette[0]),
                ("Inflation Rate (%)", [report.get(f'InflationYear{i}', 0) for i in range(1, 7)], color_palette[1]),
                ("Unemployment Rate (%)", [report.get(f'UnemploymentRateYear{i}', 0) for i in range(1, 7)], color_palette[2]),
                ("Population (millions)", [report.get(f'PopulationYear{i}', 0) for i in range(1, 7)], color_palette[3]),
                ("Government Budget Balance (% of GDP)", [report.get(f'GovernmentFinancesYear{i}', 0) for i in range(1, 7)], color_palette[4]),
                ("Current Account Balance (% of GDP)", [report.get(f'CurrentAccountBalanceYear{i}', 0) for i in range(1, 7)], color_palette[5])
            ]

            years = [2024, 2025, 2026, 2027, 2028, 2029]

            for metric, values, color in charts_data:
                df = pd.DataFrame({
                    "Year": years,
                    metric: values
                })

                # Display the chart with the specified color
                st.plotly_chart(plot_chart(df, metric, metric, color), use_container_width=True)

                # Display the data table
                st.markdown(create_data_table(df, metric), unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error(f"No report found for {country}.")

if __name__ == "__main__":
    main()




@st.cache_data(persist="disk")
def create_country_report_tab(country, color_palette):
    """
    Function to create a country report tab.
    :param country: Name of the country for which the report is generated.
    :param color_palette: List of colors for chart generation.
    """

    def fetch_data_for_country(country):
        url = "https://my-combined-app-vpljqiia2a-uc.a.run.app/process_json"
        payload = {
            "sample_key": f'{{"db_path": "credit_research.db", "table": "FullReport", "filters": {{"Country": "{country}"}}, "fields": "*", "page": 1, "page_size": 10}}'
        }

        all_data = []
        for page in range(1, 3):
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                all_data.extend(response.json())
            else:
                st.error(f"Failed to retrieve data for {country} (page {page})")
                return None

        if all_data:
            return all_data[0]
        else:
            return None

    def plot_chart(df, y_column, title, color):
        y_min = df[y_column].min()
        y_max = df[y_column].max()

        if y_min == y_max:
            y_range = [y_min - 1, y_max + 1]
        else:
            y_range = [y_min - 0.05 * abs(y_min), y_max + 0.05 * abs(y_max)]

        fig = px.bar(df, x='Year', y=y_column,
                     title=title,
                     color_discrete_sequence=[color],
                     height=375)
        fig.update_traces(marker_line_width=0)
        fig.update_layout(
            yaxis=dict(range=y_range),
            plot_bgcolor='#1f1f1f',
            paper_bgcolor='#1f1f1f',
            font=dict(color='white'),
            margin=dict(l=20, r=20, t=60, b=40),
            autosize=True
        )
        return fig
    @st.cache_data(persist="disk")
    def create_data_table(df, y_column):
    # Define the desired width for the Year column
        year_column_width = "350px"  # Adjust this value as needed

        table_html = "<table class='data-table'>"
        # Apply the width to the Year column header
        table_html += f"<tr><th style='width:{year_column_width};'>Year</th>" + "".join([f"<th>{year}</th>" for year in df['Year']]) + "</tr>"
        # Apply the width to each Year column cell
        table_html += f"<tr><td style='width:{year_column_width};'>{y_column}</td>"
        for value in df[y_column]:
            if value is not None:
                table_html += f"<td>{value:.2f}</td>"  # Format as a float with 2 decimal places
            else:
                table_html += "<td>N/A</td>"  # Use "N/A" for None values
        table_html += "</tr></table>"
        return table_html

    # Fetch and display the report
    report = fetch_data_for_country(country)

    if report:
        col1, col2 = st.columns([6, 4])

        with col1:
            st.markdown('<div class="reportColumn">', unsafe_allow_html=True)
            st.markdown(f'<h1 class="reportText">{report.get("Title", "Credit Research Report")}</h1>', unsafe_allow_html=True)
            st.markdown(f'<h2 class="reportText">Country Information</h2>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText"><strong>Country:</strong> {report.get("Country", "N/A")}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText"><strong>Ownership:</strong> {report.get("Ownership", "N/A")}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText"><strong>NFA Rating:</strong> {report.get("NFARating", "N/A")}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText"><strong>ESG Rating:</strong> {report.get("ESGRating", "N/A")}</p>', unsafe_allow_html=True)
            st.markdown(f'<h2 class="reportText">Overview</h2>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText">{report.get("Overview", "No overview available.")}</p>', unsafe_allow_html=True)
            st.markdown(f'<h2 class="reportText">Politics</h2>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText">{report.get("PoliticalNews", "No political news available.")}</p>', unsafe_allow_html=True)
            st.markdown(f'<h2 class="reportText">Strengths</h2>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText">{report.get("Strengths", "No strengths information available.")}</p>', unsafe_allow_html=True)
            st.markdown(f'<h2 class="reportText">Weaknesses</h2>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText">{report.get("Weaknesses", "No weaknesses information available.")}</p>', unsafe_allow_html=True)
            st.markdown(f'<h2 class="reportText">Opportunities</h2>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText">{report.get("Opportunities", "No opportunities information available.")}</p>', unsafe_allow_html=True)
            st.markdown(f'<h2 class="reportText">Threats</h2>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText">{report.get("Threats", "No threats information available.")}</p>', unsafe_allow_html=True)
            st.markdown(f'<h2 class="reportText">Recent News</h2>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText">{report.get("RecentNews", "No recent news available.")}</p>', unsafe_allow_html=True)
            st.markdown(f'<h2 class="reportText">Ratings and Comments from Credit Rating Agencies</h2>', unsafe_allow_html=True)
            st.markdown(f'<h3 class="reportText">Moody\'s:</h3>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText">{report.get("MoodysRating", "N/A")}</p>', unsafe_allow_html=True)
            st.markdown(f'<h3 class="reportText">S&P Global Ratings:</h3>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText">{report.get("SPGlobalRating", "N/A")}</p>', unsafe_allow_html=True)
            st.markdown(f'<h3 class="reportText">Fitch Ratings:</h3>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText">{report.get("FitchRating", "N/A")}</p>', unsafe_allow_html=True)
            st.markdown(f'<h2 class="reportText">Conclusion</h2>', unsafe_allow_html=True)
            st.markdown(f'<p class="reportText">{report.get("Conclusion", "No conclusion available.")}</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="chartColumn">', unsafe_allow_html=True)
            st.header("Economic Data (2024 Onwards)")

            charts_data = [
                ("GDP Growth (%)", [report.get(f'GDPGrowthRateYear{i}', 0) for i in range(1, 7)], color_palette[0]),
                ("Inflation Rate (%)", [report.get(f'InflationYear{i}', 0) for i in range(1, 7)], color_palette[1]),
                ("Unemployment Rate (%)", [report.get(f'UnemploymentRateYear{i}', 0) for i in range(1, 7)], color_palette[2]),
                ("Population (millions)", [report.get(f'PopulationYear{i}', 0) for i in range(1, 7)], color_palette[3]),
                ("Government Budget Balance (% of GDP)", [report.get(f'GovernmentFinancesYear{i}', 0) for i in range(1, 7)], color_palette[4]),
                ("Current Account Balance (% of GDP)", [report.get(f'CurrentAccountBalanceYear{i}', 0) for i in range(1, 7)], color_palette[5])
            ]

            years = [2024, 2025, 2026, 2027, 2028, 2029]

            for metric, values, color in charts_data:
                df = pd.DataFrame({
                    "Year": years,
                    metric: values
                })

                st.plotly_chart(plot_chart(df, metric, metric, color), use_container_width=True)
                st.markdown(create_data_table(df, metric), unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error(f"No report found for {country}.")


