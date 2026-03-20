# ==========config.py==========
import os
from dotenv import load_dotenv
load_dotenv()
# -------------------------------
# Security / Auth
# -------------------------------
SECRET_KEY = os.getenv("SECRET_KEY")
USERNAME = os.getenv("APP_USERNAME")
PASSWORD = os.getenv("APP_PASSWORD")

# -------------------------------
# Server Prometheus Mapping
# -------------------------------
SERVER_PROMETHEUS_MAPPING = {
    "DEV-SERVER": os.getenv("DEV_PROM_URL"),
    "QA-SERVER": os.getenv("QA_PROM_URL"),
    "UAT-SERVER": os.getenv("UAT_PROM_URL"),
    "PROD-SERVER": os.getenv("PROD_PROM_URL"),
    "MYSAA-SERVER": os.getenv("MYSAA_PROM_URL"),
    "KK-SERVER": os.getenv("KK_PROM_URL")
}

# -------------------------------
# Server OS Mapping
# -------------------------------
SERVER_OS = {
    "DEV-SERVER": "windows",
    "QA-SERVER": "windows",
    "UAT-SERVER": "linux",
    "PROD-SERVER": "linux",
    "MYSAA-SERVER": "linux",
    "KK-SERVER": "linux"
}

# -------------------------------
# Supported Metrics
# -------------------------------
METRICS = ["cpu", "memory", "disk"]