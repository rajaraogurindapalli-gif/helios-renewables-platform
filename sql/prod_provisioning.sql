-- ====================================================================
-- HELIOS INDUSTRIAL RENEWABLE ENERGY DIGITAL TWIN
-- Production Environment Provisioning DDL (Zero-Cost BigQuery Sandbox)
-- ====================================================================

-- 1. PROD BRONZE LAYER (Raw Telemetry Ingestion)
CREATE SCHEMA IF NOT EXISTS `responsive-sun-313908.helios_bronze_prod`
OPTIONS (location = 'US');

CREATE TABLE IF NOT EXISTS `responsive-sun-313908.helios_bronze_prod.raw_telemetry` (
    ingest_timestamp TIMESTAMP,
    plant_id STRING,
    inverter_id STRING,
    irradiation_w_m2 FLOAT64,
    ambient_temp_c FLOAT64,
    module_temp_c FLOAT64,
    dc_power_kw FLOAT64,
    ac_power_kw FLOAT64,
    daily_yield_kwh FLOAT64
)
PARTITION BY DATE(ingest_timestamp)
CLUSTER BY inverter_id;

-- 2. PROD SILVER LAYER (Cleaned, Conformed, Deduplicated)
CREATE SCHEMA IF NOT EXISTS `responsive-sun-313908.helios_silver_prod`
OPTIONS (location = 'US');

CREATE TABLE IF NOT EXISTS `responsive-sun-313908.helios_silver_prod.conformed_telemetry` (
    timestamp TIMESTAMP,
    plant_id STRING,
    inverter_id STRING,
    irradiation_w_m2 FLOAT64,
    ambient_temp_c FLOAT64,
    module_temp_c FLOAT64,
    dc_power_kw FLOAT64,
    ac_power_kw FLOAT64,
    temp_derate_loss_kw FLOAT64,
    inverter_efficiency_pct FLOAT64,
    reconstruction_loss_mse FLOAT64,
    is_anomaly INT64,
    error_code STRING
)
PARTITION BY DATE(timestamp)
CLUSTER BY inverter_id;

-- 3. PROD GOLD LAYER (Kimball Star Schema for BI & Digital Twin)
CREATE SCHEMA IF NOT EXISTS `responsive-sun-313908.helios_gold_prod`
OPTIONS (location = 'US');

CREATE OR REPLACE VIEW `responsive-sun-313908.helios_gold_prod.vw_executive_digital_twin` AS
SELECT 
    s.timestamp,
    s.plant_id,
    s.inverter_id,
    s.irradiation_w_m2,
    s.ambient_temp_c,
    s.module_temp_c,
    s.ac_power_kw,
    s.temp_derate_loss_kw,
    s.inverter_efficiency_pct,
    s.is_anomaly,
    s.error_code,
    ROUND((s.ac_power_kw / NULLIF((s.irradiation_w_m2 / 1000.0) * 2500.0, 0)) * 100, 2) AS performance_ratio_pr
FROM `responsive-sun-313908.helios_silver_prod.conformed_telemetry` s;
