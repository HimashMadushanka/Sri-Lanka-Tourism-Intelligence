import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
# Sidebar: Filter Controls
# ---------------------------------------------------------
st.sidebar.header("🎯 Filter Controls")

# Reset Button
if st.sidebar.button("🔄 Reset All Filters", use_container_width=True):
    for key in ["f_years", "f_continent", "f_period", "f_season"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

# 1. Year Range Filter
all_years = sorted(df["Year"].unique().tolist())
selected_years = st.sidebar.slider(
    "1. Year Range",
    min_value=min(all_years),
    max_value=max(all_years),
    value=(min(all_years), max(all_years)),
    key="f_years"
)

# 2. Continent / Region Filter
continents = ["All Continents"] + sorted([c for c in df["Continent"].dropna().unique().tolist() if c not in ["Other", "Antarctica"]])
selected_continent = st.sidebar.selectbox(
    "2. Continent / Region",
    continents,
    key="f_continent"
)

# 3. Economic Phase Filter
periods = ["All Periods", "Pre-Crisis (2018-2019)", "Crisis (2020-2021)", "Post-Crisis (2022-2025)"]
selected_period = st.sidebar.selectbox(
    "3. Economic Phase",
    periods,
    key="f_period"
)

# 4. Tourism Season Filter
seasons = ["All Seasons", "Peak Season (Nov–Apr & Jul–Aug)", "Off-Peak Season (May–Jun & Sep–Oct)"]
selected_season = st.sidebar.selectbox(
    "4. Tourism Season",
    seasons,
    key="f_season"
)

# ---------------------------------------------------------
# Apply Filters
# ---------------------------------------------------------
filtered = df.copy()

# 1. Year Filter
filtered = filtered[(filtered["Year"] >= selected_years[0]) & (filtered["Year"] <= selected_years[1])]

# 2. Continent Filter
if selected_continent != "All Continents":
    filtered = filtered[filtered["Continent"] == selected_continent]

# 3. Economic Phase Filter
if selected_period != "All Periods":
    filtered = filtered[filtered["Period"] == selected_period]

# 4. Season Filter
if selected_season == "Peak Season (Nov–Apr & Jul–Aug)":
    filtered = filtered[filtered["Season"] == "Peak"]
elif selected_season == "Off-Peak Season (May–Jun & Sep–Oct)":
    filtered = filtered[filtered["Season"] == "Off-Peak"]

# Fallback if no records match
if len(filtered) == 0:
    st.warning("⚠️ No tourist arrivals match this combination of filters. Please adjust your filters or click 'Reset All Filters'.")
    st.stop()

# ---------------------------------------------------------
# Title & 4 Core Executive Metrics
# ---------------------------------------------------------
st.title("🌴 Sri Lanka Tourism Analytics")
st.caption("Official Sri Lanka Tourism Development Authority (SLTDA) Records &bull; 2018–2025")

total_arrivals = filtered["Tourist_Arrivals"].sum()
top_country = filtered.groupby("Country")["Tourist_Arrivals"].sum().idxmax()
top_country_val = filtered.groupby("Country")["Tourist_Arrivals"].sum().max()
top_country_pct = (top_country_val / max(1, total_arrivals)) * 100
peak_month = filtered.groupby("Month")["Tourist_Arrivals"].sum().idxmax()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Tourist Arrivals", f"{total_arrivals/1e6:.2f}M" if total_arrivals >= 1e6 else f"{total_arrivals:,.0f}")
col2.metric("Top Source Country", top_country, f"{top_country_pct:.1f}% share")
col3.metric("Busiest Month", peak_month)
col4.metric("Active Countries", f"{filtered['Country'].nunique()}")

st.markdown("---")

# ---------------------------------------------------------
# Row 1: Macro Trend & Recovery Dynamics (2 Columns)
# ---------------------------------------------------------
st.markdown("### 📈 1. Macro Trend & Growth Dynamics")
col_trend, col_yoy = st.columns(2)

yearly_totals = filtered.groupby("Year")["Tourist_Arrivals"].sum().reset_index()

with col_trend:
    st.subheader("Annual Tourist Arrivals")
    fig_annual = px.line(
        yearly_totals,
        x="Year",
        y="Tourist_Arrivals",
        markers=True,
        labels={"Tourist_Arrivals": "Arrivals", "Year": "Year"}
    )
    fig_annual.update_traces(
        line_color="#0284c7",
        line_width=3,
        marker=dict(size=8, color="#0369a1")
    )
    fig_annual.update_layout(
        yaxis_tickformat=",.0f",
        hovermode="x unified",
        margin=dict(l=10, r=10, t=10, b=10)
    )
    st.plotly_chart(fig_annual, use_container_width=True)

with col_yoy:
    if len(yearly_totals) > 1:
        st.subheader("Year-over-Year (YoY) Growth Rate (%)")
        yearly_totals["YoY_Growth"] = yearly_totals["Tourist_Arrivals"].pct_change() * 100
        yoy_data = yearly_totals.dropna(subset=["YoY_Growth"]).copy()
        yoy_data["Color"] = yoy_data["YoY_Growth"].apply(lambda x: "#10b981" if x >= 0 else "#ef4444")
        
        fig_yoy = go.Figure(go.Bar(
            x=yoy_data["Year"],
            y=yoy_data["YoY_Growth"],
            marker_color=yoy_data["Color"],
            text=yoy_data["YoY_Growth"].apply(lambda x: f"{x:+.1f}%"),
            textposition="outside"
        ))
        fig_yoy.update_layout(
            yaxis_ticksuffix="%",
            hovermode="x unified",
            margin=dict(l=10, r=10, t=25, b=10)
        )
        st.plotly_chart(fig_yoy, use_container_width=True)
    else:
        st.subheader(f"Quarterly Performance ({selected_years[0]})")
        q_order = ["Q1", "Q2", "Q3", "Q4"]
        q_totals = filtered.groupby("Quarter")["Tourist_Arrivals"].sum().reindex(q_order).fillna(0).reset_index()
        fig_quarter = px.bar(
            q_totals,
            x="Quarter",
            y="Tourist_Arrivals",
            text=q_totals["Tourist_Arrivals"].apply(lambda x: f"{x:,.0f}"),
            color_discrete_sequence=["#0284c7"],
            labels={"Tourist_Arrivals": "Arrivals", "Quarter": "Quarter"}
        )
        fig_quarter.update_traces(textposition="outside")
        fig_quarter.update_layout(
            yaxis_tickformat=",.0f",
            margin=dict(l=10, r=10, t=25, b=10)
        )
        st.plotly_chart(fig_quarter, use_container_width=True)

st.markdown("---")

# ---------------------------------------------------------
# Row 2: Geographic & Market Structure (2 Columns)
# ---------------------------------------------------------
st.markdown("### 🌍 2. Geographic & Market Structure")
col_markets, col_share = st.columns([6, 4])

with col_markets:
    top_n = min(10, filtered["Country"].nunique())
    st.subheader(f"Top {top_n} Source Countries")
    top10 = (
        filtered.groupby("Country")["Tourist_Arrivals"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )
    fig_top = px.bar(
        top10,
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
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False
    )
    st.plotly_chart(fig_top, use_container_width=True)

with col_share:
    if selected_continent == "All Continents":
        st.subheader("Market Share by Continent")
        cont_data = (
            filtered.groupby("Continent")["Tourist_Arrivals"]
            .sum()
            .reset_index()
            .sort_values("Tourist_Arrivals", ascending=False)
        )
        fig_share = px.pie(
            cont_data,
            names="Continent",
            values="Tourist_Arrivals",
            hole=0.55,
            color_discrete_sequence=px.colors.qualitative.Safe
        )
    else:
        st.subheader(f"Top Markets in {selected_continent}")
        top_cont_countries = (
            filtered.groupby("Country")["Tourist_Arrivals"]
            .sum()
            .sort_values(ascending=False)
            .head(5)
            .reset_index()
        )
        fig_share = px.pie(
            top_cont_countries,
            names="Country",
            values="Tourist_Arrivals",
            hole=0.55,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
    fig_share.update_traces(textposition="inside", textinfo="percent+label")
    fig_share.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False
    )
    st.plotly_chart(fig_share, use_container_width=True)

st.markdown("---")

# ---------------------------------------------------------
# Row 3: Seasonal Demand Dynamics (Full Width)
# ---------------------------------------------------------
st.markdown("### 🗓️ 3. Seasonal Demand Dynamics")
st.subheader("Monthly Seasonality (Peak vs. Off-Peak Cycle)")

month_order = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]
monthly_data = (
    filtered.groupby(["Month_Number", "Month", "Season"])["Tourist_Arrivals"]
    .sum()
    .reset_index()
    .sort_values("Month_Number")
)
fig_monthly = px.bar(
    monthly_data,
    x="Month",
    y="Tourist_Arrivals",
    color="Season",
    color_discrete_map={"Peak": "#0284c7", "Off-Peak": "#94a3b8"},
    text=monthly_data["Tourist_Arrivals"].apply(lambda x: f"{x/1e3:,.0f}k" if x >= 1000 else f"{x:.0f}"),
    labels={"Tourist_Arrivals": "Arrivals", "Month": "Month", "Season": "Season"}
)
fig_monthly.update_traces(textposition="outside")
fig_monthly.update_layout(
    xaxis=dict(categoryorder="array", categoryarray=month_order),
    yaxis_tickformat=",.0f",
    margin=dict(l=10, r=10, t=10, b=10),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)
st.plotly_chart(fig_monthly, use_container_width=True)

# ---------------------------------------------------------
# Optional Clean Data Inspection & Export
# ---------------------------------------------------------
with st.expander("📋 View Filtered Data Table & Export", expanded=False):
    st.dataframe(
        filtered[["Year", "Month", "Country", "Continent", "Quarter", "Season", "Period", "Tourist_Arrivals"]],
        use_container_width=True,
        hide_index=True
    )
    csv_data = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv_data,
        file_name="sri_lanka_tourism_filtered.csv",
        mime="text/csv"
    )

# ---------------------------------------------------------
# Clean Footer
# ---------------------------------------------------------
st.markdown("---")
st.caption(f"Showing **{filtered['Country'].nunique()} countries** across **{filtered['Date'].nunique()} monthly data points** &bull; Official SLTDA Records (2018–2025)")
