# Helios Industrial Renewable Energy Platform (Solar PV/BESS)

An enterprise-grade industrial digital twin and real-time telemetry processing engine built on Google Cloud Platform (GCP) and BigQuery.

## Architecture
- **Ingestion:** Google Colab Edge Simulator -> Cloud Pub/Sub (`solar-telemetry-topic`) -> Direct BigQuery Subscription
- **Lakehouse Storage:**
  - **Bronze:** `helios_bronze_dev.telemetry_raw` (Partitioned by Date, Clustered by Inverter)
  - **Silver:** `helios_silver_dev.inverter_cleaned` (Deduplicated, Nighttime suppressed, IEC 61724-1 Temperature-Corrected PR)
  - **Gold:** `helios_gold_dev.fact_inverter_telemetry_hourly` (Kimball Dimensional Model)
- **MLOps (Phase 3):** PyTorch Deep Autoencoder for IGBT Over-temperature Anomaly Detection & Day-Ahead Solar Yield Forecasting.
