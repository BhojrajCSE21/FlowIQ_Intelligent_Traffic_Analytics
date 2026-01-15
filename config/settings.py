"""
Configuration settings for Smart City Traffic Analytics
"""

# Data paths
DATA_RAW_PATH = "data/raw"
DATA_PROCESSED_PATH = "data/processed"
DATA_EXTERNAL_PATH = "data/external"

# Model paths
MODEL_OUTPUT_PATH = "outputs/models"

# Dashboard settings
DASHBOARD_HOST = "127.0.0.1"
DASHBOARD_PORT = 8050

# Analysis parameters
PEAK_HOURS_MORNING = (8, 10)  # 8 AM - 10 AM
PEAK_HOURS_EVENING = (17, 20)  # 5 PM - 8 PM

# Congestion thresholds
CONGESTION_LEVELS = {
    "LOW": (0, 30),
    "MEDIUM": (30, 60),
    "HIGH": (60, 80),
    "SEVERE": (80, 100)
}
