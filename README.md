# GrowSight
### Greenhouse Analytics & Decision-Support Platform

GrowSight is an end-to-end **greenhouse analytics portfolio project** designed to help growers identify production batches that need attention and investigate possible environmental contributors to plant loss—without needing to inspect every batch in person.

The finished local prototype brings together **Python, PostgreSQL, SQL, Google BigQuery, Power BI, live simulated temperature readings, and a locally hosted AI assistant**. It also includes historical weather enrichment and an exploratory machine-learning component.

> **Core question:** Which greenhouse batches need attention, and what environmental conditions might explain their losses?

**Project status:** Completed portfolio/demo prototype. It uses simulated greenhouse production and sensor data, not readings from deployed physical sensors. It is not a validated commercial greenhouse-control or predictive-alert system.

## At a glance

| Metric | Project result |
| --- | ---: |
| Simulated production batches | 150 |
| High-risk batches | 19 |
| Low-risk batches | 131 |
| Average batch loss rate (project snapshot) | ~6.80% |
| Crop species | 3 |
| Greenhouse zones | 3 |
| Simulated temperature update interval | ~5 seconds |

These figures are from the project's reference dataset and may vary with report filters or subsequent data updates.

## Features

### 1. Interactive Power BI dashboard

The dashboard supports greenhouse monitoring and investigation through multiple report pages:

- **Overview:** Total Batches, Batches Requiring Attention, Average Loss Rate, filters for crop species, greenhouse zone and risk level, plus monitoring cards.
- **Risk Drivers:** Visual exploration of temperature, irrigation and loss-rate patterns to help identify conditions worth investigating.
- **Batch Investigation:** Drill into a selected batch to review its zone, crop, temperature, irrigation, loss rate and risk classification.
- **Live Current Temperature:** A zone-filterable card displaying the latest temperature value supplied by the sensor simulation pipeline. The local demo was configured to update approximately every five seconds.
- **Average pH and Average EC:** Additional environmental metric cards included in the finished report.

The dashboard uses a dark theme with high-contrast green accents. Its risk labels are based on **observed batch losses**, not an independently validated prediction of future losses.

### 2. Simulated live sensor pipeline

A Python sensor simulator generates changing environmental observations for the three zones and stores readings in PostgreSQL's `sensor_readings` table. Fields include:

- Timestamp and zone ID
- Temperature (°C)
- Relative humidity (%)
- pH
- Electrical conductivity (EC)

**Current live display:** Temperature is the live-updating reading surfaced in Power BI. Other simulator fields support the broader local data pipeline; they should not be interpreted as confirmed live-updating Power BI visualizations.

This simulates a real monitoring workflow without requiring greenhouse hardware.

### 3. AskGrowSight: local AI assistant

AskGrowSight is a greenhouse-focused chatbot integrated into the Power BI experience through a custom visual. It uses:

- **Flask** for the local HTTP API (`POST /ask`)
- **Ollama** to run **Qwen3 4B** locally
- **PostgreSQL** connectivity through `psycopg2` to support database-aware responses
- A custom **Power BI visual** for entering questions and viewing answers

The assistant is designed to answer greenhouse and GrowSight questions, such as interpreting pH, EC, temperature and plant-loss thresholds, and to use project data where supported by its implemented database functions. Its responses are decision support, not autonomous greenhouse actions.

**Local-only setup:** The demonstrated API ran at `http://127.0.0.1:5000` and Ollama at `http://127.0.0.1:11434`. This is not a publicly hosted AI service. The API, database, and Ollama process need to be running for the assistant to work.

### 4. SQL analytics and batch risk classification

PostgreSQL is used for local storage, transformations, and analysis. BigQuery was also used as part of the warehouse and analytical workflow.

The project uses a dimensional design with:

| Table | Role |
| --- | --- |
| `staging_growth` | Original batch-level production records |
| `dim_species` | Crop information |
| `dim_zone` | Greenhouse zone information |
| `dim_date` | Date attributes |
| `fact_growth` | Production measurements |
| `sensor_readings` | Timestamped simulated environmental observations |

Key analytical objects include:

- `batch_risk_analysis` — computes plant-loss percentage and classifies risk.
- `top_risk_batches_by_zone` — ranks higher-loss batches within zones.
- `batch_risk_snapshot` — stored reporting snapshot.

**Final risk logic:**

```sql
CASE
    WHEN (plants_lost::numeric / NULLIF(plants_planted, 0)) * 100 >= 10
        THEN 'High Risk'
    ELSE 'Low Risk'
END
```

| Classification | Rule |
| --- | --- |
| High Risk | Loss rate ≥ 10% |
| Low Risk | Loss rate < 10% |

The finished project uses **two** categories: High Risk and Low Risk. There is no Medium Risk category.

SQL techniques used include joins, aggregation, `CASE`, views, CTEs, and window functions for ranking.

### 5. Historical weather enrichment

A Python integration retrieves historical weather information for Jerusalem using the **Open-Meteo API**. Greenhouse batch records were enriched with outside temperature, humidity and precipitation information for the simulated production period (February–July 2026).

Example enriched fields:

- `outside_temperature_c`
- `outside_humidity_percent`
- `precipitation_mm`

The purpose is to investigate possible relationships between outside weather and greenhouse performance, not to establish causation.

### 6. Exploratory machine learning

A Python/scikit-learn proof of concept explored classifying batches as High Risk or Low Risk using features such as greenhouse temperature and water usage. Logistic Regression was the primary model explored; Random Forest was also considered or tested during development.

The dataset is small and imbalanced (**19 high-risk cases out of 150**). Model evaluations therefore serve as a learning exercise, **not** proof of reliable real-world predictive accuracy. The Power BI risk classification is based on the explicit observed-loss rule above, not a deployed ML scoring service.

## Dataset

GrowSight analyzes **150 simulated production batches** across three species and zones.

| Species | Greenhouse zone |
| --- | --- |
| Tomato | North Glasshouse |
| Cucumber | South Tunnel |
| Pepper | Propagation Room |

Species and zones are separate dimensions; the table lists the three species and the three zone names for convenience, not one-to-one crop assignments.

Example batch fields include `batch_id`, crop species, zone, production date, plants planted, plants lost, irrigation volume, and greenhouse temperature.

## Selected findings from the simulated data

| Temperature group | Average loss rate |
| --- | ---: |
| Under 20°C | 6.51% |
| 20–25°C | 6.61% |
| 25–30°C | 5.67% |
| 30–35°C | 7.52% |
| 35°C and above | 14.22% |

The hottest temperature group had the highest observed average losses. This is a descriptive result of the simulated dataset; it does **not** demonstrate that heat caused those losses.

| Crop | Average loss rate |
| --- | ---: |
| Tomato | 5.60% |
| Cucumber | 5.91% |
| Pepper | 8.79% |

Pepper showed the highest average loss rate in the reference data.

## System overview

```text
Simulated greenhouse batches ──> PostgreSQL staging / warehouse ──> SQL risk analysis
              │                                  │                      │
              ├──> Python + Open-Meteo weather ──┘                      │
              └──> Exploratory ML                                     │
                                                                       v
                                                                Power BI report
                                                                       ^
Python sensor simulator ──> PostgreSQL sensor_readings ──> latest zone temperature

Power BI AskGrowSight custom visual ──> local Flask /ask API ──> Ollama (Qwen3 4B)
                                            │
                                            └──> PostgreSQL data queries

Google BigQuery: additional analytical storage / SQL work during development
```

## Technology stack

| Area | Technologies |
| --- | --- |
| Data preparation and simulation | Python, pandas, NumPy |
| Database and analytics | PostgreSQL, SQL, Google BigQuery |
| Data modeling | Staging tables, fact and dimension tables, SQL views |
| Business intelligence | Microsoft Power BI, DAX |
| Weather enrichment | Open-Meteo API, Python requests |
| ML proof of concept | scikit-learn |
| AI assistant | Flask, Ollama, Qwen3 4B, psycopg2 |
| Dashboard AI interface | Power BI custom visual, TypeScript / Power BI visuals tooling |

## Running the local prototype

The complete project relies on local services and project files. These instructions describe the **intended local workflow**; a one-command public install is not provided.

1. **Set up PostgreSQL.** Create the `growsight_warehouse` database, load the batch dataset, create the warehouse/risk-analysis objects, and create `sensor_readings`. Check that connection settings in the Python scripts match your local machine.
2. **Install Python dependencies.** The components use packages including `pandas`, `numpy`, `requests`, `scikit-learn`, `flask`, `flask-cors`, and `psycopg2-binary`. Install only what is required by the scripts you run.
3. **Run any batch-processing or weather-analysis scripts** needed to populate the local analytical data.
4. **Start the sensor simulator** to write changing readings to PostgreSQL. The file used during development was `sensor_simulator.py`.
5. **Install Ollama and the `qwen3:4b` model**, then ensure Ollama is running locally.
6. **Start the Flask assistant API** (`growsight_api.py` during development) and confirm that its `/ask` endpoint can answer a test question.
7. **Open the Power BI report** and confirm that its data connections, current-temperature card and AskGrowSight custom visual are configured for the local environment.

The exact scripts, Power BI file, custom visual package, and database setup files must be included in the repository before someone else can reproduce the full demo. **Do not assume that the README alone provides a turnkey installation.**

## Project limitations

- Production batches and live readings are **simulated**, not collected from an operating greenhouse.
- A batch is marked high risk **after** its observed loss percentage reaches 10%; this is not a forecast of future plant loss.
- The live dashboard component demonstrated is the **temperature reading**; the remaining environmental parameters are not claimed to be live Power BI metrics.
- The AI assistant runs through local services and only has the database access explicitly implemented in its code. Its answers should be checked before making growing decisions.
- The ML experiment is not production-validated and has substantial sample-size and class-imbalance limitations.
- The current prototype is intended for a local portfolio demonstration, not remote deployment or automatic actuation of greenhouse equipment.

## Possible future extensions

- Connect to physical greenhouse sensors.
- Extend real-time reporting to humidity, pH, EC and other sensor signals.
- Collect more historical batches and independently validate predictive models.
- Add authenticated deployment, operational monitoring, and alerting.
- Package a fully reproducible demo with setup scripts, anonymized sample data, screenshots, and a Power BI file.

## Why I built GrowSight

GrowSight applies data analytics to a real horticultural problem: translating scattered crop and environmental measurements into information growers can act on. The project combines hands-on greenhouse domain understanding with SQL, Python, dashboard development, simulated sensor integration, and practical work integrating a local language model into a data product.

**The result is a completed end-to-end portfolio prototype showing how greenhouse operations data can support earlier investigation and more informed decisions.**