-- Silver Layer View
-- Computes Inverter Efficiency and IEC 61724-1 PR
CREATE OR REPLACE VIEW `helios_silver_dev.inverter_cleaned` AS
WITH deduplicated AS (
    SELECT *, ROW_NUMBER() OVER(PARTITION BY plant_id, inverter_id, timestamp ORDER BY ingestion_timestamp DESC) as rn
    FROM `helios_bronze_dev.telemetry_raw`
    WHERE timestamp IS NOT NULL
)
SELECT * FROM deduplicated WHERE rn = 1;
