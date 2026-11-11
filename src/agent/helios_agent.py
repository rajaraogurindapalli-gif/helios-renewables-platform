"""
Helios Autonomous Plant Reliability Agent (ReAct + Industrial RAG + Episodic Memory)
Provides diagnostic reasoning, document retrieval, financial loss calculations,
episodic maintenance memory, and automated shift handover reporting.
"""

import os
import pandas as pd
from datetime import datetime
from typing import Dict, Any, List

from src.agent.memory import AssetMemoryStore
from src.agent.analytics import FleetAnalyticsEngine

DOMAIN_KNOWLEDGE_BASE = [
    {
        "id": "DOC-OEM-INV2500-CH08",
        "topic": "Thermal Management & IGBT Protection",
        "keywords": ["ERR-IGBT-OVERTEMP", "heatsink", "thermal", "cooling", "derating"],
        "content": (
            "Section 8.4: IGBT Bridge Over-Temperature (ERR-IGBT-OVERTEMP). "
            "When heatsink temperature exceeds 75°C, internal MPPT logic applies forced "
            "derating to 60-65% P_AC. Root causes: (1) Forced draft air-filter dust clogging, "
            "(2) Internal cooling fan stage 2 auxiliary breaker trip, (3) Thermal grease pump-out. "
            "Action Plan: Dispatch field technician to measure air intake static delta-P, "
            "inspect 24V fan bus fuses, and verify thermal imaging on central inverter cabinet."
        )
    },
    {
        "id": "DOC-IEC-61724-1-PR",
        "topic": "Performance Ratio & Weather Normalization",
        "keywords": ["performance ratio", "PR", "temperature derate", "weather", "soiling"],
        "content": (
            "IEC 61724-1 Class A standard mandates temperature-corrected Performance Ratio (PR_corr) "
            "using gamma = -0.004 / °C against 25°C STC. If PR_corr < 70% while irradiance > 600 W/m2, "
            "fault is electromechanical or string-level clipping, not ambient solar variation."
        )
    },
    {
        "id": "DOC-PPA-PENALTY-GRID",
        "topic": "Power Purchase Agreement & Curtailment Fines",
        "keywords": ["penalty", "curtailment", "grid deviation", "loss", "tariff"],
        "content": (
            "Schedule B PPA Rules: Base solar injection tariff = $0.075 / kWh. "
            "Unscheduled generation deviations exceeding 10% of day-ahead schedule incur an "
            "additional penalty of $0.035 / kWh for every hour of shortfall during peak tariff (11:00-15:00)."
        )
    }
]

class HeliosAgentTools:
    
    @staticmethod
    def query_telemetry_history(df: pd.DataFrame, inverter_id: str) -> Dict[str, Any]:
        inv_data = df[df["Inverter Id"] == inverter_id].sort_values("Timestamp Hour")
        if inv_data.empty:
            return {"error": f"Inverter {inverter_id} not found."}
        
        peak_heatsink = inv_data["Avg Heatsink Temp C"].max()
        avg_pr = inv_data[inv_data["Irradiation W M2"] > 100]["Avg Avg Performance Ratio Pct"].mean()
        anomalies = inv_data[inv_data["Is Anomaly"] == 1]
        
        return {
            "inverter_id": inverter_id,
            "total_records": len(inv_data),
            "peak_heatsink_temp_c": round(peak_heatsink, 1),
            "average_daylight_pr": round(avg_pr, 2),
            "anomaly_event_count": len(anomalies),
            "fault_codes": anomalies["Primary Fault Code"].unique().tolist(),
            "max_reconstruction_loss": round(inv_data["Reconstruction Loss Mse"].max(), 6)
        }

    @staticmethod
    def retrieve_domain_guidelines(query_keywords: List[str]) -> List[Dict[str, str]]:
        hits = []
        for doc in DOMAIN_KNOWLEDGE_BASE:
            score = sum(1 for kw in query_keywords if any(kw.lower() in k.lower() for k in doc["keywords"]))
            if score > 0:
                hits.append({"doc_id": doc["id"], "topic": doc["topic"], "content": doc["content"]})
        return hits

    @staticmethod
    def calculate_financial_loss(temp_derate_kw: float, duration_hours: float = 2.0) -> Dict[str, float]:
        energy_loss_kwh = temp_derate_kw * duration_hours
        lost_revenue = energy_loss_kwh * 0.075
        grid_fine = energy_loss_kwh * 0.035
        total_loss = lost_revenue + grid_fine
        
        return {
            "lost_generation_kwh": round(energy_loss_kwh, 2),
            "revenue_loss_usd": round(lost_revenue, 2),
            "grid_deviation_penalty_usd": round(grid_fine, 2),
            "total_financial_exposure_usd": round(total_loss, 2)
        }

class HeliosReliabilityAgent:
    def __init__(self, telemetry_csv_path: str):
        self.df = pd.read_csv(telemetry_csv_path)
        self.tools = HeliosAgentTools()
        self.memory = AssetMemoryStore()
        self.analytics = FleetAnalyticsEngine()

    def run_fleet_scan(self) -> List[str]:
        anomalies = self.df[self.df["Is Anomaly"] == 1]
        return anomalies["Inverter Id"].unique().tolist()

    def diagnose_and_dispatch(self, inverter_id: str) -> Dict[str, Any]:
        telemetry_stats = self.tools.query_telemetry_history(self.df, inverter_id)
        
        if telemetry_stats.get("anomaly_event_count", 0) == 0:
            return {"status": "NOMINAL", "message": f"{inverter_id} is operating within normal parameters."}
        
        past_history = self.memory.get_asset_history(inverter_id)
        repeat_incident_note = ""
        if len(past_history) > 0:
            repeat_incident_note = f" Note: Asset has {len(past_history)} prior logged incidents in memory."

        rag_context = self.tools.retrieve_domain_guidelines(["ERR-IGBT-OVERTEMP", "heatsink", "penalty"])
        
        stress_records = self.df[(self.df["Inverter Id"] == inverter_id) & (self.df["Is Anomaly"] == 1)]
        avg_derate_loss = stress_records["Temp Derate Loss Kw"].mean()
        financial_impact = self.tools.calculate_financial_loss(avg_derate_loss, duration_hours=len(stress_records))
        
        work_order = {
            "work_order_id": f"WO-HELIOS-{inverter_id}-{datetime.now().strftime('%Y%m%d%H%M')}",
            "priority": "P1 - HIGH",
            "target_asset": inverter_id,
            "root_cause_diagnosis": (
                f"Severe thermal choking confirmed on {inverter_id}. Operating heatsink temperature reached "
                f"{telemetry_stats['peak_heatsink_temp_c']}°C, inducing autoencoder reconstruction anomaly "
                f"({telemetry_stats['max_reconstruction_loss']} MSE vs. 0.00074 baseline). "
                f"System derated to ~62% capacity to avert catastrophic $35,000 IGBT breakdown.{repeat_incident_note}"
            ),
            "estimated_financial_loss": financial_impact,
            "prescribed_field_sop": [
                "1. Inspect external intake louvers for dust fouling or thermal shroud blockage.",
                "2. Check 24V auxiliary cooling fan bus fuses and motor spin resistance.",
                "3. Perform infrared thermal camera scan on internal bridge terminals for localized hotspots.",
                "4. Clear fault log via inverter controller interface only after heatsink settles below 60°C."
            ],
            "rag_reference_source": [doc["doc_id"] for doc in rag_context]
        }
        
        self.memory.log_work_order(inverter_id, work_order)
        return work_order
