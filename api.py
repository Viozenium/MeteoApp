"""Chiamate alle API gratuite di Open-Meteo (geocoding + forecast)."""

import requests_cache
from retry_requests import retry

import config

cache_session = requests_cache.CachedSession(
    ".cache", expire_after=config.CACHE_EXPIRATION
)
SESSION = retry(
    cache_session, retries=config.RETRY_COUNT, backoff_factor=config.BACKOFF_FACTOR
)


def geocode_city(name, limit=None):
    """Cerca città per nome. Restituisce una lista di risultati grezzi dall'API."""
    limit = limit or config.GEOCODING_RESULTS_LIMIT
    resp = SESSION.get(
        config.GEOCODING_URL,
        params={
            "name": name,
            "count": limit,
            "language": config.GEOCODING_LANGUAGE,
            "format": "json",
        },
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json().get("results") or []


def fetch_weather(lat, lon):
    """Scarica meteo corrente + previsioni orarie/giornaliere per una coordinata."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m",
        "hourly": "temperature_2m,weather_code",
        "daily": "temperature_2m_max,temperature_2m_min,weather_code",
        "timezone": "auto",
        "forecast_days": config.FORECAST_DAYS,
    }
    resp = SESSION.get(config.FORECAST_URL, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()
