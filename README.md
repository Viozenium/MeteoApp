# Meteo App

Questo progetto Python permette di visualizzare informazioni meteo tramite un’interfaccia grafica semplice, con una schermata principale, una sezione meteo e una pagina informativa.

## Descrizione:
L’applicazione utilizza una GUI realizzata con Tkinter per consentire all’utente di:
- Aprire una finestra meteo che mostra le temperature previste per le prossime ore in diverse città.
- Visualizzare una schermata “Info” con dettagli sull’autore e link GitHub.

Il modulo meteo recupera i dati tramite API (Open-Meteo), gestendo cache e retry automatici per migliorare affidabilità e prestazioni.
I dati vengono poi mostrati in una finestra dedicata sotto forma di log testuale.

## Funzionalità principali:
- Interfaccia grafica semplice e intuitiva
- Visualizzazione meteo per più città (Roma, Tokyo, New York)
- Sistema di logging nella finestra meteo
- Gestione degli errori (in caso di dati non disponibili)
- Cache delle richieste API per ridurre le chiamate
- Pulsanti disabilitati temporaneamente per evitare conflitti tra finestre

Nota:
I dati meteo dipendono dalla disponibilità dell’API. In caso di errore o problemi di connessione, potrebbero non essere visualizzate informazioni.

## Requisiti:
- Python 3.x

### Librerie necessarie:
- tkinter (inclusa di default)
- pandas
- openmeteo-requests
- requests-cache
- retry-requests
- python-dotenv
- Connessione internet attiva per il recupero dei dati meteo

### Configurazione (opzionale):
È possibile configurare alcuni parametri tramite file .env:
- CACHE_EXPIRATION → durata cache (default: 3600)
- RETRY_COUNT → numero tentativi in caso di errore
- BACKOFF_FACTOR → ritardo tra i retry

### Avvio:
Eseguire il file principale (main.py).
Da lì è possibile accedere a tutte le funzionalità tramite i pulsanti.

---

# FAQ

1) Si può migliorare?
Sì, in molti modi, ad esempio aggiungendo la ricerca per una città specifica e altre funzionalità.

2) Perché questa app?
L’origine di questa app deriva da un progetto di Generation Italy:
- AI Training for Software Developer Graduates v2

3) È generata da IA?
No, almeno inizialmente.
Il README invece è 100% IA.

4) In che senso?
Avevo già sviluppato in passato un’app meteo.
Questo progetto nasce dall’unione di codice proveniente da più progetti, successivamente riorganizzato anche con l’aiuto dell’IA.

5) Che prompt hai usato?
"Mantenendo la struttura, le funzioni e il corretto funzionamento, ristruttura il codice: (codice qui)"
Manco a dirlo, ha rotto tutto.
I prompt successivi sono serviti per sistemare i problemi iniziali.

6) Come funziona il codice?
L’applicazione va avviata tramite main.py.
Sono presenti alcuni bug che vengono gestiti o "soppressi".

7) Ci sono bug noti?
Sì:
- meteo.py, se lanciato come standalone, rimane aperto come processo "fantasma"
- Se si chiude la finestra principale mentre la finestra meteo è attiva, possono verificarsi delle eccezioni

Entrambi i problemi derivano da Tkinter.

8) Hai intenzione di sistemarli?
No.

9) Perché la UI?
Generalmente sviluppo applicazioni pensate per essere distribuite come eseguibili.
Comando utilizzato:
pyinstaller --onefile --windowed --add-data ".env;." main.py