import requests
import json
import os
# ...

API_URL = "https://api.tracker.gg/api/v2/bf6/standard/profile/steam/3000691765"
OUTPUT_FILE = "data.json"

# *** NOVÉ: Mnohem realističtější hlavičky prohlížeče (Chrome/Edge) ***
HEADERS = {
    # Použijeme User-Agent pro novější Chrome, který je často aktualizovaný
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
    'Accept': 'application/json, text/plain, */*', # Standardní hodnota prohlížeče
    'Accept-Language': 'cs,en-US;q=0.7,en;q=0.3', # Jazyky, které prohlížeč preferuje (česky a anglicky)
    'Accept-Encoding': 'gzip, deflate, br', # Říkáme, že umíme přijmout komprimovaná data
    'Referer': 'https://tracker.gg/', # Imitujeme, že požadavek přichází z domény tracker.gg
    'Connection': 'keep-alive', # Udržuje spojení aktivní
    # Někdy je potřeba i:
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'TE': 'trailers'
}

try:
    # Provede GET požadavek na API s realističtějšími hlavičkami
    response = requests.get(API_URL, headers=HEADERS) 
    response.raise_for_status() # Stále se spoléháme na to, že chybu 403 vyhodí zde.
    
    # ... zbytek kódu ...
