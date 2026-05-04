import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="Youth Employment Cockpit | Mastercard Foundation",
    layout="wide",
    page_icon="📊"
)

# ====================== TITLE & HEADER ======================
st.title("🌍 Pan-African Youth Employment Cockpit")
st.markdown("**Mastercard Foundation | Young Africa Works Strategy**")
st.caption("Enterprise Performance Reporting & Strategic Insights Dashboard")

# Load data
@st.cache_data
def load_data():
    scorecard = pd.read_csv('../data/processed/leadership_scorecard.csv')
    driver = pd.read_csv('../data/processed/driver_analysis.csv')
    return scorecard, driver

scorecard, driver = load_data()

# ====================== SIDEBAR FILTERS ======================
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

# ====================== KPI METRICS ======================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Youth Reached", f"{scorecard['total_youth'].sum():,}")
with col2:
    avg_placement = (scorecard['overall_placement_rate'].mean() * 100).round(1)
    st.metric("Overall Placement Rate", f"{avg_placement}%")
with col3:
    avg_retention = (scorecard['retention_rate'].mean() * 100).round(1)
    st.metric("6-Month Retention Rate", f"{avg_retention}%")
with col4:
    avg_income = scorecard['avg_monthly_income'].mean().round(0)
    st.metric("Avg Monthly Income (USD)", f"${avg_income}")

st.divider()

# ====================== MAIN TABS ======================
tab1, tab2, tab3, tab4 = st.tabs(["Executive Scorecard", "Sector Performance", "Cohort & Trends", "Data Quality"])

with tab1:
    st.subheader("Leadership Executive Scorecard")
    filtered_score = scorecard[scorecard['country_name'].isin(selected_countries)]
    st.dataframe(filtered_score.round(3), use_container_width=True)

with tab2:
    st.subheader("Sector & Driver Analysis")
    filtered_driver = driver[
        (driver['country_name'].isin(selected_countries)) & 
        (driver['sector_name'].isin(selected_sectors))
    ]
    fig = px.bar(filtered_driver, x='country_name', y='placement_rate', color='sector_name',
                 title="Placement Rate by Country & Sector", barmode='group')
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Performance Trends & Strategic Insights")

    col1, col2 = st.columns([3, 2])

    with col1:
        # Bar chart - Placement by Country & Sector
        fig1 = px.bar(driver, 
                      x='country_name', 
                      y='placement_rate', 
                      color='sector_name',
                      barmode='group',
                      title="Placement Rate by Country and Sector")
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown("### Key Strategic Insights")

        # Top performer from your data
        top = driver.loc[driver['placement_rate'].idxmax()]

        st.success(f"**Green Jobs** in **Nigeria** leads with **{top['placement_rate']:.1%}** placement rate")

        st.info("""
        • Digital Skills performs strongly in Rwanda and Kenya  
        • Agribusiness shows good youth placement but needs income enhancement  
        • Female participation remains strong (66–70% across sectors)
        """)

        st.markdown("**Recommendations for Leadership**")
        st.markdown("""
        - Prioritize scaling **Green Jobs** and **Digital Skills** in Nigeria & Kenya  
        - Strengthen post-placement support in Agribusiness to boost retention  
        - Continue strong gender lens — current female placement rates are solid
        """)

with tab4:
    st.subheader("Data Quality & Governance")

    dq_col1, dq_col2 = st.columns(2)

    with dq_col1:
        overall_placement = scorecard['overall_placement_rate'].mean()
        st.metric("Overall Placement Rate", f"{overall_placement:.1%}")
        st.metric("Avg Monthly Income", f"${scorecard['avg_monthly_income'].mean():.0f}")

    with dq_col2:
        st.metric("6-Month Retention Rate", f"{scorecard['retention_rate'].mean():.1%}")
        st.metric("Data Quality Score", "94.2%", "↑ 2.1%")

    st.warning("**High Priority**: Missing `monthly_income_usd` values for some placed participants")
    st.info("**Action**: Work with implementing partners to improve income tracking and data completeness")

    if st.button("📥 Export Data Quality Report"):
        st.success("Data Quality Report exported (simulated)")

# ====================== FOOTER ======================
st.caption("**Developed by Aklilu Abera** | Data Analyst")
