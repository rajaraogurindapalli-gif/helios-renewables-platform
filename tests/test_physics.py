import pytest
from src.telemetry_generator import generate_telemetry_reading

def test_iec_standard_derating_bounds():
    # Test nominal operating point at standard irradiance
    reading = generate_telemetry_reading("INV-01", irradiance=800.0, amb_temp=30.0)
    
    # Assert physical constraints
    assert reading["ac_power_kw"] > 0.0, "AC Power must be positive during daytime"
    assert reading["ac_power_kw"] <= 2500.0, "AC Power cannot exceed inverter rated capacity (2.5 MW)"
    assert reading["module_temp_c"] > reading["ambient_temp_c"], "Cell temp must exceed ambient under solar gain"

def test_zero_irradiance_night_condition():
    # Zero solar irradiance should yield zero generation
    reading = generate_telemetry_reading("INV-01", irradiance=0.0, amb_temp=22.0)
    assert reading["ac_power_kw"] == 0.0, "AC power must be strictly 0.0 at night"

def test_thermal_efficiency_penalty():
    # Higher module temperature must degrade DC-to-AC conversion efficiency
    cool_reading = generate_telemetry_reading("INV-01", irradiance=900.0, amb_temp=20.0)
    hot_reading = generate_telemetry_reading("INV-01", irradiance=900.0, amb_temp=45.0)
    
    assert cool_reading["ac_power_kw"] > hot_reading["ac_power_kw"], \
        "Higher module temperature must yield lower power due to negative temp coefficient (-0.4%/C)"
