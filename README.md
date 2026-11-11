# Helios: 10MW Solar Fleet Autonomous Reliability & Digital Twin Platform

[![CI/CD Pipeline](https://github.com/rajaraogurindapalli-gif/helios-renewables-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/rajaraogurindapalli-gif/helios-renewables-platform/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://python.org)
[![PyTorch: Deep Autoencoder](https://img.shields.io/badge/PyTorch-Autoencoder-EE4C2C.svg)](https://pytorch.org)
[![Tableau: Production Bound](https://img.shields.io/badge/Tableau-Operational%20Twin-E97627.svg)](https://public.tableau.com)
[![Streamlit: Reliability Copilot](https://img.shields.io/badge/Streamlit-Copilot%20UI-FF4B4B.svg)](src/agent/app.py)

H# Helios: 10MW Solar Fleet Digital Twin & Autonomous Reliability Copilot

An enterprise-grade renewable energy digital twin and prescriptive operations platform. Helios bridges executive operational business intelligence (Tableau) with an autonomous, physics-informed ReAct diagnostics copilot (Streamlit + LangChain) over a secure Cloudflare tunnel to eliminate operational silos between asset monitoring and field dispatch.

---

## Architecture Overview
                                   +----------------------------------------+
                                   |         OPERATIONAL TWIN               |
                                   |    Tableau Executive Dashboard         |
                                   |   (Weather-Normalized PR, Matrix)      |
                                   +-------------------+--------------------+
                                                       |
                                           Select Anomaly (INV-04)
                                         URL Action: ?inverter=INV-04
                                                       |
                                                       v
                                   +-------------------+--------------------+
                                   |      SECURE ACCESS LAYER               |
                                   |       Cloudflare HTTPS Tunnel          |
                                   +-------------------+--------------------+
                                                       |
                                                       v


+----------------------------------------------------------+----------------------------------------------------------+
|                                        HELIOS RELIABILITY AGENT RUNTIME                                            |
|                                                                                                                     |
|   +-----------------------+     +-------------------------------+     +-----------------------------------------+   |
|   |   Asset State Store   | --> | Autonomous ReAct Diagnostics  | <-- | Industrial RAG Corpus                   |   |
|   |  Real-time Telemetry  |     | (Root Cause Analysis Engine)  |     | (OEM Manuals & IEC-61724-1 Standards)   |   |
|   +-----------------------+     +---------------+---------------+     +-----------------------------------------+   |
|                                                 |                                                                   |
|                                                 v                                                                   |
|                                 +---------------+---------------+                                                   |
|                                 | Automated CMMS Work-Order Gen |                                                   |
|                                 | (P1 Ticket & Pre-curtailment) |                                                   |
|                                 +-------------------------------+                                                   |
+-------------------------------------------------------------------------------------------------------------



---

## Core Capabilities & Engineering Highlights

* **Tableau Executive Operational Twin:** Dynamic KPI BANs, Fixed LOD expressions, and thermal derating scatter matrices calculating real-time fleet generation, weather-normalized Performance Ratio (PR), and instantaneous PPA shortfall exposure.
* **Bi-Directional Contextual Handoff:** Seamless operational escalation using Tableau URL Actions passing dynamic asset query strings (`/?inverter=<Inverter Id>`) directly into the inference layer.
* **Autonomous ReAct Diagnostic Engine:** Multi-turn ReAct reasoning agent that parses live inverter telemetry against OEM thermal thresholds to identify IGBT junction overheating and fan bus subsystem failures.
* **Industrial RAG Integration:** Grounded diagnostic synthesis referencing manufacturer engineering manuals (`DOC-OEM-INV2500-CH08`) and utility performance standards (`DOC-IEC-61724-1`).
* **Automated CMMS Dispatch:** Instant generation of structured P1 work orders complete with pre-emptive curtailment setpoints (e.g., 15% thermal derate) to avert catastrophic plant trips.

---

## Validated Diagnostic Use Case (`INV-04`)

| Parameter | Operational Value | Threshold / Target | Status |
| :--- | :--- | :--- | :--- |
| **Asset Identifier** | `INV-04` (Inverter 04) | Fleet Asset ID | Target Selected |
| **Peak Heatsink Temp** | **122.5 °C** | 75.0 °C Nominal (85.0 °C Trip) | **CRITICAL OVERHEAT** |
| **Daylight Mean PR** | **78.9%** | $\ge 82.0\%$ Baseline | **Degraded** |
| **Thermal Derate Loss**| **4,381.1 kWh** | 0 kWh Baseline | **Revenue Loss** |
| **Projected Liability**| **$275.00 / hr** | SLA Limit $0.00 | **Contractual Breach** |
| **Prescriptive Action**| Clean louvers; replace 24V fan bus fuse; enforce 15% pre-emptive curtailment |
| **Automated CMMS** | Work Order Generated: `WO-HELIOS-INV-04-20261112040` |

## Repository Structure

```text
helios-renewables-platform/
├── README.md                      # Executive architecture & portfolio summary
├── SOP_OPERATIONAL_TWIN.md        # Standard Operating Procedure for full demo execution
├── requirements.txt               # Python runtime dependencies
├── tableau/
│   └── Helios_10MW_Solar_Fleet_Operational_Twin.twbx  # Packaged Tableau Dashboard
└── src/
    ├── config.py                  # Fleet parameters, thresholds, and runtime settings
    ├── telemetry_generator.py     # Production telemetry simulator
    └── agent/
        ├── app.py                 # Streamlit web interface and URL routing
        └── helios_agent.py        # ReAct agent loop and industrial RAG chain

---
## Artifacts
### Tableau Operational Twin
- **File:** `tableau/Helios_10MW_Solar_Fleet_Operational_Twin.twbx`
- **Description:** Complete executive operational dashboard featuring weather-normalized PR tracking, thermal derating scatter matrices, and dynamic URL actions triggering the autonomous Streamlit diagnostics copilot.

## Quickstart: Running the Live Copilot
https://fit-los-judges-claimed.trycloudflare.com/?inverter=


```bash
git clone https://github.com/rajaraogurindapalli-gif/helios-renewables-platform.git
cd helios-renewables-platform
pip install -r requirements.txt
streamlit run src/agent/app.py
```
