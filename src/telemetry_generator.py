import numpy as np

def generate_telemetry_reading(inverter_id: str, irradiance: float, amb_temp: float):
    """Simulates single inverter diurnal telemetry reading with IEC 61724-1 temperature derating."""
    module_temp = amb_temp + (irradiance * 0.03)
    rated_kw = 2500.0
    gamma = 0.004  # 0.4%/°C thermal degradation rate above 25°C STC
    
    # Proper IEC 61724-1 derating: efficiency drops as temperature rises
    temp_penalty = 1.0 - (gamma * max(0.0, module_temp - 25.0))
    p_dc = (irradiance / 1000.0) * rated_kw * max(0.0, temp_penalty)
    p_ac = p_dc * 0.984
    
    return {
        "inverter_id": inverter_id,
        "irradiation_w_m2": round(irradiance, 2),
        "ambient_temp_c": round(amb_temp, 2),
        "module_temp_c": round(module_temp, 2),
        "ac_power_kw": round(p_ac, 2)
    }

if __name__ == "__main__":
    reading = generate_telemetry_reading("INV-01", 850.0, 32.0)
    print("Telemetry module verified:", reading)
