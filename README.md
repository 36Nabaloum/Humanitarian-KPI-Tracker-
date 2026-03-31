# 🌍 Humanitarian KPI Tracker — Power BI Dashboard

> **Author:** NABALOUM Emile | Data Analyst & BI Specialist
> **Contact:** emi.nabaloum@gmail.com | +226 67 07 82 76
> **Portfolio:** [github.com/nabaloum-emile/portfolio](https://github.com/nabaloum-emile/portfolio)

---

## 📌 Project Overview

A production-grade **Power BI dashboard** for monitoring humanitarian programme performance across multiple countries in the Sahel region. Built to replicate real-world reporting requirements from organisations such as **USAID, UNICEF, OCHA, IRC, and SPONG**.

This project demonstrates end-to-end BI competency:
- **Data modelling** (star schema with 5 tables)
- **Advanced DAX** (52 measures across 7 categories)
- **Power Query M** (ETL pipelines with computed columns)
- **RLS** (Row-Level Security for multi-org access control)
- **Automated reporting** (scheduled refresh simulation)

---

## 📊 Dashboard Pages

| Page | Description | Key Visuals |
|------|-------------|-------------|
| **1. Overview** | Executive KPI summary | 6 KPI cards, trend line, map |
| **2. Beneficiaries** | Who is being reached | Demographics, gender parity, timeline |
| **3. Activity Performance** | Are targets being met? | Achievement matrix, RANKX table |
| **4. Financial Tracking** | Budget vs spend | Waterfall chart, funding gap |
| **5. Incident Context** | Security & crisis events | Severity heatmap, affected pop |
| **6. Donor Report** | Per-donor view (RLS) | Filtered by donor login |

---

## 🗂 Data Model — Star Schema

```
                    ┌──────────────┐
                    │  dim_date    │
                    │  (731 rows)  │
                    └──────┬───────┘
                           │ StartDate (active)
                           │ EndDate (inactive — USERELATIONSHIP)
              ┌────────────┴───────────────┐
              │                            │
    ┌─────────▼──────────┐    ┌────────────▼───────────┐
    │   activities        │    │   incidents             │
    │   (300 rows)        │    │   (150 rows)            │
    │   MAIN FACT TABLE   │    │   CONTEXT FACT          │
    └─────────────────────┘    └─────────────────────────┘

    ┌─────────────────────┐    ┌─────────────────────────┐
    │   beneficiaries     │    │   funding                │
    │   (800 rows)        │    │   (80 rows)              │
    │   DIMENSION/FACT    │    │   FINANCIAL FACT         │
    └─────────────────────┘    └─────────────────────────┘
```

### Relationships
| From | To | Type | Active |
|------|----|------|--------|
| `dim_date[Date]` | `activities[StartDate]` | Many-to-one | ✅ Yes |
| `dim_date[Date]` | `activities[EndDate]` | Many-to-one | ❌ No (USERELATIONSHIP) |

> All other filtering is handled via disconnected slicers and CALCULATE with explicit FILTER expressions — a deliberate design choice for maximum flexibility.

---

## ⚡ DAX Measures — Highlights

### Beneficiary Measures
```dax
-- Total beneficiaries
Total Beneficiaries = COUNTROWS(beneficiaries)

-- Gender parity KPI
% Female = DIVIDE([Female Beneficiaries], [Total Beneficiaries], 0)

-- Year-over-Year growth
Beneficiaries YoY Growth % =
VAR CurrentPeriod = [Total Beneficiaries]
VAR PrevPeriod    = [Beneficiaries SPLY]
RETURN DIVIDE(CurrentPeriod - PrevPeriod, PrevPeriod, 0)
```

### Performance Measures
```dax
-- Core achievement rate
Achievement Rate % =
DIVIDE([Total Achieved], [Total Target], 0)

-- Country ranking by performance
Country Rank =
RANKX(
    ALL(activities[Country]),
    [Achievement Rate %], , DESC, DENSE
)

-- Rolling 3-month trend
Achievement Rate 3M Rolling =
CALCULATE(
    [Achievement Rate %],
    DATESINPERIOD(dim_date[Date], LASTDATE(dim_date[Date]), -3, MONTH)
)
```

### Financial Measures
```dax
-- Budget utilization with KPI status
Budget KPI Status =
VAR Rate = [Budget Utilization %]
RETURN SWITCH(TRUE(),
    Rate >= 0.90, -1,   -- Red: overspending
    Rate >= 0.70,  1,   -- Green: on track
    0                   -- Amber: underspending
)

-- Cost efficiency
Cost Per Beneficiary = DIVIDE([Total Spent], [Total Beneficiaries], 0)
```

> 📄 See [`dax/measures_complete.dax`](./dax/measures_complete.dax) for all **52 measures** with full comments.

---

## 🔄 Power Query — Key Transformations

### activities table
```m
// Achievement Rate computed column
AddedAchRate = Table.AddColumn(RemovedZeroTarget, "AchievementRate",
    each if [Target] = 0 then 0
         else Number.Round([Achieved] / [Target], 4),
    type number
)

// Budget variance flag
AddedOverBudget = Table.AddColumn(AddedBudgetVar, "IsOverBudget",
    each [Spent_USD] > [Budget_USD], type logical
)
```

> 📄 See [`dax/power_query_transformations.m`](./dax/power_query_transformations.m) for all 5 table queries.

---

## 🔐 Row-Level Security (RLS)

Three security roles are configured:

| Role | Filter Logic | Use Case |
|------|-------------|----------|
| `Country Manager` | `activities[Country] = USERPRINCIPALNAME()` | Country-level staff |
| `Sector Lead` | Sector lookup via UserRoles table | Programme sector managers |
| `Donor View` | Donor lookup via UserRoles table | Donor reporting portal |

---

## 📁 File Structure

```
project1_powerbi/
│
├── data/
│   ├── beneficiaries.csv     # 800 rows — beneficiary registry
│   ├── activities.csv        # 300 rows — programme activities & KPIs
│   ├── funding.csv           #  80 rows — donor funding flows
│   ├── incidents.csv         # 150 rows — security & crisis events
│   ├── dim_date.csv          # 731 rows — date dimension (2024-2025)
│   └── generate_data.py      # Python script to regenerate datasets
│
├── dax/
│   ├── measures_complete.dax          # All 52 DAX measures with comments
│   └── power_query_transformations.m  # All 5 Power Query M scripts
│
├── docs/
│   ├── README.md             # This file
│   ├── dashboard_spec.md     # Dashboard page specifications
│   └── data_dictionary.md    # Column definitions for all tables
│
└── screenshots/
    ├── overview_page.png
    ├── beneficiaries_page.png
    ├── performance_matrix.png
    └── financial_page.png
```

---

## 🚀 How to Reproduce

### Prerequisites
- Power BI Desktop (free) — [download here](https://powerbi.microsoft.com/desktop/)
- Python 3.x (optional — to regenerate data)

### Steps
1. **Clone this repo**
   ```bash
   git clone https://github.com/nabaloum-emile/portfolio.git
   cd portfolio/project1_powerbi
   ```

2. **Open Power BI Desktop** → `Get Data` → `CSV`

3. **Load all 5 CSV files** from the `data/` folder

4. **Open Transform Data** → for each table, paste the corresponding M code from `dax/power_query_transformations.m`

5. **Close & Apply**

6. **Create Relationships** as described in the Data Model section above

7. **Create a Measures table**: `Enter Data` → name it `_Measures` → Close

8. **Copy all DAX measures** from `dax/measures_complete.dax` into the Measures table

9. **Build visuals** following the page specifications in `docs/dashboard_spec.md`

---

## 📈 Key Results Achieved (Simulated)

| Metric | Value |
|--------|-------|
| Total Beneficiaries | 800 |
| Average Achievement Rate | ~72% |
| Budget Utilisation | ~68% |
| Countries covered | 5 |
| Sectors covered | 7 |
| Donors tracked | 7 |
| Activities monitored | 300 |

---

## 🎯 Real-World Impact (from actual experience)

This dashboard is based on real solutions delivered at:
- **SPONG / OCHA** — dashboards adopted for emergency planning (Burkina Faso, 2024-2025)
- **AUXFIN / USAID** — automated reporting reducing cycle time by **40%** (2025)
- **IRC** — KPI tracking for 3 projects (NORAD, GFFO, BHA) (2023-2024)

---

## 🤝 Connect

| Channel | Link |
|---------|------|
| Email | emi.nabaloum@gmail.com |
| LinkedIn | [linkedin.com/in/nabaloum-emile](https://linkedin.com) |
| GitHub | [github.com/nabaloum-emile](https://github.com) |
| Phone/WhatsApp | +226 67 07 82 76 |

---

*Part of the [NABALOUM Emile Data Portfolio](../README.md) — Senior Data Analyst & BI Specialist, Burkina Faso*
