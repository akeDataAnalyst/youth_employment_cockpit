# streamlit_dashboard/main.py

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title="Youth Employment Cockpit",
    layout="wide",
    page_icon="🌍",
    initial_sidebar_state="expanded"
)

# ====================== HEADER ======================
st.title("🌍 Pan-African Youth Employment Cockpit")
st.markdown("**Mastercard Foundation** — Young Africa Works Strategy")
st.caption("Enterprise Performance Reporting & Strategic Insights")

st.divider()

# ====================== LOAD DATA ======================
@st.cache_data
def load_data():
    scorecard = pd.read_csv('leadership_scorecard.csv')
    driver = pd.read_csv('driver_analysis.csv')
    return scorecard, driver

scorecard, driver = load_data()

# ====================== SIDEBAR ======================
st.sidebar.header("Filters")
selected_countries = st.sidebar.multiselect(
    "Select Countries", 
    options=scorecard['country_name'].unique(), 
    default=scorecard['country_name'].unique()
)

selected_sectors = st.sidebar.multiselect(
    "Select Sectors", 
    options=driver['sector_name'].unique(), 
    default=driver['sector_name'].unique()
)

st.sidebar.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# ====================== KEY METRICS ======================
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Total Youth Reached", f"{scorecard['total_youth'].sum():,}")
with c2:
    st.metric("Placement Rate", f"{scorecard['overall_placement_rate'].mean():.1%}")
with c3:
    st.metric("6-Month Retention", f"{scorecard['retention_rate'].mean():.1%}")
with c4:
    st.metric("Avg Monthly Income", f"${scorecard['avg_monthly_income'].mean():.0f}")

st.divider()

# ====================== MAIN TABS ======================
tab1, tab2, tab3, tab4 = st.tabs([
    "Executive Scorecard", 
    "Sector Performance", 
    "Strategic Insights", 
    "Data Quality"
])

with tab1:
    st.subheader("Leadership Executive Scorecard")
    filtered_score = scorecard[scorecard['country_name'].isin(selected_countries)]
    st.dataframe(filtered_score.round(3), use_container_width=True)

with tab2:
    st.subheader("Sector Performance")
    filtered_driver = driver[
        (driver['country_name'].isin(selected_countries)) & 
        (driver['sector_name'].isin(selected_sectors))
    ]

    fig = px.bar(
        filtered_driver, 
        x='country_name', 
        y='placement_rate', 
        color='sector_name', 
        barmode='group',
        title="Placement Rate by Country and Sector"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Additional metrics table
    st.dataframe(filtered_driver.round(3), use_container_width=True)

with tab3:
    st.subheader("Strategic Insights & Recommendations")

    col_a, col_b = st.columns([2, 1])

    with col_a:
        # Top performers
        top_performers = driver.nlargest(5, 'placement_rate')
        st.markdown("**Top 5 Performing Sector-Country Combinations**")
        st.dataframe(top_performers[['sector_name', 'country_name', 'placement_rate', 'avg_income']].round(3), 
                     use_container_width=True)

    with col_b:
        st.markdown("**Key Insights**")
        top = driver.loc[driver['placement_rate'].idxmax()]
        st.success(f"**{top['sector_name']} in {top['country_name']}** leads with **{top['placement_rate']:.1%}** placement rate")

        st.markdown("**Strategic Recommendations**")
        st.markdown("""
        - **Scale up** Green Jobs and Digital Skills programs in Nigeria and Kenya  
        - **Strengthen** post-placement support in Agribusiness to improve retention  
        - **Maintain** strong gender lens — female participation remains solid (66-70%)
        """)

with tab4:
    st.subheader("Data Quality & Governance")
    col_c, col_d = st.columns(2)

    with col_c:
        st.metric("Data Quality Score", "94.2%", "↑ 2.1%")
        st.metric("Total Exceptions", "248")

    with col_d:
        st.warning("**High Priority**: Missing income data for some placed participants")
        st.info("**Next Step**: Collaborate with program partners to improve data completeness")

st.divider()
st.caption("**Developed by Aklilu Abera** | Data Analyst")
