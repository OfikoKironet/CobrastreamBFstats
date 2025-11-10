import requests
import json
import os

API_URL = "https://api.tracker.gg/api/v2/bf6/standard/profile/steam/3000691765"
OUTPUT_FILE = "data.json"

try:
    # Provede GET požadavek na API
    response = requests.get(API_URL)
    response.raise_for_status() # Vyhodí chybu pro špatné stavové kódy (4xx nebo 5xx)

    # Získá JSON data
    data = response.json()

    # Volitelně: Můžeš data před uložením upravit, pokud je potřeba.
    # Např. vybrat jen určitou část:
    # relevant_data = data.get('data', {}) 
    # with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    #     json.dump(relevant_data, f, indent=4)

    # Uloží JSON do souboru
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4) # indent=4 pro hezké formátování

    print(f"Data úspěšně stažena a uložena do {OUTPUT_FILE}")

except requests.exceptions.RequestException as e:
    print(f"Chyba při stahování dat z API: {e}")
    exit(1)
except Exception as e:
    print(f"Došlo k chybě: {e}")
    exit(1)

# Vytvoř také soubor requirements.txt s obsahem:
# requests
