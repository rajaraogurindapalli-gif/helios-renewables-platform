# Technical Case Study: Helios Industrial Renewable Energy Platform
**Real-Time IoT Telemetry Streaming, Medallion Lakehouse, PyTorch Fault Isolation & Executive Digital Twin**

---

## 1. Executive Summary
Utility-scale solar installations face chronic energy yield losses from unmonitored component degradation, primarily insulated-gate bipolar transistor (IGBT) thermal choking and array soiling. Traditional supervisory control and data acquisition (SCADA) platforms alert operators only after hard operational thresholds or breaker trip sequences occur.

The **Helios Industrial Platform** implements an end-to-end digital twin architecture for a 10 MW ground-mounted solar PV installation comprising four 2.5 MW central inverters. Built on Google Cloud Platform (GCP) and BigQuery, the system processes continuous 15-minute operational telemetry, enforces data quality via a Medallion Lakehouse, isolates silent thermal anomalies using an unsupervised PyTorch Deep Autoencoder (dynamic threshold tau = 0.00074), predicts day-ahead generation with 0.56% WAPE via GBDT, and serves an interactive digital twin in Tableau.

---

## 2. Edge Physics & Telemetry Modeling
The edge simulator models environmental conditions and electrical conversion using standard solar engineering formulations:

1. **Diurnal Solar Irradiance and Ambient Temperature:**
   Modeled across active daylight windows (06:00 to 18:30) using sinusoidal zenith angles with peak irradiance G_peak = 980 W/m² and ambient temperature cycling between 22°C and 42°C.

2. **Module Surface Temperature:**
   T_module = T_ambient + (Irradiance * 0.03) + epsilon

3. **IEC 61724-1 Temperature-Corrected DC Power Derating:**
   Photovoltaic efficiency degrades with module heating beyond Standard Test Conditions (STC, 25°C):
   gamma = -0.4% / °C = -0.004
   P_dc_ideal = (Irradiance / 1000.0) * P_rated * [1 - 0.004 * max(0, T_module - 25.0)]

4. **Inverter Heatsink Thermal Choking (INV-03 Anomaly Injection):**
   Under high irradiance (Irradiance > 600 W/m²), inverter cooling degradation triggers a +19.5°C heatsink temperature excursion. Crossing 62°C forces internal IGBT protection derating, reducing nominal conversion efficiency by 35% and flagging diagnostic fault code `ERR-IGBT-OVERTEMP`.

---

## 3. Streaming Lakehouse Architecture

```text
[IoT Edge Simulator (Colab)]
          │ (JSON over HTTPS)
          ▼
[Cloud Pub/Sub: solar-telemetry-topic]
          │ (Direct Streaming Ingestion)
          ▼
[Bronze Lakehouse: helios_bronze_dev.telemetry_raw]
          │ (Date Partitioning & Inverter Clustering)
          ▼
[Silver Layer: helios_silver_dev.inverter_cleaned]
          │ (Deduplication, Nighttime Suppression, IEC 61724-1 PR)
          ├─────────────────────────────────────────┐
          ▼                                         ▼
[MLOps Serving Engine]                     [Kimball Star Schema Gold]
  • PyTorch Deep Autoencoder                  • dim_plant
    (tau = 0.00074; 100% anomaly isolation)   • dim_inverter
  • Day-Ahead GBDT Yield Forecaster           • fact_inverter_telemetry_hourly
    (0.56% WAPE; 9.22 kW RMSE)                • fact_yield_predictions
          │                                         │
          └────────────────────┬────────────────────┘
                               ▼
            [Tableau Public Executive Twin]
            (Real-Time PR Tracking, Thermal Anomaly Radar, Generation BANs)
```

---

## 4. Predictive MLOps Engineering

### A. Unsupervised Anomaly Detection (PyTorch Autoencoder)
- **Architecture:** Symmetric 4-layer fully connected network (7 -> 16 -> 4 -> 16 -> 7) with SiLU activation functions and Adam optimizer (learning rate = 0.005, weight decay = 1e-5).
- **Feature Space:** Irradiance, Ambient Temperature, Module Temperature, DC Voltage, DC Power, AC Power, and Heatsink Temperature.
- **Training Protocol:** Trained exclusively on healthy operational baselines (INV-01, INV-02, INV-04) over 40 epochs, driving reconstruction MSE from 0.56863 down to 0.00026.
- **Statistical Decision Boundary:** Dynamic 3-sigma anomaly threshold established at tau = mu + 3*sigma = 0.00074.
- **Validation:** On faulty inverter INV-03, average reconstruction loss spiked to 0.3271 (over 1,250x baseline), isolating 100% of active thermal derating events.

### B. Day-Ahead Generation Forecaster (GBDT)
- **Features:** Sinusoidal cyclical time encodings (hour_sin, hour_cos), irradiance, and ambient temperature.
- **Performance:** Root Mean Squared Error (RMSE) of 9.22 kW on a 2,500 kW rated inverter, achieving a Weighted Absolute Percentage Error (WAPE) of 0.56% against grid compliance deviation limits (< 10%).

---

## 5. Executive BI & Reporting
The Gold Kimball star schema connects directly to Tableau Public 2026.2 to monitor operational state across three core analytical panes:
1. **Fleet Generation BANs:** Real-time summary of active fleet power generation (7,119 kW), fleet-wide mean PR (90%), and active thermal fault counts.
2. **IEC 61724-1 PR Benchmarking:** Unit-by-unit performance comparison confirming healthy inverters operating at 98.17% to 98.23% while isolating INV-03 at 63.73%.
3. **Thermal Derating Matrix:** Multi-quadrant scatter chart correlating heatsink temperatures against power output, bounded by a 65°C critical alarm threshold.

**Live Interactive Dashboard:** [Tableau Public Executive Twin](https://public.tableau.com/app/profile/raja.rao.gurindapalli2544/viz/Helios10MWSolarFleet-OperationalDigitalTwin/Dashboard?publish=yes)

---

## 7. Enterprise SDLC & Dev-Test-Prod Environment Topology

To replicate industrial-grade mission-critical deployments, Helios isolates operational risks via a 3-tier promotion lifecycle, segregating state, streaming channels, and compute permissions across development, automated testing, and production.

---

## 8. Enterprise Architecture Alignment (TOGAF Standard)

Helios adheres to the **TOGAF Standard (The Open Group Architecture Framework)**, structured across the four core architecture domains of the Architecture Development Method (ADM): Business, Data, Application, and Technology (BDAT).

### BDAT Architecture Decomposition
