import pandas as pd
import plotly.express as px
import streamlit as st
# from PIL import Image


df = pd.read_csv('Data UNFCCC/data_webapp.csv')

st.set_page_config(page_title="A Web-based Learning Platform for Climate Transition",
                   layout="wide")


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


df_selection = df.query(
    "organizationType==@actor & country==@country & region==@region"
)


# -------------- Main Page --------------
st.title("A Web-based Learning Platform for Climate Transition")
st.write("The following database was compiled from publicly available sources, including the United Nations Framework"
         " Convention on Climate Change (UNFCCC) website. It provides detailed information on various actors—such as"
         " companies, organizations, investors, cities, and regions—and their respective engagements in climate "
         "action.")


st.markdown("##")
left_column, middle_column, right_column = st.columns(3)

current_actor = str(df_selection["organizationType"].unique()).split("[")[1].split("]")[0].split(' ')

new_actor = ''
for idx, actor in enumerate(current_actor):
    if idx == len(current_actor)-1:
        new_actor = new_actor + actor.replace("'", "")
    else:
        new_actor = new_actor + actor.replace("'", "") + ' - '
with left_column:
    st.subheader("Selected Actor(s):")
    st.subheader(new_actor)

unique_countries = df_selection["country"].nunique()
with middle_column:
    st.subheader("Total Selected Countries:")
    st.subheader(f"{unique_countries}")

unique_regions = df_selection["region"].nunique()
with right_column:
    st.subheader("Total Selected Regions:")
    st.subheader(f"{unique_regions}")

st.markdown("---")

# -------------------------------------------------------------------------------

st.markdown("##")

left_column, middle_column, right_column = st.columns([1, 2, 1])

with left_column:
    st.markdown(
        """
        <div style="text-align: center; font-size: 35px; font-weight: bold;">
            Actors
        </div>
        """,
        unsafe_allow_html=True,
    )
    organization_counts = df_selection['organizationType'].value_counts()
    organization_df = organization_counts.reset_index()
    organization_df.columns = ['Type', 'Count']
    fig_organizations = px.pie(
        organization_df,
        names='Type',
        values='Count',
    )
    st.plotly_chart(fig_organizations)

with middle_column:
    st.markdown(
        """
        <div style="text-align: center; font-size: 35px; font-weight: bold;">
            Countries
        </div>
        """,
        unsafe_allow_html=True,
    )
    country_counts = df_selection['country'].value_counts()
    country_df = country_counts.reset_index()
    country_df.columns = ['Type', 'Count']

    country_df.loc[country_df['Count'] < 3000, 'Type'] = 'Other countries'

    fig_countries = px.pie(
        country_df,
        names='Type',
        values='Count',
    )
    st.plotly_chart(fig_countries, key="unique_chart_key")

with right_column:
    st.markdown(
        """
        <div style="text-align: center; font-size: 35px; font-weight: bold;">
            Regions
        </div>
        """,
        unsafe_allow_html=True,
    )
    region_counts = df_selection['region'].value_counts()
    region_df = region_counts.reset_index()
    region_df.columns = ['Type', 'Count']
    fig_regions = px.pie(
        region_df,
        names='Type',
        values='Count',
    )
    st.plotly_chart(fig_regions, key="unique_chart_key_region")


# ------------------------------------------------------
final_df = df_selection.rename(columns={'organizationName': 'Organization Name',
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
                                        'hasClimateActionPlans': 'Climate Action Plans'})
st.dataframe(final_df)
# -------------------------------------------------------------

st.markdown("##")


left_column, middle_column, right_column = st.columns(3)
with middle_column:
    st.image("Logos/NF_HEA_GOVMT_logos.png", width=400)

st.markdown(
    """
    <div style='text-align: center;'>
        This project has been funded by the <a href="https://www.ucd.ie/teaching/awardsgrantsfellowships/satlefunding/"
         target="_blank"> Strategic Alignment of Teaching and Learning Enhancement</a> funding administered by the
          National Forum for the Enhancement of Teaching and Learning in Higher Education, in partnership with the
           Higher Education Authority.
    </div>
    """,
    unsafe_allow_html=True
)


# ------ Hide Streamlit Style ------
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)