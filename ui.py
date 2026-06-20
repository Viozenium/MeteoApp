"""Interfaccia grafica della Meteo App."""

import threading
from datetime import datetime

import tkinter as tk
from tkinter import ttk, messagebox

import config
import api
from themes import THEMES
from weather_codes import describe_weather
from info import show_info_window


class MeteoApp(ttk.Frame):
    def __init__(self, master, theme_name=None):
        super().__init__(master, padding=12)
        self.pack(fill=tk.BOTH, expand=True)
        self.master = master
        self.search_results = []
        self.theme_buttons = {}
        self.current_theme = theme_name or config.DEFAULT_THEME
        self.style = ttk.Style(master)
        self.style.theme_use("clam")

        self._build_header()
        self._build_search_bar()
        self._build_favorites()
        self._build_current_panel()
        self._build_forecast_tables()
        self._build_status_bar()

        theme_name = theme_name or config.DEFAULT_THEME
        self.apply_theme(theme_name if theme_name in THEMES else "chiaro")

    def _build_header(self):
        frame = ttk.Frame(self)
        frame.pack(fill=tk.X, pady=(0, 8))

        ttk.Label(frame, text="Meteo App", font=("Segoe UI", 14, "bold")).pack(
            side=tk.LEFT
        )

        right = ttk.Frame(frame)
        right.pack(side=tk.RIGHT)

        ttk.Button(
            right,
            text="ℹ Info",
            width=8,
            command=lambda: show_info_window(self.master, self.current_theme),
        ).pack(side=tk.RIGHT, padx=(8, 0))

        theme_frame = ttk.Frame(right)
        theme_frame.pack(side=tk.RIGHT)
        for key, label in (
            ("chiaro", "☀ Chiaro"),
            ("scuro", "🌙 Scuro"),
            ("colorato", "🎨 Colorato"),
        ):
            btn = ttk.Button(
                theme_frame,
                text=label,
                width=10,
                command=lambda k=key: self.apply_theme(k),
            )
            btn.pack(side=tk.LEFT, padx=2)
            self.theme_buttons[key] = btn

    def _build_search_bar(self):
        frame = ttk.Frame(self)
        frame.pack(fill=tk.X, pady=(0, 8))

        self.search_var = tk.StringVar()
        entry = ttk.Entry(frame, textvariable=self.search_var)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        entry.bind("<Return>", lambda e: self.on_search())

        ttk.Button(frame, text="Cerca", command=self.on_search).pack(
            side=tk.LEFT, padx=(6, 0)
        )

        self.results_list = tk.Listbox(
            self, height=4, relief="flat", highlightthickness=1
        )
        self.results_list.pack(fill=tk.X, pady=(0, 8))
        self.results_list.bind("<Double-Button-1>", self.on_result_selected)

    def _build_favorites(self):
        frame = ttk.Frame(self)
        frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(frame, text="Preferite:").pack(side=tk.LEFT)
        for name, lat, lon, country in config.FAVORITE_CITIES:
            ttk.Button(
                frame,
                text=name,
                command=lambda n=name, la=lat, lo=lon, c=country: self.load_city(
                    n, la, lo, c
                ),
            ).pack(side=tk.LEFT, padx=4)

    def _build_current_panel(self):
        panel = ttk.LabelFrame(self, text="Meteo corrente", padding=10)
        panel.pack(fill=tk.X, pady=(0, 10))

        self.city_label = ttk.Label(
            panel, text="Nessuna città selezionata", font=("Segoe UI", 13, "bold")
        )
        self.city_label.pack(anchor="w")

        self.temp_label = ttk.Label(
            panel, text="--", font=("Segoe UI", 28), style="Accent.TLabel"
        )
        self.temp_label.pack(anchor="w")

        self.detail_label = ttk.Label(panel, text="", font=("Segoe UI", 10))
        self.detail_label.pack(anchor="w")

    def _build_forecast_tables(self):
        tables_frame = ttk.Frame(self)
        tables_frame.pack(fill=tk.BOTH, expand=True)

        hourly_frame = ttk.LabelFrame(tables_frame, text="Prossime ore", padding=6)
        hourly_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))
        self.hourly_tree = ttk.Treeview(
            hourly_frame, columns=("ora", "temp", "meteo"), show="headings", height=8
        )
        for col, text, w in (
            ("ora", "Ora", 60),
            ("temp", "Temp.", 60),
            ("meteo", "Meteo", 140),
        ):
            self.hourly_tree.heading(col, text=text)
            self.hourly_tree.column(col, width=w, anchor="center")
        self.hourly_tree.pack(fill=tk.BOTH, expand=True)

        daily_frame = ttk.LabelFrame(tables_frame, text="Prossimi giorni", padding=6)
        daily_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.daily_tree = ttk.Treeview(
            daily_frame,
            columns=("giorno", "min", "max", "meteo"),
            show="headings",
            height=8,
        )
        for col, text, w in (
            ("giorno", "Giorno", 70),
            ("min", "Min", 50),
            ("max", "Max", 50),
            ("meteo", "Meteo", 140),
        ):
            self.daily_tree.heading(col, text=text)
            self.daily_tree.column(col, width=w, anchor="center")
        self.daily_tree.pack(fill=tk.BOTH, expand=True)

    def _build_status_bar(self):
        self.status_var = tk.StringVar(value="Pronto.")
        self.status_label = ttk.Label(self, textvariable=self.status_var)
        self.status_label.pack(anchor="w", pady=(8, 0))

    def apply_theme(self, name):
        colors = THEMES.get(name, THEMES["chiaro"])
        self.current_theme = name

        bg, fg = colors["bg"], colors["fg"]
        panel_bg, tree_bg = colors["panel_bg"], colors["tree_bg"]
        accent, accent_fg = colors["accent"], colors["accent_fg"]

        self.master.configure(bg=bg)

        s = self.style
        s.configure("TFrame", background=bg)
        s.configure("TLabel", background=bg, foreground=fg)
        s.configure("Accent.TLabel", background=bg, foreground=accent)
        s.configure("TLabelframe", background=bg, foreground=fg)
        s.configure("TLabelframe.Label", background=bg, foreground=fg)

        s.configure(
            "TButton", background=accent, foreground=accent_fg, borderwidth=0, padding=6
        )
        s.map("TButton", background=[("active", accent)])
        s.configure(
            "ThemeBtn.TButton",
            background=panel_bg,
            foreground=fg,
            borderwidth=1,
            relief="flat",
            padding=4,
        )
        s.map("ThemeBtn.TButton", background=[("active", panel_bg)])
        s.configure(
            "ThemeBtnActive.TButton",
            background=accent,
            foreground=accent_fg,
            borderwidth=0,
            relief="flat",
            padding=4,
        )
        s.map("ThemeBtnActive.TButton", background=[("active", accent)])

        for key, btn in self.theme_buttons.items():
            btn.configure(
                style="ThemeBtnActive.TButton" if key == name else "ThemeBtn.TButton"
            )

        s.configure("TEntry", fieldbackground=panel_bg, foreground=fg, insertcolor=fg)

        s.configure(
            "Treeview",
            background=tree_bg,
            fieldbackground=tree_bg,
            foreground=fg,
            rowheight=24,
        )
        s.configure("Treeview.Heading", background=accent, foreground=accent_fg)
        s.map(
            "Treeview",
            background=[("selected", accent)],
            foreground=[("selected", accent_fg)],
        )

        self.results_list.configure(
            bg=panel_bg,
            fg=fg,
            selectbackground=accent,
            selectforeground=accent_fg,
            highlightbackground=panel_bg,
            highlightcolor=accent,
        )

        self.status_label.configure(foreground=fg if name != "chiaro" else "#555555")

    def set_status(self, text):
        self.status_var.set(text)

    def on_search(self):
        query = self.search_var.get().strip()
        if not query:
            return
        self.results_list.delete(0, tk.END)
        self.set_status(f"Ricerca '{query}' in corso...")

        def task():
            try:
                results = api.geocode_city(query)
            except Exception as e:
                self.after(0, lambda: self.set_status(f"Errore nella ricerca: {e}"))
                return
            self.after(0, lambda: self._show_search_results(results))

        threading.Thread(target=task, daemon=True).start()

    def _show_search_results(self, results):
        self.search_results = results
        if not results:
            self.set_status("Nessun risultato trovato.")
            return
        for r in results:
            admin = r.get("admin1", "")
            country = r.get("country", "")
            label = (
                f"{r['name']}"
                + (f", {admin}" if admin else "")
                + (f" - {country}" if country else "")
            )
            self.results_list.insert(tk.END, label)
        self.set_status(
            f"{len(results)} risultati trovati. Doppio clic per selezionare."
        )

    def on_result_selected(self, event):
        sel = self.results_list.curselection()
        if not sel:
            return
        r = self.search_results[sel[0]]
        self.load_city(r["name"], r["latitude"], r["longitude"], r.get("country", ""))

    def load_city(self, name, lat, lon, country):
        self.set_status(f"Caricamento meteo per {name}...")

        def task():
            try:
                data = api.fetch_weather(lat, lon)
            except Exception as e:
                self.after(0, lambda: self._on_load_error(name, e))
                return
            self.after(0, lambda: self._update_ui(name, country, data))

        threading.Thread(target=task, daemon=True).start()

    def _on_load_error(self, name, error):
        self.set_status(f"Errore nel caricamento meteo per {name}: {error}")
        messagebox.showerror(
            "Errore", f"Impossibile scaricare il meteo per {name}.\n{error}"
        )

    def _update_ui(self, name, country, data):
        self._update_current(name, country, data)
        self._update_hourly(data)
        self._update_daily(data)
        self.set_status(f"Aggiornato alle {datetime.now().strftime('%H:%M:%S')}")

    def _update_current(self, name, country, data):
        current = data.get("current", {})
        desc, icon = describe_weather(current.get("weather_code"))

        title = name + (f", {country}" if country else "")
        self.city_label.config(text=title)
        self.temp_label.config(text=f"{icon} {current.get('temperature_2m', '--')}°C")
        self.detail_label.config(
            text=(
                f"{desc}  •  Percepita: {current.get('apparent_temperature', '--')}°C  •  "
                f"Umidità: {current.get('relative_humidity_2m', '--')}%  •  "
                f"Vento: {current.get('wind_speed_10m', '--')} km/h"
            )
        )

    def _update_hourly(self, data):
        for row in self.hourly_tree.get_children():
            self.hourly_tree.delete(row)

        hourly = data.get("hourly", {})
        times = hourly.get("time", [])
        temps = hourly.get("temperature_2m", [])
        codes = hourly.get("weather_code", [])

        now = datetime.now()
        start_idx = 0
        for i, t in enumerate(times):
            if datetime.fromisoformat(t) >= now:
                start_idx = i
                break

        for i in range(
            start_idx, min(start_idx + config.HOURLY_HOURS_SHOWN, len(times))
        ):
            hour = datetime.fromisoformat(times[i]).strftime("%H:%M")
            desc, icon = describe_weather(codes[i])
            self.hourly_tree.insert(
                "", tk.END, values=(hour, f"{temps[i]}°C", f"{icon} {desc}")
            )

    def _update_daily(self, data):
        for row in self.daily_tree.get_children():
            self.daily_tree.delete(row)

        daily = data.get("daily", {})
        dates = daily.get("time", [])
        mins = daily.get("temperature_2m_min", [])
        maxs = daily.get("temperature_2m_max", [])
        codes = daily.get("weather_code", [])

        giorni = ["Lun", "Mar", "Mer", "Gio", "Ven", "Sab", "Dom"]
        for i, d in enumerate(dates):
            day_label = giorni[datetime.fromisoformat(d).weekday()]
            desc, icon = describe_weather(codes[i])
            self.daily_tree.insert(
                "",
                tk.END,
                values=(day_label, f"{mins[i]}°C", f"{maxs[i]}°C", f"{icon} {desc}"),
            )
