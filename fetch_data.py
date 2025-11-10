import requests
import json
import os

API_URL = "https://api.tracker.gg/api/v2/bf6/standard/profile/steam/3000691765"
OUTPUT_FILE = "data.json"

# *** NOVÉ: Definice hlaviček pro imitaci prohlížeče ***
HEADERS = {
    # Můžeš použít libovolný řetězec, který imituje standardní prohlížeč.
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    # Provede GET požadavek na API s přidanými hlavičkami
    response = requests.get(API_URL, headers=HEADERS) # *** ZMĚNA ZDE ***
    response.raise_for_status() # Vyhodí chybu pro špatné stavové kódy (4xx nebo 5xx)

    # ... zbytek kódu ...

    # Získá JSON data
    data = response.json()
    
    # Uloží JSON do souboru
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4) 

    print(f"Data úspěšně stažena a uložena do {OUTPUT_FILE}")

except requests.exceptions.RequestException as e:
    # Zde ti bude chybová hláška (včetně status kódu)
    print(f"Chyba při stahování dat z API: {e}") 
    exit(1)
except Exception as e:
    print(f"Došlo k chybě: {e}")
    exit(1)
