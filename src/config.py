import os

class Settings:
    ENV: str = os.getenv("APP_ENV", "dev").lower()
    GCP_PROJECT: str = os.getenv("GCP_PROJECT", "responsive-sun-313908")
    
    # Dynamic dataset resolution: helios_<layer>_<env>
    BRONZE_DATASET: str = f"helios_bronze_{ENV}"
    SILVER_DATASET: str = f"helios_silver_{ENV}"
    GOLD_DATASET: str = f"helios_gold_{ENV}"
    
    # Pub/Sub Topic naming
    TELEMETRY_TOPIC: str = f"solar-telemetry-{ENV}-topic"
    
    # Model Thresholds
    AE_THRESHOLD_TAU: float = 0.00074
    IEC_DERATING_GAMMA: float = 0.004

settings = Settings()

if __name__ == "__main__":
    print(f"Active Environment: {settings.ENV.upper()}")
    print(f"Bronze Target: {settings.GCP_PROJECT}.{settings.BRONZE_DATASET}")
    print(f"Silver Target: {settings.GCP_PROJECT}.{settings.SILVER_DATASET}")
    print(f"Gold Target:   {settings.GCP_PROJECT}.{settings.GOLD_DATASET}")
    print(f"Pub/Sub Topic: {settings.TELEMETRY_TOPIC}")
