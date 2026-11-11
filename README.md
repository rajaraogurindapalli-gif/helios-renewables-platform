# Helios Industrial Renewable Energy Platform (Solar PV/BESS)

An enterprise-grade industrial digital twin, real-time telemetry processing engine, and predictive MLOps platform built on Google Cloud Platform (GCP) and BigQuery.

## System Architecture
- **Edge Simulator:** Diurnal solar irradiance modeling, IEC 61724-1 temperature-corrected Performance Ratio (PR), and IGBT thermal fault injection.
- **Ingestion Pipeline:** Colab Edge Simulator -> GCP Pub/Sub (`solar-telemetry-topic`) -> Direct BigQuery Streaming Subscription.
- **Medallion Lakehouse (BigQuery):**
  - **Bronze:** `helios_bronze_dev.telemetry_raw` (Partitioned by Date, Clustered by Inverter).
  - **Silver:** `helios_silver_dev.inverter_cleaned` (Deduplication, Nighttime zero-suppression, IEC 61724-1 PR, Inverter Efficiency).
  - **Gold:** `helios_gold_dev.fact_inverter_telemetry_hourly` (Kimball Star Schema with conformed `dim_plant` and `dim_inverter`).
- **MLOps & Predictive Analytics (Phase 3 Completed):**
  - **Unsupervised Anomaly Detection:** PyTorch Deep Autoencoder trained on healthy inverter baselines. Statistical dynamic threshold $\tau = \mu + 3\sigma = 0.00074$. Isolated `INV-03` thermal derating (`ERR-IGBT-OVERTEMP`) with 100% precision.
  - **Day-Ahead Generation Forecaster:** Cyclical time + weather GBDT model achieving **0.56% WAPE** and **9.22 kW RMSE** against grid deviation limits.
  - **Serving Layer:** BigQuery Gold View `fact_yield_predictions`.
