"""
Helios Episodic Asset Memory Store
Maintains persistent maintenance lifecycle logs, recurring failure counts,
and field technician sign-off history per inverter asset.
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any

MEMORY_FILE_PATH = "/content/helios-project/data/asset_memory.json"

class AssetMemoryStore:
    def __init__(self, storage_path: str = MEMORY_FILE_PATH):
        self.storage_path = storage_path
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, "w") as f:
                json.dump({}, f)

    def _read_store(self) -> Dict[str, Any]:
        try:
            with open(self.storage_path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def _write_store(self, data: Dict[str, Any]):
        with open(self.storage_path, "w") as f:
            json.dump(data, f, indent=2)

    def log_work_order(self, inverter_id: str, work_order: Dict[str, Any]) -> None:
        """Logs a generated work order to persistent history."""
        data = self._read_store()
        history = data.setdefault(inverter_id, [])
        
        # Check if already logged to prevent duplicates
        wo_id = work_order.get("work_order_id")
        if any(item.get("work_order_id") == wo_id for item in history):
            return

        history.append({
            "work_order_id": wo_id,
            "logged_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "priority": work_order.get("priority"),
            "primary_fault": work_order.get("rag_reference_source", []),
            "financial_exposure_usd": work_order.get("estimated_financial_loss", {}).get("total_financial_exposure_usd", 0.0),
            "status": "OPEN",
            "resolution_notes": None,
            "closed_at": None
        })
        self._write_store(data)

    def resolve_work_order(self, inverter_id: str, work_order_id: str, notes: str) -> bool:
        """Updates an open work order with field technician completion notes."""
        data = self._read_store()
        history = data.get(inverter_id, [])
        for record in history:
            if record.get("work_order_id") == work_order_id and record.get("status") == "OPEN":
                record["status"] = "RESOLVED"
                record["resolution_notes"] = notes
                record["closed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self._write_store(data)
                return True
        return False

    def get_asset_history(self, inverter_id: str) -> List[Dict[str, Any]]:
        """Retrieves maintenance and incident history for an asset."""
        return self._read_store().get(inverter_id, [])

    def get_fleet_incident_count(self) -> Dict[str, int]:
        """Returns total historical incidents by inverter."""
        data = self._read_store()
        return {inv: len(records) for inv, records in data.items()}
