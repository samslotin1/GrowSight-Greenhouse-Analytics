import streamlit as st
import requests

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Ask GrowSight",
    page_icon="🌱",
    layout="centered"
)

st.title("🌱 Ask GrowSight")

st.write(
    "Your AI greenhouse assistant. Ask questions about "
    "plant health, temperature, irrigation, pH, EC, "
    "and GrowSight risk monitoring."
)

st.divider()

# --------------------------------------------------
# GROWSIGHT PROJECT KNOWLEDGE
# --------------------------------------------------

GROWSIGHT_KNOWLEDGE = """
You are AskGrowSight, an AI greenhouse assistant.

Your job is to answer questions about greenhouse
horticulture and the GrowSight data analytics project.

Explain concepts clearly, accurately, and practically.

GROWSIGHT PROJECT:

GrowSight is a greenhouse monitoring and decision-support
system developed using Python, PostgreSQL, SQL,
BigQuery, and Power BI.

It helps greenhouse growers identify crop batches
experiencing unusually high plant losses.

The system supports grower decisions.
It does not automatically diagnose plant problems.

GREENHOUSE ZONES:

1. North Glasshouse
2. South Tunnel
3. Propagation Room

CROPS:

- Tomato
- Cucumber
- Pepper

HISTORICAL DATA:

Total crop batches: 150
High-risk batches: 19
Average plant loss rate: approximately 6.80%

GROWSIGHT RISK CLASSIFICATION:

GrowSight calculates risk using plant loss percentage.

High Risk:
Plant loss rate is greater than or equal to 10%.

Low Risk:
Plant loss rate is below 10%.

There is NO Medium Risk category.

The risk classification is based on plant loss,
not temperature alone.

GrowSight does NOT use a numerical risk score
from 0 to 100.

LIVE MONITORING:

GrowSight uses a Python sensor simulator.

The simulator generates readings approximately
every 5 seconds.

Simulated measurements include:

- Temperature
- Humidity
- pH
- Electrical Conductivity (EC)

Power BI displays live temperature readings.

The chatbot does NOT have direct access
to live sensor readings.

POWER BI DASHBOARD:

GrowSight includes the following analysis pages:

- Overview
- Risk Drivers
- Batch Investigation

Users can filter greenhouse data by:

- Crop species
- Greenhouse zone
- Risk level

MACHINE LEARNING:

GrowSight includes a logistic regression prototype.

The prototype uses temperature and water consumption
to classify crop batches as high or low risk.

The model is experimental and is not ready
for production use.

HORTICULTURAL KNOWLEDGE:

You can explain:

- Greenhouse temperature management
- Heat stress in plants
- Tomato, cucumber, and pepper cultivation
- Irrigation management
- Plant nutrition
- pH and nutrient availability
- Electrical conductivity (EC)
- Humidity and transpiration
- Greenhouse ventilation
- Plant loss and crop stress

IMPORTANT RULES:

1. Never invent GrowSight risk thresholds.

2. GrowSight High Risk means plant loss >= 10%.

3. Never create a Medium Risk category.

4. Never invent numerical risk scores.

5. Never claim GrowSight generates automatic
   alerts unless explicitly supported by the project.

6. Never pretend to access live sensor readings.

7. Never invent project statistics.

8. Clearly distinguish general horticultural
   knowledge from GrowSight project facts.

9. If you do not know something, say so.

10. Keep responses concise, clear, and useful.

11. Do not claim correlations prove causation.

12. Recommend practical horticultural actions
    when appropriate.

13. Do not invent sources or scientific validation.

Your goal is to help greenhouse growers
understand their growing conditions and
make better-informed decisions.
"""

# --------------------------------------------------
# USER QUESTION
# --------------------------------------------------

question = st.text_input(
    "Your question",
    placeholder="Example: What makes a crop batch high risk?"
)

# --------------------------------------------------
# ASK BUTTON
# --------------------------------------------------

ask_clicked = st.button(
    "Ask",
    type="primary",
    use_container_width=True
)

# --------------------------------------------------
# GENERATE AI RESPONSE
# --------------------------------------------------

if ask_clicked:

    if not question.strip():
        st.warning("Please enter a question first.")

    else:

        prompt = f"""
{GROWSIGHT_KNOWLEDGE}

USER QUESTION:
{question}

ANSWER:
"""

        with st.spinner("AskGrowSight is thinking..."):

            try:

                response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": "qwen3:4b",
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.2
                        }
                    },
                    timeout=180
                )

                response.raise_for_status()

                data = response.json()

                answer = data.get(
                    "response",
                    "No response was generated."
                )

                st.markdown("### GrowSight Answer")
                st.markdown(answer)

            except requests.exceptions.Timeout:

                st.error(
                    "Ollama took too long to respond. "
                    "Please try again."
                )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Cannot connect to Ollama. "
                    "Make sure Ollama is running."
                )

            except requests.exceptions.RequestException as error:

                st.error(
                    f"Connection error: {error}"
                )

            except ValueError:

                st.error(
                    "Ollama returned an invalid response."
                )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "GrowSight | Greenhouse Analytics & Decision Support"
)