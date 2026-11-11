# Helios: 10MW Solar Fleet Autonomous Reliability & Digital Twin Platform

[![CI/CD Pipeline](https://github.com/rajaraogurindapalli-gif/helios-renewables-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/rajaraogurindapalli-gif/helios-renewables-platform/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://python.org)
[![PyTorch: Deep Autoencoder](https://img.shields.io/badge/PyTorch-Autoencoder-EE4C2C.svg)](https://pytorch.org)
[![Tableau: Production Bound](https://img.shields.io/badge/Tableau-Operational%20Twin-E97627.svg)](https://public.tableau.com)
[![Streamlit: Reliability Copilot](https://img.shields.io/badge/Streamlit-Copilot%20UI-FF4B4B.svg)](src/agent/app.py)

Helios is an **Industry 5.0 Agentic Digital Twin** built for continuous 10MW utility-scale photovoltaic fleets (4x 2.5MW central inverters). It replaces static telemetry thresholds with a closed-loop reliability pipeline: **Physics Engine -> BigQuery Medallion Lakehouse -> PyTorch Autoencoder -> Autonomous ReAct & Industrial RAG Agent -> Predictive Horizons & CMMS Memory**.

---

## Core Operational Metrics & Capabilities

* **Fleet Architecture:** 10 MW Utility Fleet (4x 2.5 MW central inverter blocks: INV-01, INV-02, INV-03, INV-04).
* **Deep Anomaly Isolation:** PyTorch Deep Autoencoder isolates incipient thermal breakdown with **0.095404 MSE** against the **tau = 0.00074** healthy baseline.
* **Autonomous Reliability Copilot:** ReAct agent grounded in OEM engineering manuals (DOC-OEM-INV2500-CH08) and PPA contractual tariffs (DOC-PPA-PENALTY-GRID).
* **Financial Risk Quantification:** Real-time revenue loss calculation ($0.075/kWh base tariff + $0.035/kWh grid deviation penalty = **$343.09** total exposure).
* **Predictive Asset Horizons:**
  * 24-hour day-ahead solar yield forecasting calibrated to **0.56% WAPE**.
  * Real-time thermal drift velocity (dT/dt) projecting time-to-trip before the 85 C hardware shutdown limit.
* **Episodic CMMS Memory:** Closed-loop maintenance tracking with field technician sign-offs and auditable resolution histories.
* **Shift Handover Summaries:** One-click executive handover memos summarizing fleet-wide PR, derate drag, and open P1 tickets.

---

## Quickstart: Running the Live Copilot

```bash
git clone https://github.com/rajaraogurindapalli-gif/helios-renewables-platform.git
cd helios-renewables-platform
pip install -r requirements.txt
streamlit run src/agent/app.py
```
