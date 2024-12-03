"""
SATLE Web Application
======================

Author: Sergio Garcia-Vega, Ph.D., University College Dublin, Republic of Ireland

This script provides a Streamlit web application for visualizing and analyzing climate transition data.

HOW TO RUN:
-----------
1. Ensure you have Python 3.7 or later installed.
2. Install the required dependencies by running:
   pip install streamlit pandas plotly
3. Place the dataset (`data_webapp.csv`) and logo image (`NF_HEA_GOVMT_logos.png`)
   in the respective folders: `Data UNFCCC/` and `Logos/`.
4. Run the application using the command:
   streamlit run satle_webapp.py
5. Open the URL provided in the terminal (e.g., http://localhost:8501) in your browser.

File Structure:
---------------
Project Directory
│
├── satle_webapp.py                # This script
├── Data UNFCCC/                   # Folder containing the dataset
│   └── data_webapp.csv
├── Logos/                         # Folder containing logo images
│   └── NF_HEA_GOVMT_logos.png
├── .streamlit/                    # Hidden folder for Streamlit configuration
│   └── config.toml                # Configuration file for Streamlit
"""

# Import required libraries
import pandas as pd
import plotly.express as px
import streamlit as st


def load_data(file_path):
    """
    Load data from the given CSV file path.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        DataFrame: Loaded data as a pandas DataFrame.
    """
    return pd.read_csv(file_path)


def configure_page():
    """
    Configure the Streamlit page settings.
    """
    st.set_page_config(
        page_title="A Web-based Learning Platform for Climate Transition",
        layout="wide"
    )


def create_sidebar_filters(df):
    """
    Create sidebar filters for the application.

    Args:
        df (DataFrame): The dataset.

    Returns:
        DataFrame: Filtered dataset based on user selections.
    """
    st.sidebar.header("Searching Criteria")

    actor = st.sidebar.multiselect(
        "Actor:",
        options=df["organizationType"].unique(),
        default=df["organizationType"].unique()
    )
    country = st.sidebar.multiselect(
        "Country:",
        options=df["country"].unique(),
        default=df["country"].unique()
    )
    region = st.sidebar.multiselect(
        "Region:",
        options=df["region"].unique(),
        default=df["region"].unique()
    )

    return df.query(
        "organizationType == @actor & country == @country & region == @region"
    )


def display_main_page_info():
    """
    Display the main page information.
    """
    st.title("A Web-based Learning Platform for Climate Transition")
    st.write(
        "The following database was compiled from publicly available sources, "
        "including the United Nations Framework Convention on Climate Change (UNFCCC) website. "
        "It provides detailed information on various actors—such as companies, organizations, investors, cities, "
        "and regions—and their respective engagements in climate action."
    )
    st.markdown("---")


def display_summary_statistics(df_selection):
    """
    Display summary statistics about the selected dataset.

    Args:
        df_selection (DataFrame): Filtered dataset.
    """
    left_column, middle_column, right_column = st.columns(3)

    # Selected Actor(s)
    current_actor = str(df_selection["organizationType"].unique()).split("[")[1].split("]")[0].split(' ')
    new_actor = ' - '.join(actor.replace("'", "") for actor in current_actor)
    with left_column:
        st.subheader("Selected Actor(s):")
        st.subheader(new_actor)

    # Total Selected Countries
    unique_countries = df_selection["country"].nunique()
    with middle_column:
        st.subheader("Total Selected Countries:")
        st.subheader(f"{unique_countries}")

    # Total Selected Regions
    unique_regions = df_selection["region"].nunique()
    with right_column:
        st.subheader("Total Selected Regions:")
        st.subheader(f"{unique_regions}")

    st.markdown("---")


def create_pie_charts(df_selection):
    """
    Create pie charts for actors, countries, and regions.

    Args:
        df_selection (DataFrame): Filtered dataset.
    """
    left_column, middle_column, right_column = st.columns([1, 2, 1])

    # Actors
    with left_column:
        st.markdown(
            "<div style='text-align: center; font-size: 35px; font-weight: bold;'>Actors</div>",
            unsafe_allow_html=True,
        )
        organization_counts = df_selection['organizationType'].value_counts()
        organization_df = organization_counts.reset_index()
        organization_df.columns = ['Type', 'Count']
        fig_organizations = px.pie(organization_df, names='Type', values='Count')
        st.plotly_chart(fig_organizations)

    # Countries
    with middle_column:
        st.markdown(
            "<div style='text-align: center; font-size: 35px; font-weight: bold;'>Countries</div>",
            unsafe_allow_html=True,
        )
        country_counts = df_selection['country'].value_counts()
        country_df = country_counts.reset_index()
        country_df.columns = ['Type', 'Count']
        country_df.loc[country_df['Count'] < 3000, 'Type'] = 'Other countries'
        fig_countries = px.pie(country_df, names='Type', values='Count')
        st.plotly_chart(fig_countries, key="unique_chart_key")

    # Regions
    with right_column:
        st.markdown(
            "<div style='text-align: center; font-size: 35px; font-weight: bold;'>Regions</div>",
            unsafe_allow_html=True,
        )
        region_counts = df_selection['region'].value_counts()
        region_df = region_counts.reset_index()
        region_df.columns = ['Type', 'Count']
        fig_regions = px.pie(region_df, names='Type', values='Count')
        st.plotly_chart(fig_regions, key="unique_chart_key_region")


def display_final_table(df_selection):
    """
    Display the final table with selected dataset.

    Args:
        df_selection (DataFrame): Filtered dataset.
    """
    final_df = df_selection.rename(columns={
        'organizationName': 'Organization Name',
        'organizationType': 'Actor',
        'country': 'Country',
        'region': 'Region',
        'dateactor': 'Date',
        'actorProperties_businessActivity': 'Business Activity',
        'hasCommitments': 'Commitments',
        'hasInitiativeParticipations': 'Initiative Participations',
        'hasActionsUndertaken': 'Actions Undertaken',
        'hasMitigations': 'Mitigations',
        'hasAdaptations': 'Adaptations',
        'hasRiskAssessments': 'Risk Assessments',
        'hasClimateActionPlans': 'Climate Action Plans'
    })
    st.dataframe(final_df)


def display_logo():
    """
    Display the logo and funding information at the bottom of the app.
    """
    left_column, middle_column, right_column = st.columns(3)
    with middle_column:
        st.image("Logos/NF_HEA_GOVMT_logos.png", width=400)

    st.markdown(
        """
        <div style='text-align: center;'>
            This project has been funded by the 
            <a href="https://www.ucd.ie/teaching/awardsgrantsfellowships/satlefunding/" target="_blank">
            Strategic Alignment of Teaching and Learning Enhancement</a> funding administered by the
            National Forum for the Enhancement of Teaching and Learning in Higher Education, in partnership with the
            Higher Education Authority.
        </div>
        """,
        unsafe_allow_html=True
    )


def hide_streamlit_style():
    """
    Hide Streamlit's default style elements (header, footer, and menu).
    """
    hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)


def main():
    """
    Main function to run the SATLE Web Application.
    """
    configure_page()

    # Load dataset
    df = load_data('Data UNFCCC/data_webapp.csv')

    # Sidebar filters
    df_selection = create_sidebar_filters(df)

    # Main page content
    display_main_page_info()
    display_summary_statistics(df_selection)
    create_pie_charts(df_selection)
    display_final_table(df_selection)
    display_logo()

    # Hide Streamlit style
    hide_streamlit_style()


# Run the main function
if __name__ == "__main__":
    main()
