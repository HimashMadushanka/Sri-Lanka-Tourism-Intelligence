# 🇱🇰 Sri Lanka Tourism Analytics: Demand, Crisis Impact & Strategic Growth (2018–2025)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-darkblue.svg)](https://pandas.pydata.org/)
[![Seaborn](https://img.shields.io/badge/Seaborn-Data%20Viz-teal.svg)](https://seaborn.pydata.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Executive Deck](https://img.shields.io/badge/Presentation-5--Slide%20Deck-orange.svg)](EXECUTIVE_SUMMARY.md)

> A strategic, end-to-end data and business analytics project evaluating Sri Lanka's inbound tourism performance, crisis resilience, seasonal dynamics, and source market concentration across 2018–2025.

---

## 📌 1-Page Executive Summary *(Recruiter & Decision-Maker Fast Track)*

Between 2018 and 2025, Sri Lanka's tourism economy endured an unprecedented series of catastrophic external shocks: the **2019 Easter Sunday Attacks**, the **2020–2021 COVID-19 pandemic**, and the **2022 domestic economic crisis**. 

This analytics project tracks how demand plummeted to a historic low of **194,495 arrivals in 2021 (-91.7% from 2018 baseline)** and executed a remarkable turnaround to reach **2,362,521 arrivals in 2025 (101.2% recovery)**, setting an all-time national record.

### 🏆 Macro Performance Snapshot

| Strategic Metric | Baseline (2018) | Crisis Trough (2021) | Mid-Recovery (2023) | Full Rebound (2025) |
| :--- | :---: | :---: | :---: | :---: |
| **Annual International Arrivals** | 2,333,796 | 194,495 | 1,487,303 | **2,362,521** |
| **YoY Arrival Trajectory** | Baseline | -61.7% YoY | +106.6% YoY | **+15.1% YoY** |
| **Recovery Index (vs. 2018 Baseline)** | 100.0% | 8.3% | 63.7% | **101.2% (Record High)** |
| **Dominant Source Market** | India (~20%) | Domestic / India | India / Russia | **India (2.3M Cumulative)** |
| **Peak Demand Period** | December–February | Restricted | December–March | **December (1.39M Total)** |

---

## 📊 Hero Visualizations

### 1. Crisis Impact & Recovery Timeline (2018–2025)
*Directly maps macroeconomic shocks, trough levels, and rebound velocity against pre-crisis baseline.*

![Sri Lanka Tourism Crisis Timeline](outputs/figures/yearly_tourism_performance.png)

---

### 2. Executive Performance Dashboard (4-Panel Strategic View)
*Comprehensive cross-sectional breakdown covering crisis trajectories, market concentration, seasonality curves, and recovery velocity.*

![Executive Performance Dashboard](outputs/figures/final_tourism_analysis.png)

---

### 3. Monthly Seasonality & Off-Peak Demand Swings
*Highlights the critical 62% demand swing between December peaks and May–June monsoon troughs.*

![Monthly Seasonality Distribution](outputs/figures/monthly_seasonality.png)

---

### 4. Top 10 Source Markets & Cumulative Pareto Concentration
*Illustrates market concentration where the top 5 countries account for over 51% of all inbound tourists.*

![Top Source Markets Pareto Analysis](outputs/figures/top_source_markets.png)

---

## 💡 Actionable Business Recommendations

Rather than generic tourism advice, the data reveals specific operational, pricing, and marketing interventions:

### 1. Off-Peak Demand Smoothing (May–June Monsoon Trough)
* **The Problem:** Total arrivals drop to **~527K in May** and **~596K in June** (a **62% decrease** compared to December), driving hotel vacancy and airline yield drops.
* **Actionable Solution:** 
  * Launch focused **Ayurveda, Wellness, and MICE (Corporate Meetings)** campaigns tailored specifically to short-haul markets (**India, GCC, Singapore**) where flight times are short (<4 hours) and booking lead times are under 14 days.
  * Form joint capacity bundles with regional carriers (SriLankan Airlines, IndiGo, Emirates) offering discounted off-peak seat guarantees linked with luxury hotel stays.

### 2. European Winter Campaign Lead-Time (December–February Peak)
* **The Problem:** December is the highest arrival month (**1.39M historical arrivals**), followed by January and February, driven by high-spending Western European travelers escaping cold winters.
* **Actionable Solution:** 
  * Allocate 55% of the annual digital marketing and trade roadshow budget to the **UK, Germany, and France** during **September–October (90–120 days lead time)**.
  * Target long-stay packages (14+ nights) highlighting cultural round-trips and south-coast beach stays to maximize revenue yield and length-of-stay metrics.

### 3. Source Market Diversification & Risk Mitigation
* **The Problem:** India represents **~20% (2.3M arrivals)** of all visitors, and the top 5 markets represent **over 51%**. This leaves the industry exposed to regional geopolitical or economic fluctuations.
* **Actionable Solution:** 
  * Actively cultivate resilient secondary markets: **Australia (526K), China (800K), and Scandinavia**.
  * Integrate seamless friction-free local payment channels (**UPI for Indian travelers**, **Alipay/WeChat Pay for Chinese travelers**) across hospitality operators to boost in-destination retail and dining expenditure.

### 4. Dynamic Crisis Resilience & Capacity Planning
* **The Problem:** Historical recovery was rapid (+106% in 2023) once external barriers lifted, but strained local power, transportation, and border facilities.
* **Actionable Solution:** 
  * Develop institutional scenario playbooks with flexible cancellation frameworks and guaranteed utility access for hotels during future supply disruptions.
  * Scale e-Visa processing capacity and fast-track automated airport biometric lanes to comfortably handle projected 2.5M+ peak arrival surges without tourist friction.

---

## 📂 Project Architecture

```
Sri-Lanka-Tourism-Analytics/
│
├── data/
│   ├── raw/                  # Official SLTDA yearly Excel reports (2018–2025)
│   ├── processed/            # Standardized, cleaned master datasets
│   └── reference/            # Country code mappings and continent definitions
│
├── notebooks/
│   ├── 01_Data_Loading_and_Integration.ipynb   # Multi-year schema integration
│   ├── 02_Data_Quality_and_Cleaning.ipynb      # Anomaly detection & cleaning
│   ├── 03_Descriptive_Statistics.ipynb         # Distribution & summary statistics
│   └── 04_Overall_Tourism_Performance.ipynb    # Deep business analytics, forecasting & scenarios
│
├── outputs/
│   ├── figures/              # High-resolution publication & dashboard figures (300 DPI)
│   │   ├── yearly_tourism_performance.png      # Annotated timeline chart
│   │   ├── monthly_seasonality.png             # Seasonality distribution
│   │   ├── top_source_markets.png              # Pareto market concentration
│   │   └── final_tourism_analysis.png          # Executive 4-panel dashboard
│   └── tables/               # Automated summary tables & business insight metrics
│
├── EXECUTIVE_SUMMARY.md      # 5-Slide Executive Pitch Deck for decision-makers
├── requirements.txt          # Reproducible environment dependencies
└── README.md                 # Primary project documentation
```

---

## 🛠️ Tech Stack & Analytical Methodologies

* **Data Engineering & Wrangling:** `pandas`, `numpy`, `openpyxl`
* **Country Normalization:** `country_converter` (ISO standard mapping across 200+ regions)
* **Statistical Analysis:** `scipy`, `statsmodels` (Time series decomposition, CAGR, Demand Index)
* **Visual Storytelling & Dashboards:** `matplotlib`, `seaborn` (Multi-panel layouts, event annotations, Pareto curves)
* **Business Frameworks:** Pareto (80/20 Rule), YoY Growth Analysis, Recovery Index Benchmarking, Scenario Analysis (Bull/Base/Bear)

---

## 🚀 Setup & Reproduction

1. **Clone the repository:**
   ```bash
   git clone https://github.com/HimashMadushanka/Sri-Lanka-Tourism-Analytics.git
   cd Sri-Lanka-Tourism-Analytics
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run analysis:**
   Open and execute notebooks in sequence (`01` through `04`) or view the presentation deck in [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md).

---

## 👤 Author & Contact

* **Himash Madushanka**  
* **Focus:** Data Analysis | Business Analytics | Market Intelligence  
* **Executive Presentation Deck:** [View 5-Slide Presentation Deck](EXECUTIVE_SUMMARY.md)
