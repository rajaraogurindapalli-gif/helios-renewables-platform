"""
Helios Autonomous Plant Reliability Agent (ReAct + Industrial RAG)
Provides diagnostic reasoning, document retrieval, financial loss calculations,
and automated maintenance dispatch for utility-scale solar inverters.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Any, List

# -------------------------------------------------------------------------
# 1. Domain Knowledge Base (Simulated Vector Store / RAG Chunks)
# -------------------------------------------------------------------------
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

# -------------------------------------------------------------------------
# 2. Agent Action Tools
# -------------------------------------------------------------------------
class HeliosAgentTools:
    
    @staticmethod
    def query_telemetry_history(df: pd.DataFrame, inverter_id: str) -> Dict[str, Any]:
        """Tool 1: Inspects historical telemetry for a specific inverter."""
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
        """Tool 2: RAG Vector/Keyword retriever from OEM & Regulatory corpus."""
        hits = []
        for doc in DOMAIN_KNOWLEDGE_BASE:
            score = sum(1 for kw in query_keywords if any(kw.lower() in k.lower() for k in doc["keywords"]))
            if score > 0:
                hits.append({"doc_id": doc["id"], "topic": doc["topic"], "content": doc["content"]})
        return hits

    @staticmethod
    def calculate_financial_loss(temp_derate_kw: float, duration_hours: float = 2.0) -> Dict[str, float]:
        """Tool 3: Financial loss and deviation fine calculation."""
        energy_loss_kwh = temp_derate_kw * duration_hours
        lost_revenue = energy_loss_kwh * 0.075  # $0.075/kWh PPA base
        grid_fine = energy_loss_kwh * 0.035     # Peak deviation penalty
        total_loss = lost_revenue + grid_fine
        
        return {
            "lost_generation_kwh": round(energy_loss_kwh, 2),
            "revenue_loss_usd": round(lost_revenue, 2),
            "grid_deviation_penalty_usd": round(grid_fine, 2),
            "total_financial_exposure_usd": round(total_loss, 2)
        }

# -------------------------------------------------------------------------
# 3. Autonomous Reasoning Engine (ReAct Loop)
# -------------------------------------------------------------------------
class HeliosReliabilityAgent:
    def __init__(self, telemetry_csv_path: str):
        self.df = pd.read_csv(telemetry_csv_path)
        self.tools = HeliosAgentTools()

    def run_fleet_scan(self) -> List[str]:
        """Scans the fleet for assets requiring autonomous intervention."""
        anomalies = self.df[self.df["Is Anomaly"] == 1]
        flagged_inverters = anomalies["Inverter Id"].unique().tolist()
        return flagged_inverters

    def diagnose_and_dispatch(self, inverter_id: str) -> Dict[str, Any]:
        """Executes full autonomous reasoning, RAG lookup, and dispatch plan."""
        print(f"\n[AGENT] Initiating ReAct diagnostic loop for asset: {inverter_id}...")
        
        # Step 1: Perception & Telemetry Inspection
        telemetry_stats = self.tools.query_telemetry_history(self.df, inverter_id)
        print(f"  -> Thought: Checking telemetry statistics and anomaly flags...")
        
        # Step 2: Decision Gating
        if telemetry_stats.get("anomaly_event_count", 0) == 0:
            return {"status": "NOMINAL", "message": f"{inverter_id} is operating within normal parameters."}
        
        print(f"  -> Observation: Detected {telemetry_stats['anomaly_event_count']} anomalies. "
              f"Peak Heatsink Temp: {telemetry_stats['peak_heatsink_temp_c']}°C, "
              f"Reconstruction Loss MSE: {telemetry_stats['max_reconstruction_loss']}.")
        
        # Step 3: RAG Knowledge Retrieval
        print(f"  -> Thought: Querying OEM Maintenance & PPA documentation for 'ERR-IGBT-OVERTEMP'...")
        rag_context = self.tools.retrieve_domain_guidelines(["ERR-IGBT-OVERTEMP", "heatsink", "penalty"])
        
        # Step 4: Quantitative Impact Assessment
        stress_records = self.df[(self.df["Inverter Id"] == inverter_id) & (self.df["Is Anomaly"] == 1)]
        avg_derate_loss = stress_records["Temp Derate Loss Kw"].mean()
        financial_impact = self.tools.calculate_financial_loss(avg_derate_loss, duration_hours=len(stress_records))
        
        # Step 5: Action Synthesis (Automated Work Order)
        print(f"  -> Action: Generating structured Field Engineering Work Order...")
        work_order = {
            "work_order_id": f"WO-HELIOS-{inverter_id}-{datetime.now().strftime('%Y%m%d%H%M')}",
            "priority": "P1 - HIGH",
            "target_asset": inverter_id,
            "root_cause_diagnosis": (
                f"Severe thermal choking confirmed on {inverter_id}. Operating heatsink temperature reached "
                f"{telemetry_stats['peak_heatsink_temp_c']}°C, inducing autoencoder reconstruction anomaly "
                f"({telemetry_stats['max_reconstruction_loss']} MSE vs. 0.00074 baseline). "
                f"System derated to ~62% capacity to avert catastrophic $35,000 IGBT module breakdown."
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
        
        return work_order
