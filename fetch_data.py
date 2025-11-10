import requests
import json
import os
import sys

API_URL = "https://api.tracker.gg/api/v2/bf6/standard/profile/steam/3000691765"
OUTPUT_FILE = "data.json"

# *** KOMPLETNÍ SADA HLAVIČEK PRO MAXIMÁLNÍ IMITACI PROHLÍŽEČE ***
HEADERS = {
    # 1. User-Agent: Moderní prohlížeč (Chrome/Edge)
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
    
    # 2. Accept Hlavičky: Jaká data a v jaké formě očekáváme
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'cs,en-US;q=0.7,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    
    # 3. Hlavičky pro Obcházení CORS / Odkazující stránka
    'Referer': 'https://tracker.gg/',
    'Connection': 'keep-alive',
    
    # 4. Hlavičky pro Fetch API (které Chrome používá pro AJAX volání)
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'TE': 'trailers'
}

try:
    print(f"Pokouším se stáhnout data z API: {API_URL}")
    
    # Provede GET požadavek s pokročilými hlavičkami
    response = requests.get(API_URL, headers=HEADERS, timeout=15) 
    response.raise_for_status() # Vyhodí chybu 4xx/5xx, pokud nastane
    
    print("Stahování bylo úspěšné. Parsuji data.")
    
    # Získá JSON data
    data = response.json()
    
    # Uloží JSON do souboru
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4) 

    print(f"Data úspěšně stažena a uložena do {OUTPUT_FILE}")

except requests.exceptions.HTTPError as e:
    # Blok pro zachycení chyby 403 Forbidden a dalších HTTP chyb
    if e.response.status_code == 403:
        print("CHYBA: 403 Forbidden přetrvává i s maximální imitací prohlížeče.")
        print("Server vyžaduje pravděpodobně API klíč nebo řešení přes Selenium/Playwright (což je pro GitHub Actions složité).")
    else:
        print(f"CHYBA PŘI STAHOVÁNÍ DAT Z API (HTTP Chyba): {e}")
    sys.exit(1)
    
except Exception as e:
    # Blok pro zachycení jiných obecných chyb
    print(f"CHYBA: Došlo k obecné chybě: {e}")
    sys.exit(1)
