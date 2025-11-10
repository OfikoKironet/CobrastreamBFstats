import json
import os
import sys
import asyncio
from playwright.async_api import async_playwright

API_URL = "https://api.tracker.gg/api/v2/bf6/standard/profile/steam/3000691765"
OUTPUT_FILE = "data.json"

async def fetch_data_with_playwright():
    """Použije Playwright (Firefox) pro stažení dat a pokusí se obejít Cloudflare."""
    
    async with async_playwright() as p:
        # Zkusíme Firefox místo Chromium, je méně častý pro boty
        browser = await p.firefox.launch() 
        
        # Nastavení kontextu, aby se choval více jako skutečný uživatel
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0',
            locale='en-US',
            viewport={"width": 1920, "height": 1080}
        )
        page = await context.new_page()

        print(f"Playwright (Firefox) spuštěn. Načítám: {API_URL}")
        
        try:
            # Přejdeme na API URL. Cloudflare uvidí komplexní požadavky
            response = await page.goto(API_URL, wait_until="domcontentloaded", timeout=60000)
            
            # Ponecháme čas na dokončení Cloudflare Javascript Challenge (možná 5-10s)
            await page.wait_for_timeout(7000) # Počkáme 7 sekund na Cloudflare ověření

            # Opětovné načtení obsahu pro případ, že mezitím Cloudflare Challenge proběhla
            content_text = await page.content()
            
            # Server vrací HTML (stránku o blokování) místo JSON. 
            # Potřebujeme získat konečnou URL, na kterou se prohlížeč přesměroval:
            final_url = page.url
            
            # Pokud Playwright úspěšně prošel, finální URL by měla být původní API URL
            if final_url != API_URL:
                 # Pokud se Playwright přesměroval (třeba na 404), zkusíme získat tělo znovu
                 print(f"Playwright byl přesměrován na: {final_url}")
            
            # Nyní zkusíme najít na stránce JSON, který byl zobrazen, nebo ho zkusit parsovat.
            # Musíme zkontrolovat, zda content_text NENÍ zpráva o blokování
            if "Blocked Request" in content_text or "Cloudflare" in content_text:
                print("CHYBA: Playwright Challenge selhala. Stále blokováno Cloudflare.")
                print(f"Konečný Status: {response.status}")
                sys.exit(1)


            # Pokud se nejedná o blokaci, zkusíme parsovat obsah jako JSON.
            # To je nejtěžší část, protože nevíme, jestli se Playwright dostal k JSON tělu.
            data = json.loads(content_text)
            
            # Uložení JSON do souboru
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4) 

            print(f"Data úspěšně stažena (Firefox) a uložena do {OUTPUT_FILE}")

        except Exception as e:
            print(f"CHYBA PŘI POUŽITÍ PLAYWRIGHT (Firefox): {e}")
            sys.exit(1)
        
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(fetch_data_with_playwright())
