# Helios: 10MW Solar Fleet Autonomous Reliability & Digital Twin Platform

**Description**  
Enterprise-grade renewable-energy digital-twin and prescriptive-operations platform that connects a Tableau executive operational dashboard with an autonomous, physics-informed ReAct diagnostics copilot (Streamlit + LangChain) via a secure Cloudflare tunnel. It eliminates silos between asset monitoring and field dispatch for a 10 MW solar fleet, delivering weather-normalized performance ratios, automated diagnostics, and CMMS work-order generation.

[![CI/CD Pipeline](https://github.com/rajaraogurindapalli-gif/helios-renewables-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/rajaraogurindapalli-gif/helios-renewables-platform/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://python.org)
[![PyTorch: Deep Autoencoder](https://img.shields.io/badge/PyTorch-Autoencoder-EE4C2C.svg)](https://pytorch.org)
[![Tableau: Production Bound](https://img.shields.io/badge/Tableau-Operational%20Twin-E97627.svg)](https://public.tableau.com)
[![Streamlit: Reliability Copilot](https://img.shields.io/badge/Streamlit-Copilot%20UI-FF4B4B.svg)](src/agent/app.py)

## Tech Stack
- **Tableau** (executive operational twin, weather-normalized PR, thermal matrices, URL actions)
- **Streamlit** + **LangChain** (ReAct diagnostics copilot)
- **Python** (telemetry simulation, agent runtime)
- **Cloudflare Tunnel** (secure bi-directional access)
- **PyTorch** (deep autoencoder elements)
- **Industrial RAG** (OEM manuals, IEC-61724-1 standards)
- **Docker** / CI/CD (GitHub Actions)

## Architecture Overview
(Existing architecture diagram preserved in the repository)

## Core Capabilities & Engineering Highlights

* **Tableau Executive Operational Twin:** Dynamic KPI BANs, Fixed LOD expressions, and thermal derating scatter matrices calculating real-time fleet generation, weather-normalized Performance Ratio (PR), and instantaneous PPA shortfall exposure.
* **Bi-Directional Contextual Handoff:** Seamless operational escalation using Tableau URL Actions passing dynamic asset query strings (`/?inverter=<Inverter Id>`) directly into the inference layer.
* **Autonomous ReAct Diagnostic Engine:** Multi-turn ReAct reasoning agent that parses live inverter telemetry against OEM thermal thresholds to identify IGBT junction overheating and fan bus subsystem failures.
* **Industrial RAG Integration:** Grounded diagnostic synthesis referencing manufacturer engineering manuals and utility performance standards.
* **Automated CMMS Dispatch:** Instant generation of structured P1 work orders complete with pre-emptive curtailment setpoints.

## Validated Diagnostic Use Case (`INV-04`)

| Parameter | Operational Value | Threshold / Target | Status |
| :--- | :--- | :--- | :--- |
| **Asset Identifier** | `INV-04` (Inverter 04) | Fleet Asset ID | Target Selected |
| **Peak Heatsink Temp** | **122.5 °C** | 75.0 °C Nominal (85.0 °C Trip) | **CRITICAL OVERHEAT** |
| **Daylight Mean PR** | **78.9%** | ≥ 82.0% Baseline | **Degraded** |
| **Thermal Derate Loss**| **4,381.1 kWh** | 0 kWh Baseline | **Revenue Loss** |
| **Projected Liability**| **$275.00 / hr** | SLA Limit $0.00 | **Contractual Breach** |
| **Prescriptive Action**| Clean louvers; replace 24V fan bus fuse; enforce 15% pre-emptive curtailment |
| **Automated CMMS** | Work Order Generated: `WO-HELIOS-INV-04-20261112040` |

## Repository Structure

```text
helios-renewables-platform/
├── README.md
├── SOP_OPERATIONAL_TWIN.md
├── requirements.txt
├── tableau/
│   └── Helios_10MW_Solar_Fleet_Operational_Twin.twbx
└── src/
    ├── config.py
    ├── telemetry_generator.py
    └── agent/
        ├── app.py
        └── helios_agent.py
```

## Artifacts
### Tableau Operational Twin
- **File:** `tableau/Helios_10MW_Solar_Fleet_Operational_Twin.twbx`
- **Description:** Complete executive operational dashboard featuring weather-normalized PR tracking, thermal derating scatter matrices, and dynamic URL actions triggering the autonomous Streamlit diagnostics copilot.

## Quickstart: Running the Live Copilot
Demo URL: https://fit-los-judges-claimed.trycloudflare.com/?inverter=

```bash
git clone https://github.com/rajaraogurindapalli-gif/helios-renewables-platform.git
cd helios-renewables-platform
pip install -r requirements.txt
streamlit run src/agent/app.py
```
