# 🇱🇰 Sri Lanka Tourism Analytics: Demand, Crisis Impact & Strategic Growth (2018–2025)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=flat&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-FF4B4B.svg?style=flat&logo=streamlit)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458.svg?style=flat&logo=pandas)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75.svg?style=flat&logo=plotly)](https://plotly.com/)
[![GitHub Actions](https://img.shields.io/badge/CI%2FCD-Auto--Update%20Pipeline-2088FF.svg?style=flat&logo=githubactions)](https://github.com/features/actions)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Executive Deck](https://img.shields.io/badge/Presentation-5--Slide%20Deck-orange.svg)](EXECUTIVE_SUMMARY.md)

> **An end-to-end data analytics and business intelligence platform evaluating Sri Lanka's inbound tourism performance, crisis resilience, seasonal demand dynamics, and source market concentration across 2018–2025, powered by automated data pipelines and an interactive Streamlit decision platform.**

---

## 📌 Executive Summary *(Recruiter & Decision-Maker Fast Track)*

Between 2018 and 2025, Sri Lanka's tourism industry faced an unprecedented sequence of severe macroeconomic and geopolitical shocks:
1. **2019 Easter Sunday Attacks** (-18.0% immediate drop)
2. **2020–2021 Global COVID-19 Pandemic** (crashing to a historic low of **194,495 arrivals in 2021; -91.7% from 2018 baseline**)
3. **2022 Domestic Economic & Fuel Crisis**
4. **2023–2025 V-Shaped Rebound** culminating in **2,362,521 arrivals in 2025 (101.2% recovery)**, setting a new **all-time national record**.

### 🏆 Macro Performance Snapshot

| Strategic Metric | Baseline (2018) | Crisis Trough (2021) | Mid-Recovery (2023) | Full Rebound (2025) |
| :--- | :---: | :---: | :---: | :---: |
| **Annual International Arrivals** | 2,333,796 | 194,495 | 1,487,303 | **2,362,521** |
| **YoY Arrival Trajectory** | Baseline | -61.7% YoY | +106.6% YoY | **+15.1% YoY** |
| **Recovery Index (vs. 2018 Baseline)** | 100.0% | 8.3% | 63.7% | **101.2% (Record High)** |
| **Dominant Source Market** | India (424K) | India (56K) | India (302K) | **India (531K)** |
| **Peak Arrival Month** | December (253K) | Domestic / Restricted | December (210K) | **December (245K)** |
| **Top 5 Market Concentration** | 48.2% | 58.1% | 54.3% | **51.8%** |

---

## 🖥️ Interactive Decision Platform (`app.py`)

The project features a full-stack interactive dashboard engineered with **Streamlit** and **Plotly**, styled in an **Executive Dark Mode with Flame Orange Accents (`#f97316`)**:

```
Live Dashboard Structure
├── 🎛️ Dynamic Sidebar: Real-time time preset, year slider, continent & country selectors, month/season filters
├── 1️⃣ Shocks & Recovery: Annotated timeline with crisis callouts, YoY growth, and expandable yearly data table
├── 2️⃣ Top Countries: Pareto 80/20 market share chart, cumulative curves, and month-by-country seasonality heatmap
├── 3️⃣ Future Forecast: 2026–2028 baseline projections with interactive What-If scenario shock testing
├── 4️⃣ Hotel Planning: Dynamic hotel room demand calculator (length of stay, room occupancy) & monthly capacity bar chart
└── 5️⃣ Decision Center: Operational playbooks for hotels, airlines & tourism planners, plus 1-click Year-by-Year dataset downloads
```

### Key Interactive Features:
* **Fully Dynamic Visual Filters:** Filter sliders and preset dropdowns automatically adjust their date bounds dynamically whenever new data is added.
* **Pixel-Perfect Metric Cards:** Unified 136px card heights with comparative delta badges.
* **Defensive Data Guards:** Built-in safeguards preventing division-by-zero or empty-filter crashes.
* **Year-by-Year Data Downloader:** Allows instant export of filtered CSVs, individual year datasets, or the 1-page executive markdown deck.

---

## 🔄 Automated Ingestion & Cloud CI/CD Pipeline

To ensure the platform never becomes outdated, the project implements an **automated data pipeline**:

```
               [Official SLTDA Website]
                          │ (Annual Statistical Reports)
                          ▼
            [update_data.py Script]
             ├── Checks online publications
             ├── Standardizes country names (country_converter)
             ├── Maps continents & formats dates
             └── Saves master CSV & splits by_year/ files
                          │
                          ▼
       [GitHub Actions Workflow: auto_fetch.yml]
             ├── Runs scheduled check quarterly in the cloud
             ├── Commits new data: [Auto-update: appended latest data]
             └── Pushes to GitHub repository
                          │
                          ▼
         [Streamlit Community Cloud / Local App]
             └── Auto-reloads updated data with zero manual effort
```

### Automation Commands:
```bash
# Check current latest data status in database
python update_data.py --check

# View & export complete Year-by-Year summary table (with YoY growth)
python update_data.py --yearly

# Split master dataset into individual yearly CSV files in data/processed/by_year/
python update_data.py --split-years

# Ingest any newly downloaded SLTDA Excel or CSV file
python update_data.py --file path_to_report.xlsx
```

---

## 📊 Hero Visualizations

### 1. Crisis Impact & Recovery Timeline (2018–2025)
*Directly maps macroeconomic shocks, trough levels, and rebound velocity against the 2018 pre-crisis baseline.*

![Sri Lanka Tourism Crisis Timeline](outputs/figures/yearly_tourism_performance.png)

---

### 2. Executive Performance Dashboard (4-Panel Strategic View)
*Cross-sectional analytical breakdown covering crisis trajectories, Pareto market concentration, seasonality curves, and recovery velocity.*

![Executive Performance Dashboard](outputs/figures/final_tourism_analysis.png)

---

### 3. Monthly Seasonality & Off-Peak Demand Swings
*Highlights the 62% demand swing between December winter peaks and May–June monsoon troughs.*

![Monthly Seasonality Distribution](outputs/figures/monthly_seasonality.png)

---

### 4. Top 10 Source Markets & Cumulative Pareto Concentration
*Demonstrates market concentration where the top 5 countries account for over 51% of all inbound tourists.*

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

## 📓 Research & Analytics Notebooks

The analytical foundation of this project is organized across 4 modular Jupyter Notebooks in the `notebooks/` directory:

| Notebook | Focus | Key Methods & Deliverables |
| :--- | :--- | :--- |
| **`01_Data_Loading_and_Integration.ipynb`** | Multi-Year Data Wrangling | Automated ingestion of 8 years of SLTDA Excel reports, column harmonization, and schema unification. |
| **`02_Data_Quality_and_Cleaning.ipynb`** | Data Cleaning & Standardization | Anomaly detection, null imputation, zero-handling, and standardizing 200+ regions via `country_converter`. |
| **`03_Descriptive_Statistics.ipynb`** | Statistical Analysis | Summary statistics, skewness/kurtosis, distribution profiles, and seasonal variance metrics. |
| **`04_Overall_Tourism_Performance.ipynb`** | Strategic Analytics & ML Forecasting | Pareto 80/20 analysis, Time-Series Decomposition, SARIMAX forecasting with MAE validation, and What-If scenario simulations. |

---

## 📂 Project Architecture

```
Sri-Lanka-Tourism-Analytics/
│
├── .github/
│   └── workflows/
│       └── auto_fetch.yml            # Automated cloud pipeline (GitHub Actions)
│
├── .streamlit/
│   └── config.toml                   # Dark theme configuration & port settings
│
├── data/
│   ├── raw/                          # Official SLTDA yearly Excel reports (2018–2025)
│   ├── processed/
│   │   ├── tourism_arrivals_app_ready.csv    # Master validated dataset (18,396 rows)
│   │   ├── tourism_arrivals_clean.csv        # Cleaned baseline dataset
│   │   └── by_year/                          # Individual yearly CSV datasets (2018–2025)
│   └── reference/                    # Country mappings and continent definitions
│
├── notebooks/
│   ├── 01_Data_Loading_and_Integration.ipynb
│   ├── 02_Data_Quality_and_Cleaning.ipynb
│   ├── 03_Descriptive_Statistics.ipynb
│   └── 04_Overall_Tourism_Performance.ipynb
│
├── outputs/
│   ├── figures/                      # High-resolution publication figures (300 DPI)
│   │   ├── yearly_tourism_performance.png
│   │   ├── monthly_seasonality.png
│   │   ├── top_source_markets.png
│   │   └── final_tourism_analysis.png
│   └── tables/                       # Automated business summaries
│       ├── final_business_insights.csv
│       └── yearly_tourism_summary.csv
│
├── app.py                            # Streamlit Executive Decision Platform
├── update_data.py                    # Automated SLTDA Ingestion & Year-by-Year Pipeline
├── EXECUTIVE_SUMMARY.md              # 5-Slide Executive Pitch Deck
├── requirements.txt                  # Environment dependencies
├── LICENSE                           # MIT License
└── README.md                         # Primary project documentation
```

---

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Dashboard Framework:** Streamlit
* **Data Engineering & Wrangling:** Pandas, NumPy, OpenPyXL
* **Entity Standardization:** `country_converter` (ISO-3166 alpha-3 / short name mapping)
* **Visual Storytelling & Charts:** Plotly Graph Objects, Plotly Express, Seaborn, Matplotlib
* **Statistical Modeling & Forecasting:** SciPy, Statsmodels (SARIMAX, Seasonal Decomposition)
* **Automation & CI/CD:** GitHub Actions (cron scheduling, git automation)
* **Web Scraping:** Requests, BeautifulSoup4

---

## 🚀 Installation & Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/HimashMadushanka/Sri-Lanka-Tourism-Analytics.git
cd Sri-Lanka-Tourism-Analytics
```

### 2. Create and activate a virtual environment
```bash
# Windows:
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux:
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit Dashboard
```bash
streamlit run app.py
```
*Open your browser and navigate to `http://localhost:8501` to view the platform.*

---

## 👤 Author & Contact

* **Himash Madushanka**
* **Focus:** Data Analytics | Business Intelligence | Decision Science
* **Executive Pitch Deck:** [View 5-Slide Presentation Deck](EXECUTIVE_SUMMARY.md)
* **Repository:** [GitHub Repository](https://github.com/HimashMadushanka/Sri-Lanka-Tourism-Analytics)

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
