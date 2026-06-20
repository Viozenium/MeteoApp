# Meteo App

## Italiano

Questa applicazione Python permette di cercare qualsiasi città del mondo e visualizzarne il meteo corrente, le previsioni orarie e quelle giornaliere, tramite un'interfaccia grafica semplice e personalizzabile.

### Descrizione
L'applicazione utilizza una GUI realizzata con Tkinter per consentire all'utente di:
- Cercare una città qualsiasi tramite il servizio di geocoding gratuito di Open-Meteo, oppure selezionarne una rapidamente tra le città preferite (Roma, Tokyo, New York).
- Visualizzare il meteo corrente (temperatura, percepita, umidità, vento) e le previsioni nelle ore e nei giorni successivi, mostrate in tabelle.
- Cambiare l'aspetto dell'app tra tre temi (Chiaro, Scuro, Colorato) tramite tre pulsanti dedicati.
- Aprire una finestra "Info" con i miei dettagli e il link GitHub, che adotta automaticamente i colori del tema attivo.

Il modulo `api.py` recupera i dati tramite le API gratuite di Open-Meteo (geocoding + forecast), gestendo cache e retry automatici per migliorare affidabilità e prestazioni.
Le chiamate di rete vengono eseguite in thread separati, così l'interfaccia non si blocca durante il caricamento.

### Funzionalità principali
- Ricerca di qualsiasi città del mondo, senza elenco fisso
- Città preferite come scorciatoie rapide
- Meteo corrente + previsioni orarie e giornaliere in tabelle
- Tre temi grafici selezionabili a runtime
- Finestra "Info" con stile coerente al tema attivo
- Cache delle richieste API per ridurre le chiamate
- Gestione degli errori (dati non disponibili, problemi di rete)
- Codice organizzato secondo il principio di Separazione dei Compiti (vedi sezione "Struttura del progetto")

### Struttura del progetto
```
meteo_app/
├── .env              # configurazione
├── config.py         # legge .env, espone le costanti
├── weather_codes.py  # mappatura codici meteo WMO -> testo/icona
├── themes.py         # palette colori dei 3 temi
├── api.py            # chiamate HTTP a Open-Meteo
├── ui.py             # interfaccia grafica
├── info.py           # finestra Info / About
└── main.py           # punto di ingresso
```

### Requisiti
1. Python 3.x
2. Connessione internet attiva per il recupero dei dati meteo

#### Librerie necessarie
- tkinter (inclusa di default)
- requests
- requests-cache
- retry-requests
- python-dotenv

### Configurazione (file `.env`)
- `CACHE_EXPIRATION`               -> durata cache in secondi (default: 3600)
- `RETRY_COUNT`                    -> numero tentativi in caso di errore (default: 3)
- `BACKOFF_FACTOR`                 -> ritardo tra i retry (default: 0.3)
- `DEFAULT_THEME`                  -> tema all'avvio: chiaro / scuro / colorato (default: chiaro)
- `WINDOW_WIDTH`, `WINDOW_HEIGHT`  -> dimensioni iniziali della finestra (default: 1100x750)
- `FORECAST_DAYS`                  -> giorni di previsione richiesti all'API (default: 6)
- `HOURLY_HOURS_SHOWN`             -> ore mostrate nella tabella oraria (default: 8)
- `GEOCODING_RESULTS_LIMIT`        -> numero massimo di risultati nella ricerca città (default: 8)
- `GEOCODING_LANGUAGE`             -> lingua dei risultati di ricerca (default: it)

### Utilizzo
```bash
python main.py
```

### Note
- Le ricerche e i caricamenti meteo girano in thread separati per non bloccare l'interfaccia.
- In caso di errore di rete, lo stato precedente non viene alterato e viene mostrato un messaggio descrittivo.

### Motivazione
Questo progetto nasce dall'esigenza di avere un'app meteo semplice ma ben strutturata, capace di cercare qualsiasi città senza dover modificare il codice ogni volta.

---

## English

This Python application lets you search for any city in the world and view its current weather, hourly forecast, and daily forecast, through a simple and customizable graphical interface.

### Description
The application uses a Tkinter-based GUI to let the user:
- Search for any city via Open-Meteo's free geocoding service, or quickly pick one from the favorite cities (Rome, Tokyo, New York).
- View current weather (temperature, feels-like, humidity, wind) and upcoming hourly/daily forecasts, shown in tables.
- Switch the app's appearance between three themes (Light, Dark, Colored) using three dedicated buttons.
- Open an "Info" window with my details and a GitHub link, automatically styled to match the active theme.

The `api.py` module fetches data through Open-Meteo's free APIs (geocoding + forecast), handling caching and automatic retries to improve reliability and performance.
Network calls run on separate threads so the UI never freezes while loading.

### Main features
- Search for any city worldwide, no fixed list
- Favorite cities as quick shortcuts
- Current weather + hourly and daily forecast tables
- Three runtime-switchable themes
- "Info" window styled consistently with the active theme
- Request caching to reduce API calls
- Error handling (unavailable data, network issues)
- Code organized following the Separation of Concerns principle (see "Project structure")

### Requirements
1. Python 3.x
2. Active internet connection to fetch weather data

#### Required libraries
- tkinter (included by default)
- requests
- requests-cache
- retry-requests
- python-dotenv

### Usage
```bash
python main.py
```

### Notes
- Searches and weather lookups run on separate threads to keep the UI responsive.
- On network errors, the previous state is left unchanged and a descriptive message is shown.

### Motivation
This project was born out of the need for a simple but well-structured weather app, able to search any city without ever touching the code again.

---

## FAQ

1) **Si può migliorare?**
   Sì, in molti modi: unità di misura alternative (°F), grafici delle temperature, salvataggio delle ultime ricerche, notifiche meteo.

2) **Perché questa app?**
   L'origine iniziale di questa app deriva da un progetto di Generation Italy: AI Training for Software Developer Graduates v2.

3) **È generata da IA?**
   No, almeno inizialmente, i file `weather_codes.py` e `.env` sono generati da IA.
   Il README invece è scritto parzialmente con l'aiuto dell'IA.

4) **In che senso?**
   Avevo già sviluppato in passato un'app meteo.
   Questo progetto nasce dall'unione di codice proveniente da più progetti, poi riorganizzato, ampliato (ricerca città, temi, finestra Info) e suddiviso in più file.

5) **Che prompt hai usato?**
   Nessun prompt unico, una serie di richieste incrementali, una per ogni miglioramento (configurazione via `.env` e codifica `weather_codes.py`, fix di bug).

6) **Come funziona il codice?**
   L'applicazione va avviata tramite `main.py`, che assembla i vari moduli (`config`, `api`, `ui`, `themes`, `weather_codes`, `info`).

7) **Ci sono bug noti?**
   Il problema del processo "fantasma" rimasto attivo in console dopo la chiusura, presente nelle prime versioni, è stato risolto dalla v1.2.0.
   Al momento non ci sono bug noti.

8) **Hai intenzione di sistemare eventuali bug futuri?**
   Sì: a differenza dei primi prototipi, qui il codice è organizzato per responsabilità (SoC), quindi è più semplice da mantenere e correggere.

9) **Perché la UI?**
   Generalmente sviluppo applicazioni pensate per essere distribuite come eseguibili.

---

## Changelog

### v2.0.0
- Aggiunti 3 temi grafici (Chiaro, Scuro, Colorato)
- Dimensione di default della finestra aumentata (1100x750, configurabile via `.env`)
- La finestra "Info" ora adotta automaticamente i colori del tema attivo nell'app principale
- Architettura a più file consolidata e documentata (vedi "Struttura del progetto")
- Aggiunta la barra di ricerca città con geocoding gratuito (Open-Meteo Geocoding API), al posto della lista fissa di città
- Aggiunta la visualizzazione di meteo corrente, previsioni orarie e giornaliere in tabelle, al posto del semplice log testuale
- Aggiunta la finestra "Info / About" con autore, versione e link GitHub
- Selettore del tema convertito da menu a tendina a 3 pulsanti rapidi (☀ Chiaro / 🌙 Scuro / 🎨 Colorato), per evitare l'effetto "tendina selezionata"
- Refactoring completo: codice suddiviso in più file seguendo il principio di Separazione dei Compiti (`config.py`, `weather_codes.py`, `themes.py`, `api.py`, `ui.py`, `main.py`)
- Tutte le costanti di configurazione spostate in `config.py`, caricate da `.env`

### v1.1.0
- File `.env` ampliato con nuove variabili (dimensioni finestra, tema di default, durata previsioni, ecc.)
- Risolto il bug del processo "fantasma" rimasto attivo in console dopo la chiusura della finestra in modalità standalone
- Le chiamate di rete ora girano in thread separati per non bloccare la UI
- Rimosse le dipendenze da `pandas` e `openmeteo-requests`; le chiamate API ora usano direttamente `requests`

### v1.0.0
- Prima versione: interfaccia Tkinter minimale con log testuale e 3 città fisse (Roma, Tokyo, New York)
- Recupero dati meteo tramite la libreria `openmeteo-requests`, con cache (`requests-cache`) e retry (`retry-requests`)