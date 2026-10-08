import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime

# Page Configuration & Modern Dark Theme Styling
st.set_page_config(
    page_title="Sri Lanka Tourism Intelligence & Decision Platform",
    page_icon="🇱🇰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Dark Theme + Vivid Orange Accent Design
st.markdown("""
<style>
    /* Global Base */
    .stApp {
        background-color: #0b0f19;
        color: #f8fafc;
    }
    
    /* Sleek Prominent Gradient Orange Hero Header - Guaranteed One Line */
    .hero-container {
        margin-top: -10px;
        margin-bottom: 18px;
        padding-bottom: 4px;
        width: 100%;
    }
    .hero-title-text {
        background: linear-gradient(135deg, #ffffff 0%, #ffedd5 20%, #fb923c 65%, #f97316 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: clamp(1.85rem, 2.5vw, 2.65rem);
        line-height: 1.2;
        letter-spacing: -0.5px;
        display: block;
        white-space: nowrap;
        text-shadow: 0 4px 28px rgba(249, 115, 22, 0.35);
    }
    .hero-subtitle {
        color: #cbd5e1;
        font-size: 1.22rem;
        font-weight: 500;
        margin-top: 8px;
        letter-spacing: 0.2px;
    }
    
    /* Metric Card Styling: Dark Glassmorphic with Uniform Exact Size */
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #111827 0%, #1e293b 100%);
        border: 1px solid rgba(249, 115, 22, 0.3);
        padding: 14px 16px !important;
        border-radius: 12px;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.4);
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
        height: 136px !important;
        min-height: 136px !important;
        max-height: 136px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
        box-sizing: border-box !important;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        border-color: #f97316;
        box-shadow: 0 6px 24px rgba(249, 115, 22, 0.3);
    }
    /* Prevent metric label truncation: allow wrapping and clear display */
    div[data-testid="stMetric"] label,
    div[data-testid="stMetric"] [data-testid="stMetricLabel"],
    div[data-testid="stMetric"] [data-testid="stMetricLabel"] div,
    div[data-testid="stMetric"] [data-testid="stMetricLabel"] p {
        font-size: 0.78rem !important;
        font-weight: 700 !important;
        color: #cbd5e1 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.3px !important;
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: clip !important;
        line-height: 1.25 !important;
        height: auto !important;
        word-break: break-word !important;
        margin: 0 !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        font-size: 1.65rem !important;
        font-weight: 800 !important;
        color: #f97316 !important;
        text-shadow: 0 0 14px rgba(249, 115, 22, 0.35);
        margin-top: 2px !important;
        line-height: 1.2 !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricDelta"] {
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        margin-top: 2px !important;
    }
    
    /* Tabs with Vibrant Orange Indicators */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
        border-bottom: 1px solid #1e293b;
        padding-bottom: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        background-color: #111827;
        color: #94a3b8;
        border: 1px solid #1e293b;
        border-radius: 8px 8px 0px 0px;
        padding: 10px 18px;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.2s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #fdba74;
        border-color: rgba(249, 115, 22, 0.4);
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(180deg, #1e293b 0%, #131b2e 100%) !important;
        color: #f97316 !important;
        border-color: #f97316 !important;
        border-bottom: 3px solid #f97316 !important;
        box-shadow: 0 -2px 12px rgba(249, 115, 22, 0.2);
    }
    
    /* Alert Banners (Dark Mode + Neon Glow) */
    .alert-box {
        padding: 14px 18px;
        border-radius: 10px;
        margin-bottom: 18px;
        font-size: 0.92rem;
        line-height: 1.5;
    }
    .alert-orange {
        background-color: rgba(249, 115, 22, 0.12);
        border: 1px solid #f97316;
        border-left: 5px solid #f97316;
        color: #fed7aa;
    }
    .alert-green {
        background-color: rgba(34, 197, 94, 0.12);
        border: 1px solid #22c55e;
        border-left: 5px solid #22c55e;
        color: #bbf7d0;
    }
    .alert-amber {
        background-color: rgba(245, 158, 11, 0.12);
        border: 1px solid #f59e0b;
        border-left: 5px solid #f59e0b;
        color: #fde68a;
    }

    /* Primary Buttons & Downloads: Flame Orange */
    .stDownloadButton button, .stButton button {
        background: linear-gradient(135deg, #f97316 0%, #ea580c 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 22px !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 14px rgba(234, 88, 12, 0.45) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }
    .stDownloadButton button:hover, .stButton button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(249, 115, 22, 0.65) !important;
    }
</style>
""", unsafe_allow_html=True)


# Plotly Dark Theme Preset Helper
def apply_dark_theme(fig, height=430):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111827",
        plot_bgcolor="#0b0f19",
        font=dict(color="#f8fafc", family="sans-serif"),
        xaxis=dict(gridcolor="#1e293b", linecolor="#334155", zerolinecolor="#334155"),
        yaxis=dict(gridcolor="#1e293b", linecolor="#334155", zerolinecolor="#334155"),
        height=height,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig

# Data Loading & Caching
def load_data():
    data_path = Path("data/processed/tourism_arrivals_app_ready.csv")
    if not data_path.exists():
        data_path = Path("data/processed/tourism_arrivals_clean.csv")
        df = pd.read_csv(data_path)
        df["Standard_Country"] = df["Country"]
        df["Continent"] = "All"
    else:
        df = pd.read_csv(data_path)
    
    df["Date"] = pd.to_datetime(df["Date"])
    df["Tourist_Arrivals"] = pd.to_numeric(df["Tourist_Arrivals"], errors="coerce").fillna(0)
    return df

df_raw = load_data()


# Sidebar: Control Panel & 5 Strategic Filters
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 14px;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/1/11/Flag_of_Sri_Lanka.svg" 
             style="width: 100%; max-width: 260px; border-radius: 10px; border: 2px solid #f97316; box-shadow: 0 4px 18px rgba(249, 115, 22, 0.35);">
    </div>
    """, unsafe_allow_html=True)
    st.markdown("### 🎛️ Control Panel")
    st.divider()

    #  Timeline Preset & Year Range
    min_year, max_year = int(df_raw["Year"].min()), int(df_raw["Year"].max())
    
    st.subheader("1. Choose Time Period")
    all_years_label = f"All Years ({min_year}–{max_year})"
    rec_years_label = f"Recovery Period (2023–{max_year})"

    phase_preset = st.selectbox(
        "Select Time Period",
        options=[
            all_years_label,
            "Before Crisis (2018–2019)", 
            "Crisis Years (2020–2022)",
            rec_years_label
        ],
        index=0
    )

    if phase_preset == "Before Crisis (2018–2019)":
        default_years = (2018, min(2019, max_year))
    elif phase_preset == "Crisis Years (2020–2022)":
        default_years = (2020, min(2022, max_year))
    elif phase_preset == rec_years_label:
        default_years = (2023, max_year)
    else:
        default_years = (min_year, max_year)

    selected_years = st.slider("Select Year Range", min_value=min_year, max_value=max_year, value=default_years)

    #  Continent / Region Filter
    all_continents = ["All Continents"] + sorted([c for c in df_raw["Continent"].dropna().unique() if c != "Other"])
    selected_continent = st.selectbox("Select Region ", options=all_continents, index=0)

    #  Country Filter
    st.subheader("2. Choose Countries")
    market_mode = st.radio("Filter Countries:", options=["All Countries", "Top 10 Countries", "Pick My Own"], index=0)
    
    top_10_countries = (
        df_raw.groupby("Standard_Country")["Tourist_Arrivals"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .index.tolist()
    )

    if market_mode == "Top 10 Countries":
        selected_countries = top_10_countries
    elif market_mode == "Pick My Own":
        available_countries = sorted(df_raw["Standard_Country"].dropna().unique().tolist())
        selected_countries = st.multiselect("Select Countries", options=available_countries, default=top_10_countries[:5])
    else:
        selected_countries = None

    #  Season / Month Filter
    st.subheader("3. Season & Months")
    season_preset = st.selectbox(
        "Select Season Range",
        options=[
            "Full Year (All Months)",
            "Winter High Season (Dec - Feb)",
            "Rainy Season (May - Jun)",
            "Summer Holidays (Jul - Aug)",
            "Pick Months"
        ],
        index=0
    )

    months_map = {
        "January": 1, "February": 2, "March": 3, "April": 4,
        "May": 5, "June": 6, "July": 7, "August": 8,
        "September": 9, "October": 10, "November": 11, "December": 12
    }

    if season_preset == "Winter High Season (Dec - Feb)":
        selected_months = [12, 1, 2]
    elif season_preset == "Rainy Season (May - Jun)":
        selected_months = [5, 6]
    elif season_preset == "Summer Holidays (Jul - Aug)":
        selected_months = [7, 8]
    elif season_preset == "Pick Months":
        chosen_m_names = st.multiselect("Select Months", options=list(months_map.keys()), default=["December", "January"])
        selected_months = [months_map[m] for m in chosen_m_names] if chosen_m_names else list(range(1, 13))
    else:
        selected_months = list(range(1, 13))

    st.divider()
    st.caption("Sri Lanka Tourism Analytics • v2.0")


# Apply Filters to Dataset
df_filtered = df_raw.copy()
df_filtered = df_filtered[(df_filtered["Year"] >= selected_years[0]) & (df_filtered["Year"] <= selected_years[1])]

if selected_continent != "All Continents":
    df_filtered = df_filtered[df_filtered["Continent"] == selected_continent]

if selected_countries is not None and len(selected_countries) > 0:
    df_filtered = df_filtered[df_filtered["Standard_Country"].isin(selected_countries)]

if selected_months:
    df_filtered = df_filtered[df_filtered["Month_Number"].isin(selected_months)]

# Macro reference data
yearly_full = df_raw.groupby("Year")["Tourist_Arrivals"].sum().reset_index()
base_2018 = yearly_full.loc[yearly_full["Year"] == 2018, "Tourist_Arrivals"].values[0] if 2018 in yearly_full["Year"].values else 2333796
latest_year_num = int(yearly_full["Year"].max())
curr_latest = yearly_full.loc[yearly_full["Year"] == latest_year_num, "Tourist_Arrivals"].values[0]
curr_2025 = curr_latest


# Top Header & Macro KPI Snapshot
st.markdown("""
<div class="hero-container">
    <div class="hero-title-text">Sri Lanka Tourism Intelligence & Decision Platform</div>
</div>
""", unsafe_allow_html=True)

kpi_c1, kpi_c2, kpi_c3, kpi_c4, kpi_c5 = st.columns(5)
total_filtered_arrivals = df_filtered["Tourist_Arrivals"].sum()
unique_markets = df_filtered["Standard_Country"].nunique()
peak_filtered_year = df_filtered.groupby("Year")["Tourist_Arrivals"].sum().idxmax() if not df_filtered.empty else "-"
peak_val = df_filtered.groupby("Year")["Tourist_Arrivals"].sum().max() if not df_filtered.empty else 0
recovery_index_calc = (curr_latest / base_2018) * 100

kpi_c1.metric("Total Visitors", f"{total_filtered_arrivals/1e6:.2f}M" if total_filtered_arrivals >= 1e6 else f"{total_filtered_arrivals:,.0f}", delta=f"{selected_years[0]}–{selected_years[1]} Total", delta_color="off", help="Total tourist arrivals under current filters")
kpi_c2.metric(f"Recovery ({latest_year_num})", f"{recovery_index_calc:.1f}%", delta=f"{recovery_index_calc - 100:+.1f}% vs 2018", help=f"{latest_year_num} arrivals compared to 2018 record peak")
kpi_c3.metric("Busiest Year", f"{peak_filtered_year}", delta=f"{peak_val/1e6:.2f}M Peak Volume", help="Year with the highest recorded tourist arrivals")
kpi_c4.metric("Countries", f"{unique_markets}", delta="Contributing Markets", delta_color="off", help="Number of inbound tourist source countries")
kpi_c5.metric("Lowest Year (2021)", "194.5K", delta="-91.7% vs 2018", delta_color="inverse", help="Lowest arrival level recorded during global pandemic lockdowns")

st.markdown("---")


# 5-Step Operational Framework Tabs
tabs = st.tabs([
    "1️⃣ Shocks & Recovery",
    "2️⃣ Top Countries",
    "3️⃣ Future Forecast",
    "4️⃣ Hotel Planning",
    "5️⃣ Action Plans"
])


# TAB 1: SHOCKS & RECOVERY
with tabs[0]:
    st.subheader(f"1️⃣ Major Shocks & Visitor Recovery ({min_year}–{max_year})")
   
    yearly_filtered = df_filtered.groupby("Year")["Tourist_Arrivals"].sum().reset_index()
    yearly_filtered["YoY_Growth_%"] = yearly_filtered["Tourist_Arrivals"].pct_change() * 100

    min_growth = yearly_filtered["YoY_Growth_%"].min()
    if min_growth < -50:
        st.markdown("""
        <div class="alert-box alert-amber">
            <strong>⚠️ Major Drop Detected:</strong> Tourist arrivals fell by more than 50% during crisis years.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="alert-box alert-orange">
            <strong>🔥 Strong Recovery:</strong> Tourist arrivals have fully recovered and crossed the 2018 record ({curr_latest/1e6:.2f}M visitors in {latest_year_num}).
        </div>
        """, unsafe_allow_html=True)

    # Timeline with Crisis Annotations (Full Width Clean Layout)
    fig_timeline = go.Figure()

    # Add Shaded Areas for Crisis & Recovery
    fig_timeline.add_vrect(x0=2018.7, x1=2022.3, fillcolor="rgba(239, 68, 68, 0.12)", line_width=0, annotation_text="Crisis Period (2019–2022)", annotation_position="top left", annotation_font_color="#ef4444")
    fig_timeline.add_vrect(x0=2022.3, x1=2025.3, fillcolor="rgba(249, 115, 22, 0.12)", line_width=0, annotation_text="Recovery (2023–2025)", annotation_position="top left", annotation_font_color="#f97316")

    # Baseline line
    fig_timeline.add_hline(y=base_2018, line_dash="dash", line_color="#94a3b8", annotation_text=f"2018 Record Peak ({base_2018/1e6:.2f}M visitors)", annotation_font_color="#cbd5e1")

    # Main timeline trace in glowing orange
    fig_timeline.add_trace(go.Scatter(
        x=yearly_filtered["Year"],
        y=yearly_filtered["Tourist_Arrivals"],
        mode="lines+markers+text",
        name="Visitors",
        text=[f"{v/1e6:.2f}M" for v in yearly_filtered["Tourist_Arrivals"]],
        textposition="top center",
        textfont=dict(color="#f97316", size=11),
        line=dict(color="#f97316", width=3.8),
        marker=dict(size=10, color="#fb923c", line=dict(color="#0b0f19", width=2.5))
    ))

    # Event Annotations in Dark Theme Callouts (dynamically matched to filtered data)
    event_annotations = [
        (2019, "<b>2019: Easter Attacks</b><br>(-18% drop)", "#ef4444", "#fca5a5", -65, -40),
        (2021, "<b>2020–21: COVID Lockdowns</b><br>(Lowest: 194K visitors)", "#ef4444", "#fca5a5", 0, -50),
        (2022, "<b>2022: Economic Crisis</b><br>(Fuel & power shortages)", "#f59e0b", "#fde68a", -65, -45),
        (2025, "<b>2025: All-Time Record</b><br>(2.36M visitors)", "#22c55e", "#86efac", -65, -45),
    ]
    for yr, text, color, font_color, ax, ay in event_annotations:
        if yr in yearly_filtered["Year"].values:
            y_val = yearly_filtered.loc[yearly_filtered["Year"] == yr, "Tourist_Arrivals"].values[0]
            fig_timeline.add_annotation(
                x=yr, y=y_val, text=text, showarrow=True, arrowhead=2,
                arrowcolor=color, ax=ax, ay=ay, bgcolor="#1f2937",
                bordercolor=color, font=dict(color=font_color, size=10)
            )

    fig_timeline.update_layout(
        title="Yearly Tourist Arrivals: Crises & Recovery (2018–2025)",
        xaxis=dict(title="Year", tickmode="linear", dtick=1),
        yaxis=dict(title="Yearly Visitors"),
        hovermode="x unified"
    )
    apply_dark_theme(fig_timeline, height=450)
    st.plotly_chart(fig_timeline, use_container_width=True)

    with st.expander("📊 View Year-by-Year Summary Table (with YoY Growth)"):
        y_summary = yearly_filtered.copy()
        y_summary["YoY Growth %"] = y_summary["Tourist_Arrivals"].pct_change() * 100
        y_summary["Total Visitors"] = y_summary["Tourist_Arrivals"].map(lambda x: f"{x:,.0f}")
        y_summary["YoY Growth"] = y_summary["YoY Growth %"].map(lambda x: f"{x:+.1f}%" if pd.notnull(x) else "Baseline")
        st.dataframe(y_summary[["Year", "Total Visitors", "YoY Growth"]], use_container_width=True, hide_index=True)



# TAB 2: TOP COUNTRIES & SEASONALITY
with tabs[1]:
    st.subheader("2️⃣ Top Countries & Seasonality")
    
    col_m1, col_m2 = st.columns([6, 4])
    
    country_totals = df_filtered.groupby("Standard_Country")["Tourist_Arrivals"].sum().sort_values(ascending=False).reset_index()
    country_totals = country_totals[~country_totals["Standard_Country"].isin(["Other", "Unknown", "NOT FOUND"])].head(15)
    safe_filtered_total = total_filtered_arrivals if total_filtered_arrivals > 0 else 1
    country_totals["Share_%"] = (country_totals["Tourist_Arrivals"] / safe_filtered_total) * 100
    country_totals["Cumulative_%"] = country_totals["Share_%"].cumsum()

    with col_m1:
        fig_pareto = go.Figure()
        # Bars in Vivid Orange
        fig_pareto.add_trace(go.Bar(
            x=country_totals["Standard_Country"],
            y=country_totals["Tourist_Arrivals"],
            name="Visitors",
            marker=dict(color="#f97316", line=dict(color="#ea580c", width=1))
        ))
        # Cumulative line in Neon Cyan for high-contrast visibility
        fig_pareto.add_trace(go.Scatter(
            x=country_totals["Standard_Country"],
            y=country_totals["Cumulative_%"],
            name="Share of Total %",
            yaxis="y2",
            line=dict(color="#38bdf8", width=2.8),
            marker=dict(size=8, color="#0284c7")
        ))
        fig_pareto.update_layout(
            title="Top 15 Countries by Tourist Arrivals",
            xaxis=dict(title="Country", tickangle=35),
            yaxis=dict(title="Total Visitors"),
            yaxis2=dict(title="Share of Total Visitors (%)", overlaying="y", side="right", range=[0, 105], gridcolor="rgba(0,0,0,0)"),
            legend=dict(x=0.02, y=0.95, bgcolor="rgba(17,24,39,0.8)")
        )
        apply_dark_theme(fig_pareto, height=440)
        st.plotly_chart(fig_pareto, use_container_width=True)

    with col_m2:
        st.markdown("#### Country Share Breakdown")
        top5_share = country_totals["Cumulative_%"].iloc[4] if len(country_totals) >= 5 else (country_totals["Cumulative_%"].iloc[-1] if not country_totals.empty else 0)

        st.metric("Top 5 Countries Share", f"{top5_share:.1f}%", help="Percentage of all tourists coming from the top 5 countries")
        top_name = country_totals["Standard_Country"].iloc[0] if not country_totals.empty else "-"
        top_pct = country_totals["Share_%"].iloc[0] if not country_totals.empty else 0
        st.metric("Top Source Market", f"{top_name}", f"{top_pct:.1f}% of all visitors" if not country_totals.empty else "", help="Country bringing the single highest number of tourists")

        st.markdown("""
        <div style="background-color: rgba(30, 41, 59, 0.6); border: 1px solid rgba(249, 115, 22, 0.25); border-radius: 8px; padding: 12px; margin-top: 14px; font-size: 0.88rem; color: #cbd5e1;">
            💡 <strong>Key Fact:</strong> More than half of all visitors come from just 5 countries (led by India and the UK).
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Heatmap of Seasonality across Top Markets
    st.markdown("#### When Do Tourists Visit? (Month-by-Month Matrix)")
    
    col_hm1, col_hm2 = st.columns([7, 3])
    with col_hm1:
        hm_view_mode = st.radio(
            "View Type:",
            options=[
                "Seasonal Pattern (% of country's annual total) — Recommended",
                "Total Visitor Count (Numbers)"
            ],
            index=0,
            horizontal=True,
            help="The Seasonal Pattern view normalizes each country so you can clearly see the peak and low months for EVERY country, even smaller markets."
        )
    with col_hm2:
        show_cell_labels = st.checkbox("Show Numbers on Chart", value=True, help="Display exact percentages or visitor counts directly on each tile")

    top10_list = country_totals["Standard_Country"].head(10).tolist()
    chron_months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    heatmap_raw = df_filtered[df_filtered["Standard_Country"].isin(top10_list)].pivot_table(
        index="Standard_Country",
        columns="Month",
        values="Tourist_Arrivals",
        aggfunc="sum"
    ).fillna(0)

    available_months = [m for m in chron_months if m in heatmap_raw.columns]
    heatmap_raw = heatmap_raw.reindex(index=top10_list, columns=available_months).fillna(0)

    # Glowing Ember Palette with distinct slate base tile (#151e2e) so low values don't vanish into black
    orange_flame = [
        [0.0, "#151e2e"],
        [0.18, "#1e293b"],
        [0.4, "#9a3412"],
        [0.65, "#ea580c"],
        [0.85, "#f97316"],
        [1.0, "#fef08a"]
    ]

    if heatmap_raw.empty or len(available_months) == 0 or len(top10_list) == 0:
        st.info("No visitor data matches the current filter selection to display the seasonality heatmap.")
    else:
        is_relative = "Seasonal Pattern" in hm_view_mode

        if is_relative:
            row_totals = heatmap_raw.sum(axis=1).replace(0, 1)
            display_df = (heatmap_raw.div(row_totals, axis=0) * 100).round(1)
            color_label = "Share of Year %"
            text_matrix = display_df.map(lambda v: f"{v:.1f}%")
        else:
            display_df = heatmap_raw
            color_label = "Visitors"
            text_matrix = display_df.map(lambda v: f"{v/1e6:.2f}M" if v >= 1e6 else (f"{v/1e3:.0f}K" if v >= 1e4 else (f"{v/1e3:.1f}K" if v >= 1e3 else f"{int(v)}")))

        fig_heat = px.imshow(
            display_df,
            labels=dict(x="Month", y="Country", color=color_label),
            x=display_df.columns,
            y=display_df.index,
            color_continuous_scale=orange_flame,
            aspect="auto"
        )

        if show_cell_labels:
            fig_heat.update_traces(
                text=text_matrix.values,
                texttemplate="%{text}",
                textfont=dict(size=11, color="#f8fafc", family="sans-serif"),
                xgap=3,
                ygap=3
            )
        else:
            fig_heat.update_traces(
                xgap=3,
                ygap=3
            )

        if is_relative:
            fig_heat.update_traces(
                customdata=heatmap_raw.values,
                hovertemplate="<b>%{y}</b> • %{x}<br>Share of Year: <b>%{z:.1f}%</b><br>Visitors: <b>%{customdata:,.0f}</b><extra></extra>"
            )
        else:
            fig_heat.update_traces(
                hovertemplate="<b>%{y}</b> • %{x}<br>Visitors: <b>%{z:,.0f}</b><extra></extra>"
            )

        fig_heat.update_layout(
            xaxis=dict(tickangle=0, tickfont=dict(size=12, color="#cbd5e1")),
            yaxis=dict(tickfont=dict(size=12, color="#cbd5e1")),
            coloraxis_colorbar=dict(
                title=dict(text=color_label, font=dict(color="#cbd5e1", size=12)),
                tickfont=dict(color="#cbd5e1", size=11)
            )
        )
        apply_dark_theme(fig_heat, height=480)
        st.plotly_chart(fig_heat, use_container_width=True)



# TAB 3: FUTURE FORECAST (2026–2028)
with tabs[2]:
    st.subheader("3️⃣ Future Visitor Forecast (2026–2028)")
    
    sc_col1, sc_col2 = st.columns([4, 6])

    with sc_col1:
        st.markdown("#### Forecast Settings")
        sim_growth_base = st.slider("Expected Yearly Growth (%)", min_value=-10.0, max_value=25.0, value=8.5, step=0.5)
        sim_shock = st.selectbox(
            "Special Situation / Event:",
            options=[
                "Normal Growth (No major shock)",
                "Expensive Flights & Airfare Surge (-15%)",
                "Free Visas & Extra Promotion (+20%)",
                "Regional Economic Slowdown (-10%)"
            ],
            index=0
        )
        sim_horizon = st.radio("Forecast Up To Year:", options=["2026", "2027", "2028"], horizontal=True, index=2)

        shock_factor = 0.0
        if "Expensive Flights" in sim_shock or "Travel Cost" in sim_shock:
            shock_factor = -0.15
        elif "Free Visas" in sim_shock:
            shock_factor = 0.20
        elif "Regional Economic Slowdown" in sim_shock:
            shock_factor = -0.10

        curr_base = curr_latest
        max_proj_yr = int(sim_horizon)
        proj_years = [y for y in [2026, 2027, 2028] if y <= max_proj_yr]
        eff_growth = (sim_growth_base / 100.0) + shock_factor

        projections = []
        val = curr_base
        for y in proj_years:
            val = val * (1 + eff_growth)
            projections.append({"Year": y, "Projected_Arrivals": val})
        proj_df = pd.DataFrame(projections)

        predicted_end_val = proj_df["Projected_Arrivals"].iloc[-1]
        pct_growth_from_base = ((predicted_end_val - curr_base) / curr_base) * 100
        st.metric(
            label=f"Predicted Arrivals in {max_proj_yr}",
            value=f"{predicted_end_val/1e6:.2f}M visitors",
            delta=f"{pct_growth_from_base:+.1f}% vs 2025",
            help="Forecasted total international tourist arrivals based on selected scenario and year horizon"
        )

    bull_df = []
    bear_df = []
    val_bull = curr_base
    val_bear = curr_base
    for y in proj_years:
        val_bull = val_bull * (1 + (sim_growth_base/100 + 0.12))
        val_bear = val_bear * (1 + (sim_growth_base/100 - 0.12))
        bull_df.append(val_bull)
        bear_df.append(val_bear)

    with sc_col2:
        fig_fc = go.Figure()
        
        hist_df = yearly_full[yearly_full["Year"] >= 2022]
        fig_fc.add_trace(go.Scatter(x=hist_df["Year"], y=hist_df["Tourist_Arrivals"], mode="lines+markers", name="Past Numbers", line=dict(color="#f97316", width=3.5), marker=dict(size=8, color="#fb923c")))

        all_x = [2025] + proj_years
        all_y_base = [curr_base] + proj_df["Projected_Arrivals"].tolist()
        all_y_bull = [curr_base] + bull_df
        all_y_bear = [curr_base] + bear_df

        fig_fc.add_trace(go.Scatter(x=all_x, y=all_y_base, mode="lines+markers+text", name="Forecast", text=[f"{v/1e6:.2f}M" for v in all_y_base], textposition="top center", line=dict(color="#38bdf8", width=3, dash="dot"), marker=dict(size=8, color="#38bdf8")))
        fig_fc.add_trace(go.Scatter(x=all_x, y=all_y_bull, mode="lines", name="Best Case (+12%)", line=dict(color="#22c55e", width=1.8, dash="dash")))
        fig_fc.add_trace(go.Scatter(x=all_x, y=all_y_bear, mode="lines", name="Worst Case (-12%)", line=dict(color="#ef4444", width=1.8, dash="dash")))

        fig_fc.update_layout(
            title=f"Future Visitor Forecast (2026–{max_proj_yr})",
            xaxis=dict(title="Year", tickmode="linear", dtick=1, range=[2021.7, max_proj_yr + 0.35]),
            yaxis=dict(title="Estimated Tourist Arrivals")
        )
        apply_dark_theme(fig_fc, height=440)
        st.plotly_chart(fig_fc, use_container_width=True)



# TAB 4: HOTEL ROOM PLANNING
with tabs[3]:
    st.subheader("4️⃣ Hotel Room Planning")
   

    monthly_demand = df_filtered.groupby(["Month_Number", "Month"])["Tourist_Arrivals"].sum().reset_index().sort_values("Month_Number")
    peak_month_arrivals = monthly_demand["Tourist_Arrivals"].max() if not monthly_demand.empty else 0
    trough_month_arrivals = monthly_demand["Tourist_Arrivals"].min() if not monthly_demand.empty else 0

    st.markdown("#### 🏨 Hotel Room Demand & Capacity")
    st.caption("Estimate how many hotel rooms are needed based on visitor stays and room occupancy.")

    hotel_col1, hotel_col2 = st.columns(2)
    with hotel_col1:
        avg_length_stay = st.slider("Average Days Tourists Stay", min_value=5, max_value=21, value=10)
        persons_per_room = st.slider("Average Guests per Room", min_value=1.0, max_value=2.5, value=1.8, step=0.1)

    total_tourists_yr = df_filtered.groupby("Year")["Tourist_Arrivals"].sum().iloc[-1] if not df_filtered.empty else curr_latest
    est_annual_room_nights = (total_tourists_yr * avg_length_stay) / persons_per_room
    peak_daily_rooms = (peak_month_arrivals * avg_length_stay) / (30 * persons_per_room)

    with hotel_col2:
        st.metric("Daily Rooms Needed in Peak Season", f"{peak_daily_rooms:,.0f} rooms", help="Number of hotel rooms needed each day during the busiest month")
        st.metric("Total Room Nights Needed per Year", f"{est_annual_room_nights/1e6:.2f}M nights", help="Total annual room nights needed for all visitors")

    # Seasonality Bar Chart in Flame Orange
    if monthly_demand.empty or monthly_demand["Tourist_Arrivals"].sum() == 0:
        st.info("No visitor data matches the current filter selection to estimate room demand or display seasonality.")
    else:
        fig_cap = px.bar(
            monthly_demand,
            x="Month",
            y="Tourist_Arrivals",
            title="Which Months Have the Most Visitors?",
            color="Tourist_Arrivals",
            color_continuous_scale="Oranges",
            text_auto=".2s"
        )
        fig_cap.update_layout(xaxis_title="Month", yaxis_title="Total Visitors")
        apply_dark_theme(fig_cap, height=350)
        st.plotly_chart(fig_cap, use_container_width=True)



# TAB 5: DECISION CENTER (Action Plans & Next Steps)
with tabs[4]:
    st.subheader("5️⃣ Decision Center: Simple Action Plans")
    st.markdown("Clear, practical steps for hotels, airlines, and tourism planners to grow visitors and revenue.")

    playbook_selection = st.selectbox(
        "Choose a Goal:",
        options=[
            "1. Bring More Visitors in the Low Season (May–June)",
            "2. Maximize Income in the Busy Winter Season (December–February)",
            "3. Attract Visitors from More Countries (Reduce Risk)",
            "4. Fix Airport Congestion & Infrastructure Readiness"
        ]
    )

    if "1. Bring More Visitors" in playbook_selection:
        st.markdown("""
        ### 📋 Action Plan: Low Season Visitor Boost (May–June)
        | Area | What to Do | Who Does It | When to Start |
        | :--- | :--- | :--- | :--- |
        | **Marketing** | Promote wellness, ayurveda, and business trip deals to nearby countries (India, UAE, Singapore). | Tourism Board & Ad Agencies | April (1 month before) |
        | **Airlines** | Fly medium-sized planes and offer cheaper weekend flights from South India. | Airlines (SriLankan, IndiGo) | 1–2 months before |
        | **Hotels** | Offer "Stay 4 Nights, Pay for 3" deals and free spa treatments to fill empty rooms. | Hotel Association & Resorts | Start now |
        """)
    elif "2. Maximize Income" in playbook_selection:
        st.markdown("""
        ### 📋 Action Plan: Busy Winter Season (December–February)
        | Area | What to Do | Who Does It | When to Start |
        | :--- | :--- | :--- | :--- |
        | **Marketing** | Start winter advertising in the UK, Germany, and France early (around September–October). | Tourism Board & Embassies | 2–3 months before |
        | **Airlines** | Add extra direct and charter flights from London and Frankfurt to handle the crowd. | Airlines | 3 months before |
        | **Hotels** | Require a 5-night minimum stay around Christmas and New Year (Dec 20 – Jan 10) for higher earnings. | Hotel Managers | 2 months before |
        """)
    elif "3. Attract Visitors" in playbook_selection:
        st.markdown("""
        ### 📋 Action Plan: Attract Tourists from More Countries
        | Area | What to Do | Who Does It | When to Start |
        | :--- | :--- | :--- | :--- |
        | **New Markets** | Promote tours in Australia, China, and Nordic countries so we don't depend only on 1 or 2 nations. | Ministry of Tourism | Ongoing |
        | **Easy Payments** | Let tourists pay using Indian UPI and Chinese WeChat Pay / Alipay at hotels and popular spots. | Banks & Local Shops | Within 2 months |
        | **Easy Visas** | Approve online tourist visas (e-Visas) in under 2 hours to make visiting hassle-free. | Immigration Office | Immediate |
        """)
    else:
        st.markdown("""
        ### 📋 Action Plan: Fix Airport Delays & Lines
        | Area | What to Do | Who Does It | When to Start |
        | :--- | :--- | :--- | :--- |
        | **Passport Control** | Open electronic passport gates (e-Gates) and add more immigration counters at Colombo Airport. | Airport Authority | Busy season (Dec–Feb) |
        | **Luggage Staff** | Add extra baggage handlers on night shifts (9 PM to 4 AM) when most European flights land. | Airport Baggage Crew | 2 weeks before |
        """)

    st.divider()
    st.markdown("#### 📥 Download Datasets Year-by-Year & Reports")
    st.caption("Export official visitor datasets for any individual year, all years combined, or annual totals.")

    y_pick_col, dl_btn_col1, dl_btn_col2 = st.columns([2.5, 2.5, 2.5])
    
    available_years = sorted(df_raw["Year"].unique(), reverse=True)
    with y_pick_col:
        chosen_year_str = st.selectbox(
            "Select Year to Download:",
            options=["All Years (2018–2025)"] + [str(y) for y in available_years],
            help="Choose an individual year or all years"
        )

    if "All Years" in chosen_year_str:
        export_dataset = df_raw.copy()
        export_filename = f"sri_lanka_tourism_all_years_{datetime.now().strftime('%Y%m%d')}.csv"
        btn_label = "📥 Download All Years (CSV)"
    else:
        sel_yr = int(chosen_year_str)
        export_dataset = df_raw[df_raw["Year"] == sel_yr].copy()
        export_filename = f"sri_lanka_tourism_{sel_yr}_{datetime.now().strftime('%Y%m%d')}.csv"
        btn_label = f"📥 Download {sel_yr} Dataset (CSV)"

    csv_data = export_dataset.to_csv(index=False).encode('utf-8')
    with dl_btn_col1:
        st.download_button(
            label=btn_label,
            data=csv_data,
            file_name=export_filename,
            mime="text/csv",
            use_container_width=True
        )

    with dl_btn_col2:
        yearly_summary_df = df_raw.groupby("Year")["Tourist_Arrivals"].sum().reset_index()
        yearly_summary_df["YoY Growth %"] = (yearly_summary_df["Tourist_Arrivals"].pct_change() * 100).round(1)
        summary_csv = yearly_summary_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📊 Download Yearly Totals (CSV)",
            data=summary_csv,
            file_name="sri_lanka_tourism_yearly_totals.csv",
            mime="text/csv",
            use_container_width=True
        )

    try:
        with open("EXECUTIVE_SUMMARY.md", "r", encoding="utf-8") as f:
            exec_text = f.read()
        st.download_button(
            label="📄 Download 1-Page Summary Deck (MD)",
            data=exec_text.encode('utf-8'),
            file_name="Sri_Lanka_Tourism_Executive_Summary.md",
            mime="text/markdown",
            use_container_width=True
        )
    except Exception:
        pass
