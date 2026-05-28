from playwright.sync_api import sync_playwright
import time
from config import BRANDS
from telegram_utils import send_telegram_message

seen = set()

def scrape():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("🚀 BOT VINTED PRO lancé")
        send_telegram_message("TEST DEPLOY OK")

        while True:
            try:
                for brand in BRANDS:
                    url = f"https://www.vinted.fr/catalog?search_text={brand['query']}"
                    page.goto(url)
                    time.sleep(5)

                    links = page.locator("a").evaluate_all(
                        "(elements) => elements.map(e => e.href)"
                    )

                    print(f"{brand['name']} -> {len(links)} liens")
                       
                    print(links[:20])                    

                    for link in links:
                        if "/items/" not in link:
                            continue

                        if link in seen:
                            continue

                        seen.add(link)

                        print(link)

                        text = f"""
TEST VINTED

🏷️ {brand['name']}
🔗 {link}
"""

                        print("MESSAGE ENVOYÉ")
                        send_telegram_message(text)
                        time.sleep(2)

                time.sleep(30)

            except Exception as e:
                print("ERREUR :", e)
                time.sleep(10)
