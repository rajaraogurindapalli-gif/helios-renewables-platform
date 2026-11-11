# Helios Industrial Renewable Energy Platform (Solar PV/BESS)

An enterprise-grade industrial digital twin, real-time telemetry processing engine, and predictive MLOps platform built on Google Cloud Platform (GCP), BigQuery, and Tableau.

# Helios Industrial Renewable Energy Platform (Solar PV/BESS)

[![Helios CI & Container Validation](https://github.com/rajaraogurindapalli-gif/helios-renewables-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/rajaraogurindapalli-gif/helios-renewables-platform/actions/workflows/ci.yml)

An enterprise-grade industrial digital twin, real-time telemetry processing engine, and predictive MLOps platform built on Google Cloud Platform (GCP), BigQuery, and Tableau.

## Live Executive Dashboard
- **Tableau Public Interactive View:** [Helios Solar Fleet Executive Twin](https://public.tableau.com/app/profile/raja.rao.gurindapalli2544/viz/Helios10MWSolarFleet-OperationalDigitalTwin/Dashboard?publish=yes)

---

## Architecture Overview

```text
[IoT Edge Simulator (Colab)] 
          │  (JSON Telemetry: 15-min intervals, Diurnal Physics, IGBT Faults)
          ▼
[GCP Pub/Sub (solar-telemetry-topic)]
          │  (Direct Streaming Ingestion)
          ▼
[BigQuery Bronze Lakehouse (helios_bronze_dev.telemetry_raw)]
          │  (Partitioned by Timestamp, Clustered by Inverter)
          ▼
[BigQuery Silver Layer (helios_silver_dev.inverter_cleaned)]
          │  (Deduplication, Nighttime Zero-Suppression, IEC 61724-1 PR Correction)
          ├─────────────────────────────────────────┐
          ▼                                         ▼
[MLOps Serving Engine]                     [Kimball Star Schema Gold]
  • PyTorch Deep Autoencoder                  • dim_plant
    (MSE threshold tau = 0.00074; 100% isolation) • dim_inverter
  • Day-Ahead GBDT Yield Forecaster           • fact_inverter_telemetry_hourly
    (0.56% WAPE; 9.22 kW RMSE)                • fact_yield_predictions
          │                                         │
          └────────────────────┬────────────────────┘
                               ▼
            [Tableau Public Executive Twin]
            (Real-Time PR Tracking, Thermal Anomaly Radar, Generation BANs)
```

## System Highlights & Performance
* **Streaming Architecture:** Direct Pub/Sub to BigQuery ingestion supporting sub-second row arrival.
* **Standards Compliance:** Full implementation of **IEC 61724-1** temperature-corrected Performance Ratio (PR) at the Silver lakehouse layer.
* **Unsupervised Fault Isolation:** PyTorch Deep Autoencoder isolates IGBT overheating (`ERR-IGBT-OVERTEMP`) on derated inverters (`INV-03`) with a reconstruction loss ratio of over 1,200x against healthy baseline units.
* **Yield Forecasting:** Day-ahead GBDT model achieving **0.56% WAPE** against strict 10% grid code deviation limits.
* **Business Intelligence:** Kimball Gold star schema serving executive KPIs, inverter PR benchmarking, and thermal risk quadrants.
