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
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Custom Styling (Modern Executive Design System)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Sleek Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }
    
    /* Metric Card Polish */
    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.03);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.06);
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.80rem !important;
        font-weight: 700 !important;
        color: #64748b !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.80rem !important;
        font-weight: 800 !important;
        color: #0f172a !important;
    }
    
    /* Section Headings */
    .section-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #0f172a;
        margin-top: 10px;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .section-subtitle {
        font-size: 0.85rem;
        color: #64748b;
        margin-bottom: 14px;
    }
    
    /* Badges */
    .filter-chip {
        display: inline-block;
        background: #e0f2fe;
        color: #0369a1;
        font-weight: 600;
        font-size: 0.78rem;
        padding: 4px 10px;
        border-radius: 20px;
        margin-right: 6px;
        margin-bottom: 6px;
        border: 1px solid #bae6fd;
    }
</style>
""", unsafe_allow_html=True)

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
st.sidebar.markdown("## 🎯 Filter Controls")

# Reset Button
if st.sidebar.button("🔄 Reset All Filters", use_container_width=True):
    for key in ["f_years", "f_continent", "f_period", "f_season"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

st.sidebar.markdown("---")

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
# Executive Header Banner
# ---------------------------------------------------------
st.title("🌴 Sri Lanka Tourism Analytics")
st.markdown(
    "**Executive Decision-Support Portal** &bull; Official Sri Lanka Tourism Development Authority (SLTDA) Data (2018–2025)"
)

# Active Filter Chips
chips_html = f"""
<div style="margin-bottom: 18px;">
    <span class="filter-chip">📅 Years: {selected_years[0]}–{selected_years[1]}</span>
    <span class="filter-chip">🌍 Region: {selected_continent}</span>
    <span class="filter-chip">⚡ Phase: {selected_period}</span>
    <span class="filter-chip">☀️ Season: {selected_season.split(' (')[0]}</span>
</div>
"""
st.markdown(chips_html, unsafe_allow_html=True)

# ---------------------------------------------------------
# Top 4 KPI Metrics
# ---------------------------------------------------------
total_arrivals = filtered["Tourist_Arrivals"].sum()
top_country = filtered.groupby("Country")["Tourist_Arrivals"].sum().idxmax()
top_country_val = filtered.groupby("Country")["Tourist_Arrivals"].sum().max()
top_country_pct = (top_country_val / max(1, total_arrivals)) * 100
peak_month = filtered.groupby("Month")["Tourist_Arrivals"].sum().idxmax()

col1, col2, col3, col4 = st.columns(4)
col1.metric(
    "Total Tourist Arrivals",
    f"{total_arrivals/1e6:.2f}M" if total_arrivals >= 1e6 else f"{total_arrivals:,.0f}",
    help="Total tourist arrivals for the selected filters"
)
col2.metric(
    "Top Source Market",
    top_country,
    f"{top_country_pct:.1f}% share",
    help=f"{top_country} accounts for {top_country_pct:.1f}% of total selected arrivals"
)
col3.metric(
    "Busiest Month",
    peak_month,
    help="Month with the highest cumulative tourist arrival volume"
)
col4.metric(
    "Active Feeder Markets",
    f"{filtered['Country'].nunique()} Countries",
    help="Number of distinct source countries contributing to this selection"
)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Section 1: Macro Volume Trajectory & Recovery (2 Columns)
# ---------------------------------------------------------
st.markdown('<div class="section-title">📈 1. Macro Trend & Growth Dynamics</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Annual volume progression and year-over-year shock/recovery trajectories</div>', unsafe_allow_html=True)

yearly_totals = filtered.groupby("Year")["Tourist_Arrivals"].sum().reset_index()

c_trend, c_yoy = st.columns(2)

with c_trend:
    st.markdown("**Annual Tourist Arrivals Trend**")
    fig_annual = go.Figure()
    fig_annual.add_trace(go.Scatter(
        x=yearly_totals["Year"],
        y=yearly_totals["Tourist_Arrivals"],
        mode="lines+markers",
        line=dict(color="#0284c7", width=3.5, shape="spline"),
        marker=dict(size=8, color="#0369a1", symbol="circle", line=dict(color="white", width=2)),
        fill="tozeroy",
        fillcolor="rgba(2, 132, 199, 0.08)",
        name="Arrivals"
    ))
    fig_annual.update_layout(
        template="plotly_white",
        hovermode="x unified",
        margin=dict(l=10, r=10, t=10, b=10),
        yaxis=dict(gridcolor="#f1f5f9", tickformat=",.0f", title="Tourist Arrivals"),
        xaxis=dict(gridcolor="#f1f5f9", tickmode="linear", dtick=1, title="Year")
    )
    st.plotly_chart(fig_annual, use_container_width=True)

with c_yoy:
    if len(yearly_totals) > 1:
        st.markdown("**Year-over-Year (YoY) Growth Rate (%)**")
        yearly_totals["YoY_Growth"] = yearly_totals["Tourist_Arrivals"].pct_change() * 100
        yoy_data = yearly_totals.dropna(subset=["YoY_Growth"]).copy()
        yoy_data["Color"] = yoy_data["YoY_Growth"].apply(lambda x: "#10b981" if x >= 0 else "#ef4444")
        
        fig_yoy = go.Figure(go.Bar(
            x=yoy_data["Year"],
            y=yoy_data["YoY_Growth"],
            marker=dict(color=yoy_data["Color"]),
            text=yoy_data["YoY_Growth"].apply(lambda x: f"{x:+.1f}%"),
            textposition="outside"
        ))
        fig_yoy.update_layout(
            template="plotly_white",
            hovermode="x unified",
            margin=dict(l=10, r=10, t=25, b=10),
            yaxis=dict(gridcolor="#f1f5f9", ticksuffix="%", title="YoY Growth (%)"),
            xaxis=dict(gridcolor="#f1f5f9", tickmode="linear", dtick=1, title="Year")
        )
        st.plotly_chart(fig_yoy, use_container_width=True)
    else:
        st.markdown(f"**Quarterly Performance ({selected_years[0]})**")
        q_order = ["Q1", "Q2", "Q3", "Q4"]
        q_totals = filtered.groupby("Quarter")["Tourist_Arrivals"].sum().reindex(q_order).fillna(0).reset_index()
        fig_quarter = px.bar(
            q_totals,
            x="Quarter",
            y="Tourist_Arrivals",
            text=q_totals["Tourist_Arrivals"].apply(lambda x: f"{x:,.0f}"),
            color_discrete_sequence=["#0284c7"],
            labels={"Tourist_Arrivals": "Arrivals", "Quarter": "Quarter"},
            template="plotly_white"
        )
        fig_quarter.update_traces(textposition="outside")
        fig_quarter.update_layout(
            yaxis_tickformat=",.0f",
            margin=dict(l=10, r=10, t=25, b=10),
            yaxis=dict(gridcolor="#f1f5f9"),
            xaxis=dict(gridcolor="#f1f5f9")
        )
        st.plotly_chart(fig_quarter, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Section 2: Geographic & Market Structure (2 Columns)
# ---------------------------------------------------------
st.markdown('<div class="section-title">🌍 2. Geographic & Market Structure</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Core feeder market rankings and regional share breakdown</div>', unsafe_allow_html=True)

c_markets, c_share = st.columns([6, 4])

with c_markets:
    top_n = min(10, filtered["Country"].nunique())
    st.markdown(f"**Top {top_n} Source Countries**")
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
        text=top10["Tourist_Arrivals"].apply(lambda x: f"{x/1e6:.2f}M" if x >= 1e6 else f"{x/1e3:.0f}k"),
        labels={"Tourist_Arrivals": "Arrivals", "Country": "Country"},
        template="plotly_white"
    )
    fig_top.update_traces(textposition="outside")
    fig_top.update_layout(
        yaxis=dict(autorange="reversed", gridcolor="#f1f5f9"),
        xaxis=dict(tickformat=",.0f", gridcolor="#f1f5f9"),
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False
    )
    st.plotly_chart(fig_top, use_container_width=True)

with c_share:
    if selected_continent == "All Continents":
        st.markdown("**Regional Market Share by Continent**")
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
            color_discrete_sequence=["#0284c7", "#06b6d4", "#10b981", "#f59e0b", "#8b5cf6"]
        )
    else:
        st.markdown(f"**Top Markets in {selected_continent}**")
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
            color_discrete_sequence=["#0284c7", "#0ea5e9", "#38bdf8", "#7dd3fc", "#bae6fd"]
        )
    fig_share.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hoverinfo="label+value+percent"
    )
    fig_share.update_layout(
        template="plotly_white",
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False
    )
    st.plotly_chart(fig_share, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Section 3: Seasonal Demand Dynamics (Full Width)
# ---------------------------------------------------------
st.markdown('<div class="section-title">🗓️ 3. Seasonal Demand Dynamics</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Monthly arrival distribution highlighting the high-yield Peak vs. Off-Peak operating cycle</div>', unsafe_allow_html=True)

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
    labels={"Tourist_Arrivals": "Arrivals", "Month": "Month", "Season": "Season"},
    template="plotly_white"
)
fig_monthly.update_traces(textposition="outside")
fig_monthly.update_layout(
    xaxis=dict(categoryorder="array", categoryarray=month_order, gridcolor="#f1f5f9"),
    yaxis=dict(tickformat=",.0f", gridcolor="#f1f5f9"),
    margin=dict(l=10, r=10, t=10, b=10),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        title=None
    )
)
st.plotly_chart(fig_monthly, use_container_width=True)

st.caption("🔵 **Peak Season**: Nov–Apr (European winter holiday) & Jul–Aug (Summer travel & Kandy Esala Perahera) &bull; ⚪ **Off-Peak**: May–Jun & Sep–Oct (Inter-monsoon periods)")

# ---------------------------------------------------------
# Section 4: Data Inspection & Export (Collapsible)
# ---------------------------------------------------------
with st.expander("📋 View Filtered Data Table & Export as CSV", expanded=False):
    st.dataframe(
        filtered[["Year", "Month", "Country", "Continent", "Quarter", "Season", "Period", "Tourist_Arrivals"]],
        use_container_width=True,
        hide_index=True
    )
    csv_data = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Filtered Dataset (.csv)",
        data=csv_data,
        file_name="sri_lanka_tourism_filtered.csv",
        mime="text/csv"
    )

# ---------------------------------------------------------
# Clean Footer
# ---------------------------------------------------------
st.markdown("---")
st.caption(
    f"📊 Dataset Status: **{filtered['Country'].nunique():,} countries** &bull; **{filtered['Date'].nunique():,} monthly timepoints** &bull; Official SLTDA Records (2018–2025)"
)
