import json
import os
import sys
import asyncio
from playwright.async_api import async_playwright

API_URL = "https://api.tracker.gg/api/v2/bf6/standard/profile/steam/3000691765"
OUTPUT_FILE = "data.json"

async def fetch_data_with_playwright():
    """Použije Playwright (virtuální prohlížeč) pro stažení dat."""
    
    # Použijeme Chromium, které je efektivní a je součástí instalace Playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        print(f"Playwright spuštěn. Načítám: {API_URL}")
        
        try:
            # Přejdeme na API URL. Playwright pošle všechny hlavičky jako skutečný prohlížeč.
            response = await page.goto(API_URL, wait_until="load", timeout=30000)
            
            # Kontrola status kódu
            if response.status != 200:
                print(f"CHYBA: Playwright obdržel status kód {response.status}. Text odpovědi:")
                print(await response.text())
                await browser.close()
                sys.exit(1)
            
            # Získání obsahu jako text a převod na JSON
            content_text = await response.text()
            data = json.loads(content_text)

            # Uložení JSON do souboru
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4) 

            print(f"Data úspěšně stažena pomocí Playwright a uložena do {OUTPUT_FILE}")

        except Exception as e:
            print(f"CHYBA PŘI POUŽITÍ PLAYWRIGHT: {e}")
            sys.exit(1)
        
        finally:
            await browser.close()

if __name__ == "__main__":
    # Playwright vyžaduje asynchronní spuštění (asyncio)
    asyncio.run(fetch_data_with_playwright())
