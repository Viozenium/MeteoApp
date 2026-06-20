"""Configurazione dell'applicazione, caricata dal file .env"""

# ----------------------------------------
# Metadati dell'applicazione

__version__ = "2.0.0"
__app_name__ = "Meteo App"
__author__ = "Mizu"

import os
from dotenv import load_dotenv

load_dotenv()

# ----------------------------------------
# Cache e retry per le chiamate HTTP

CACHE_EXPIRATION = int(os.getenv("CACHE_EXPIRATION", 3600))
RETRY_COUNT = int(os.getenv("RETRY_COUNT", 3))
BACKOFF_FACTOR = float(os.getenv("BACKOFF_FACTOR", 0.3))

# ----------------------------------------
# Aspetto della finestra

DEFAULT_THEME = os.getenv("DEFAULT_THEME", "chiaro")
WINDOW_WIDTH = int(os.getenv("WINDOW_WIDTH", 1100))
WINDOW_HEIGHT = int(os.getenv("WINDOW_HEIGHT", 750))

# ----------------------------------------
# Dati meteo

FORECAST_DAYS = int(os.getenv("FORECAST_DAYS", 6))
HOURLY_HOURS_SHOWN = int(os.getenv("HOURLY_HOURS_SHOWN", 8))
GEOCODING_RESULTS_LIMIT = int(os.getenv("GEOCODING_RESULTS_LIMIT", 8))
GEOCODING_LANGUAGE = os.getenv("GEOCODING_LANGUAGE", "it")

# ----------------------------------------
# Città preferite: (nome, lat, lon, paese)

FAVORITE_CITIES = [
    ("Roma", 41.9028, 12.4964, "Italia"),
    ("Tokyo", 35.6895, 139.6917, "Giappone"),
    ("New York", 40.7128, -74.0060, "USA"),
]

# ----------------------------------------
# Endpoint API Open-Meteo

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
