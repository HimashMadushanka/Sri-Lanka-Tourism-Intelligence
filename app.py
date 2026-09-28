import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Sri Lanka Tourism Analytics",
    page_icon="🌴",
    layout="wide"
)

# ---------------------------------------------------------
# Load Data
# ---------------------------------------------------------
@st.cache_data
def load_data():
    file_path = Path("data/processed/tourism_arrivals_clean.csv")
    if not file_path.exists():
        st.error(f"File not found: {file_path}")
        st.stop()
    df = pd.read_csv(file_path)
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

# ---------------------------------------------------------
# Sidebar: Rich Filters to Explore & Get Ideas
# ---------------------------------------------------------
st.sidebar.header("🎯 Filters & Controls")
st.sidebar.caption("Change filters to discover new ideas & patterns")

# 1. Year Range Filter
all_years = sorted(df["Year"].unique().tolist())
selected_years = st.sidebar.slider(
    "1. Select Year Range",
    min_value=min(all_years),
    max_value=max(all_years),
    value=(min(all_years), max(all_years))
)

# 2. Continent Filter
continents = ["All Continents"] + sorted([c for c in df["Continent"].dropna().unique().tolist() if c not in ["Other", "Antarctica"]])
selected_continent = st.sidebar.selectbox("2. Select Continent / Region", continents)

# 3. Macroeconomic Period Filter
periods = ["All Periods", "Pre-Crisis (2018-2019)", "Crisis (2020-2021)", "Post-Crisis (2022-2025)"]
selected_period = st.sidebar.selectbox("3. Select Economic Phase", periods)

# 4. Season Filter
seasons = ["All Seasons", "Peak Season (Nov–Apr & Jul–Aug)", "Off-Peak Season (May–Jun & Sep–Oct)"]
selected_season = st.sidebar.selectbox("4. Select Tourism Season", seasons)

# ---------------------------------------------------------
# Apply Filters
# ---------------------------------------------------------
filtered = df.copy()

# Year filter
filtered = filtered[(filtered["Year"] >= selected_years[0]) & (filtered["Year"] <= selected_years[1])]

# Continent filter
if selected_continent != "All Continents":
    filtered = filtered[filtered["Continent"] == selected_continent]

# Period filter
if selected_period != "All Periods":
    filtered = filtered[filtered["Period"] == selected_period]

# Season filter
if selected_season == "Peak Season (Nov–Apr & Jul–Aug)":
    filtered = filtered[filtered["Season"] == "Peak"]
elif selected_season == "Off-Peak Season (May–Jun & Sep–Oct)":
    filtered = filtered[filtered["Season"] == "Off-Peak"]

# Fallback if no records match
if len(filtered) == 0:
    st.warning("⚠️ No tourist arrivals found for the selected combination of filters. Please adjust your filters.")
    st.stop()

# ---------------------------------------------------------
# Header & 4 Key Numbers
# ---------------------------------------------------------
st.title("🌴 Sri Lanka Tourism Intelligence Dashboard")

total_arrivals = filtered["Tourist_Arrivals"].sum()
yearly_totals = filtered.groupby("Year")["Tourist_Arrivals"].sum().reset_index()

# Peak year in filter
peak_year_row = yearly_totals.loc[yearly_totals["Tourist_Arrivals"].idxmax()]

# Top country in filter
top_countries_series = filtered.groupby("Country")["Tourist_Arrivals"].sum()
top_country_name = top_countries_series.idxmax()
top_country_val = top_countries_series.max()
top_country_pct = (top_country_val / max(1, total_arrivals)) * 100

# Peak month in filter
monthly_totals = filtered.groupby("Month")["Tourist_Arrivals"].sum()
peak_month_name = monthly_totals.idxmax()

# 4 KPI Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Tourist Arrivals", f"{total_arrivals/1e6:.2f}M" if total_arrivals >= 1e6 else f"{total_arrivals:,.0f}")
col2.metric("Highest Year in Filter", f"{int(peak_year_row['Year'])}", f"{peak_year_row['Tourist_Arrivals']:,.0f} arrivals")
col3.metric("Top Source Market", top_country_name, f"{top_country_pct:.1f}% share")
col4.metric("Busiest Month", peak_month_name, f"{monthly_totals.max():,.0f} arrivals")

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 💡 Dynamic "Instant Idea from Selected Filters" Box
# ---------------------------------------------------------
idea_text = []

# Idea based on continent
if selected_continent == "Europe":
    idea_text.append("✈️ **European Market Insight:** European tourists heavily concentrate in **December, January, and February** to escape the European winter, with the UK and Germany leading demand.")
elif selected_continent == "Asia":
    idea_text.append("✈️ **Asian Market Insight:** Asian travel is heavily driven by **India and China**, showing strong year-round arrivals and an additional peak during the **August Kandy Esala Perahera festival**.")
elif selected_continent == "America":
    idea_text.append("✈️ **American Market Insight:** The US and Canada represent high-spending, long-haul travelers with steady arrivals peaking from December through March.")

# Idea based on period
if selected_period == "Crisis (2020-2021)":
    idea_text.append("📉 **Crisis Insight:** Arrivals plummeted to just **194k in 2021**. India and Russia were the first markets to restart flights via regional air bubbles.")
elif selected_period == "Post-Crisis (2022-2025)":
    idea_text.append("🚀 **Recovery Insight:** Post-crisis growth skyrocketed, surging from **720k in 2022 to an all-time record 2.36 Million in 2025** (+227% expansion).")

# Idea based on season
if selected_season == "Peak Season (Nov–Apr & Jul–Aug)":
    idea_text.append("☀️ **Seasonality Insight:** Peak season accounts for the vast majority of hospitality foreign exchange earnings. Hotels should maximize room rates (ADR).")
elif selected_season == "Off-Peak Season (May–Jun & Sep–Oct)":
    idea_text.append("🌧️ **Off-Peak Insight:** May and June are the quietest monsoon months. Resorts offer domestic staycation rates and MICE (conventions) to sustain revenue.")

# Default general idea if no specific filter
if len(idea_text) == 0:
    idea_text.append(f"💡 **Key Market Idea:** In this view, **{top_country_name}** is the #1 source market generating **{top_country_pct:.1f}%** of total arrivals. The single busiest month is **{peak_month_name}**.")

# Display Key Idea box
st.info("\n\n".join(idea_text))

st.markdown("---")

# ---------------------------------------------------------
# Visualizations: 3 Clear, Direct Charts
# ---------------------------------------------------------
c_left, c_right = st.columns([6, 4])

with c_left:
    st.subheader("1. Annual Trend (Filtered View)")
    fig_annual = px.area(
        yearly_totals,
        x="Year",
        y="Tourist_Arrivals",
        markers=True,
        labels={"Tourist_Arrivals": "Tourist Arrivals", "Year": "Year"},
        color_discrete_sequence=["#0284c7"]
    )
    fig_annual.update_layout(yaxis_tickformat=",.0f", hovermode="x unified", margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_annual, use_container_width=True)

with c_right:
    st.subheader("2. Top Source Countries")
    top_n = min(8, filtered["Country"].nunique())
    top_chart_data = (
        filtered.groupby("Country")["Tourist_Arrivals"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )
    fig_top = px.bar(
        top_chart_data,
        x="Tourist_Arrivals",
        y="Country",
        orientation="h",
        color="Tourist_Arrivals",
        color_continuous_scale="Blues",
        labels={"Tourist_Arrivals": "Arrivals", "Country": "Country"}
    )
    fig_top.update_layout(
        yaxis=dict(autorange="reversed"),
        xaxis_tickformat=",.0f",
        margin=dict(l=10, r=10, t=10, b=10)
    )
    st.plotly_chart(fig_top, use_container_width=True)

st.markdown("---")

# Row 2: Monthly Seasonality Curve
st.subheader("3. Monthly Seasonality (When Do They Visit?)")
month_order = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]
monthly_chart_data = (
    filtered.groupby(["Month_Number", "Month"])["Tourist_Arrivals"]
    .sum()
    .reset_index()
    .sort_values("Month_Number")
)

fig_monthly = px.bar(
    monthly_chart_data,
    x="Month",
    y="Tourist_Arrivals",
    text=monthly_chart_data["Tourist_Arrivals"].apply(lambda x: f"{x/1e3:,.0f}k" if x >= 1000 else f"{x:.0f}"),
    color="Tourist_Arrivals",
    color_continuous_scale="Teal",
    labels={"Tourist_Arrivals": "Total Arrivals", "Month": "Month"}
)
fig_monthly.update_traces(textposition="outside")
fig_monthly.update_layout(
    xaxis=dict(categoryorder="array", categoryarray=month_order),
    yaxis_tickformat=",.0f",
    margin=dict(l=10, r=10, t=10, b=10)
)
st.plotly_chart(fig_monthly, use_container_width=True)

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown("---")
st.caption(f"Showing **{filtered['Country'].nunique()} countries** across **{filtered['Date'].nunique()} months** &bull; Data Source: Official SLTDA Records &bull; Sri Lanka Tourism Analytics")
