# main.py aggiornato per log nella finestra figlia

import tkinter as tk
from tkinter import Text
import openmeteo_requests
from datetime import datetime
import pandas as pd
import requests_cache
from retry_requests import retry
from dotenv import load_dotenv
import os

load_dotenv()

CACHE_EXPIRATION = int(os.getenv("CACHE_EXPIRATION", 3600))
RETRY_COUNT = int(os.getenv("RETRY_COUNT", 5))
BACKOFF_FACTOR = float(os.getenv("BACKOFF_FACTOR", 0.2))

cache_session = requests_cache.CachedSession('.cache', expire_after=CACHE_EXPIRATION)
retry_session = retry(cache_session, retries=RETRY_COUNT, backoff_factor=BACKOFF_FACTOR)
openmeteo = openmeteo_requests.Client(session=retry_session)

cities = {
    "Roma": (41.9028, 12.4964),
    "Tokyo": (35.6895, 139.6917),
    "New York": (40.7128, -74.0060)
}

# ----- FUNZIONI METEO -----
def get_weather(latitude, longitude):
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {"latitude": latitude, "longitude": longitude, "hourly": "temperature_2m"}
        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]
        hourly = response.Hourly()
        temperatures = hourly.Variables(0).ValuesAsNumpy()
        dates = pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        )
        return pd.DataFrame({"date": dates, "temperature": temperatures})
    except Exception as e:
        return pd.DataFrame()

# ----- FUNZIONE LOG -----
def log_message(log_widget: Text, message: str):
    log_widget.config(state=tk.NORMAL)
    log_widget.insert(tk.END, message + "\n")
    log_widget.see(tk.END)
    log_widget.update()
    log_widget.config(state=tk.DISABLED)

# ----- MOSTRA DATI -----
def show_next_hours(city_name, df, log_widget, hours=5):
    if df.empty:
        log_message(log_widget, f"{city_name}: Nessun dato disponibile")
        return

    now = datetime.now()
    current_index = df[df["date"] >= pd.Timestamp(now, tz="UTC")].index.min()

    if pd.isna(current_index):
        log_message(log_widget, f"{city_name}: Nessun dato attuale trovato")
        return

    log_message(log_widget, f"\n----- {city_name} -----")
    for i in range(hours):
        if current_index + i < len(df):
            row = df.loc[current_index + i]
            formatted_date = row['date'].strftime("%d %H:%M")
            temperature = round(float(row['temperature']), 1)
            log_message(log_widget, f"{formatted_date} - temperatura: {temperature}°C")

# ----- FINESTRA FIGLIA -----
def meteo_window(parent):
    root = tk.Toplevel(parent)
    root.title("Meteo App")
    root.geometry("600x450")
    root.resizable(False, False)

    log_box = Text(root, height=20, width=70, state=tk.DISABLED)
    log_box.pack(padx=10, pady=10)

    def fetch_weather():
        for city, (lat, lon) in cities.items():
            df = get_weather(lat, lon)
            show_next_hours(city, df, log_box)

    fetch_btn = tk.Button(root, text="Mostra Meteo", command=fetch_weather)
    fetch_btn.pack(pady=5)

    exit_btn = tk.Button(root, text="Esci", command=root.destroy)
    exit_btn.pack(pady=5)

    root.protocol("WM_DELETE_WINDOW", root.destroy)
    return root

# ----- MAIN -----

if __name__ == "__main__":
    app = tk.Tk()
    app.withdraw()  # nasconde la finestra principale
    win = meteo_window(app)
    app.mainloop()