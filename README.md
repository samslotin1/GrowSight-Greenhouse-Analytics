# GrowSight 🌱
### Greenhouse Growth & Risk Analytics Platform

GrowSight is a data analytics project designed to analyze greenhouse crop performance, identify high-risk growing batches, and explore environmental factors that may contribute to plant loss.

The project combines **SQL, PostgreSQL, BigQuery, Python, APIs, machine learning, and Power BI** into a small end-to-end analytics workflow.

The main goal is to answer a practical greenhouse management question:

> **Which growing batches require attention, and what environmental factors may be contributing to plant loss?**

---

# Project Overview

GrowSight simulates greenhouse production data across multiple crop species and growing zones.

The project analyzes:

- Plant loss rates
- Temperature
- Irrigation
- Greenhouse zones
- Crop species
- High-risk production batches
- External weather conditions

The final output is an interactive **Power BI dashboard** that allows users to investigate greenhouse performance and identify potentially problematic batches.

---

# Technologies Used

## Data & SQL

- PostgreSQL
- SQL
- BigQuery
- Star schema / dimensional modeling

## Python

- Python
- pandas
- NumPy
- scikit-learn
- API requests

## Visualization

- Power BI

## External Data

- Open-Meteo Weather API

---

# Dataset

The GrowSight dataset contains **150 simulated greenhouse production batches**.

Each batch contains information including:

- Batch ID
- Crop species
- Greenhouse zone
- Plants planted
- Plants lost
- Irrigation amount
- Greenhouse temperature
- Production date

The crops included are:

- Tomato
- Cucumber
- Pepper

The greenhouse zones include:

- North Glasshouse
- South Tunnel
- Propagation Room

---

# Data Architecture

GrowSight uses a simple dimensional warehouse structure.

## Dimension Tables

### `dim_species`

Contains information about crop species.

### `dim_zone`

Contains greenhouse zone information.

### `dim_date`

Contains date-related attributes.

## Fact Table

### `fact_growth`

Stores greenhouse batch measurements including:

- Plants planted
- Plants lost
- Water usage
- Temperature
- Species
- Zone
- Date

A staging table was used before loading records into the warehouse.

### `staging_growth`

The staging dataset contains the original batch-level greenhouse records before transformation.

---

# SQL Analysis

SQL was used to clean, transform, classify, and analyze greenhouse production data.

Key SQL techniques used include:

- Aggregate functions
- `GROUP BY`
- `HAVING`
- `CASE`
- Views
- CTEs
- Window functions
- Ranking
- Risk classification

---

# Risk Classification

Batch risk was calculated using plant loss rate.

```sql
loss_rate_percent =
plants_lost / plants_planted * 100
```

Batches were classified as:

```text
High Risk: loss rate >= 10%

Low Risk: loss rate < 10%
```

The analysis identified:

- **150 total batches**
- **19 high-risk batches**
- **6.80% average loss rate**

---

# SQL Views

Several SQL views were created to support the analysis.

## `batch_risk_analysis`

Calculates batch loss rate and assigns a risk level.

Important fields include:

- `batch_id`
- `loss_rate_percent`
- `risk_level`

---

## `top_risk_batches_by_zone`

Ranks the highest-risk batches inside each greenhouse zone.

Window functions were used to rank batches and identify the top risk cases.

---

## `batch_risk_snapshot`

Stores a snapshot of the batch risk analysis for reporting and dashboard use.

---

# Temperature Analysis

Temperature was grouped into categories to investigate its relationship with plant loss.

Observed average loss rates:

| Temperature Range | Average Loss Rate |
|---|---:|
| Under 20°C | 6.51% |
| 20–25°C | 6.61% |
| 25–30°C | 5.67% |
| 30–35°C | 7.52% |
| 35°C+ | 14.22% |

The highest loss rate occurred when greenhouse temperatures exceeded **35°C**.

This suggests extreme heat may be associated with increased crop loss in the simulated dataset.

---

# Crop Analysis

Average loss rate by species:

| Species | Average Loss Rate |
|---|---:|
| Tomato | 5.60% |
| Cucumber | 5.91% |
| Pepper | 8.79% |

Pepper showed the highest average plant loss rate among the three crops.

---

# Weather API Integration

GrowSight integrates external weather data using the **Open-Meteo API**.

Weather data was retrieved for Jerusalem for the production period.

The API provides:

- Outside temperature
- Precipitation
- Relative humidity

Python was used to retrieve and transform the API data before merging it with greenhouse batch records.

The resulting dataset contains greenhouse measurements alongside external weather conditions.

Example fields include:

```text
outside_temperature_c
outside_humidity_percent
precipitation_mm
```

This allows greenhouse performance to be compared with external environmental conditions.

---

# Machine Learning

A small machine-learning prototype was created to explore whether batch risk could be classified using environmental features.

## Target

A batch was classified as:

```text
1 = High Risk
0 = Low Risk
```

High risk was defined as:

```text
loss_rate >= 10%
```

## Features

The initial model used features including:

- Greenhouse temperature
- Irrigation / water usage

## Models

Two models were tested:

- Logistic Regression
- Random Forest

The models were compared using:

- Confusion matrix
- Precision
- Recall
- Classification report

---

# Machine Learning Limitations

The machine-learning portion of GrowSight is intentionally a **proof of concept**.

The dataset contains only 150 records and just 19 high-risk cases.

This creates a significant class imbalance.

Because of the limited dataset, the model should not be interpreted as a production-ready prediction system.

Future versions of GrowSight could improve the model using:

- Larger datasets
- Additional environmental variables
- Greenhouse humidity
- Light levels
- Soil measurements
- Crop age
- Fertilizer data
- More historical growing cycles

---

# Power BI Dashboard

The GrowSight Power BI report provides an interactive interface for exploring greenhouse performance.

The dashboard contains multiple pages.

---

## Overview

The Overview page provides high-level greenhouse performance metrics.

Key KPIs include:

- Total Batches
- Batches Requiring Attention
- Average Loss Rate

Users can filter the dashboard using:

- Species
- Zone
- Risk Level

---

## Risk Drivers

The Risk Drivers page allows users to explore relationships between environmental conditions and plant loss.

One of the primary visualizations compares:

```text
Temperature
vs.
Loss Rate
```

This helps identify conditions associated with higher batch risk.

---

## Batch Investigation

The Batch Investigation page allows users to inspect individual greenhouse batches.

Users can examine batch-level information including:

- Species
- Zone
- Temperature
- Irrigation
- Loss rate
- Risk classification

This allows potentially problematic batches to be investigated in more detail.

---

# Key Findings

The analysis produced several notable observations.

### 1. Extreme temperatures were associated with higher loss

Batches exposed to temperatures above **35°C** had an average loss rate of approximately **14.22%**, substantially higher than other temperature ranges.

### 2. Pepper had the highest average crop loss

Pepper batches showed an average loss rate of approximately **8.79%**.

### 3. Most batches were not classified as high risk

Out of 150 batches:

```text
19 were classified as High Risk
131 were classified as Low Risk
```

### 4. Environmental conditions may help identify risky batches

Temperature and irrigation showed some relationship with plant loss, although the dataset is too small to make strong predictive conclusions.

---

# Project Workflow

The GrowSight workflow follows this process:

```text
Greenhouse Data
      ↓
PostgreSQL Staging
      ↓
Data Warehouse
      ↓
SQL Analysis
      ↓
BigQuery
      ↓
Python Analysis
      ↓
Weather API
      ↓
Machine Learning
      ↓
Power BI Dashboard
```

---

# Repository Structure

A suggested GitHub repository structure:

```text
GrowSight/
│
├── README.md
│
├── data/
│   ├── staging_growth.csv
│   └── weather_enriched_growth.csv
│
├── sql/
│   ├── create_tables.sql
│   ├── insert_data.sql
│   ├── risk_analysis.sql
│   └── analysis_queries.sql
│
├── python/
│   ├── weather_api.py
│   └── ml_risk_model.py
│
├── powerbi/
│   └── GrowSight.pbix
│
├── screenshots/
│   ├── overview.png
│   ├── risk_drivers.png
│   └── batch_investigation.png
│
└── presentation/
    └── GrowSight_Presentation.pdf
```

---

# How to Run the Project

## 1. Database

Create the PostgreSQL database and run the SQL scripts inside the `sql` directory.

Example order:

```text
create_tables.sql
insert_data.sql
risk_analysis.sql
analysis_queries.sql
```

---

## 2. Python Environment

Install the required Python packages.

```bash
pip install pandas numpy scikit-learn requests
```

---

## 3. Weather API

Run:

```bash
python weather_api.py
```

This retrieves weather data and merges it with the greenhouse batch dataset.

---

## 4. Machine Learning

Run:

```bash
python ml_risk_model.py
```

The script trains and evaluates the machine-learning models used in the proof-of-concept risk classification.

---

## 5. Power BI

Open:

```text
GrowSight.pbix
```

in Microsoft Power BI Desktop.

Use the dashboard filters to explore batch performance by species, greenhouse zone, and risk level.

---

# Future Improvements

Future versions of GrowSight could include:

- Real greenhouse sensor data
- Larger historical datasets
- Humidity monitoring
- Soil moisture
- Light intensity
- Fertilizer information
- Automated anomaly detection
- Improved machine-learning models
- Real-time greenhouse monitoring
- Automated risk alerts

---

# Project Purpose

GrowSight was developed as a data analytics portfolio project demonstrating the ability to combine:

- SQL
- relational databases
- dimensional modeling
- Python
- API integration
- machine learning
- data visualization
- business-oriented analytics

The project is designed to demonstrate an end-to-end analytical workflow rather than a production greenhouse management system.
