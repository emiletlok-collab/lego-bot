from playwright.sync_api import sync_playwright
import time
from config import BRANDS
from scoring import score_item
from telegram_utils import send_telegram_message

seen = set()

def scrape():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        print("🔥 BOT VINTED PRO lancé")
        send_telegram_message("TEST TELEGRAM OK")

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

                    for link in links:

                        if "/items/" not in link:
                            continue

                        if link in seen:
                            continue

                        seen.add(link)

                        print(link)

                        title = link.replace("-", " ").lower()

                        if not any(
                            keyword.lower() in title
                            for keyword in brand["keywords"]
                        ):
                            continue

                        item = {
                            "title": title,
                            "price": brand["max_price"] * 0.5,
                            "brand": brand["name"]
                        }

                        score, risk = score_item(item, brand)

                        if score < brand["min_score"]:
                            continue

                        if risk > brand["max_risk"]:
                            continue

                        text = f"""
🔥 BON DEAL DÉTECTÉ

🏷️ {brand['name']}
⭐ Score : {score}/100
⚠️ Risque : {risk}/100

🔗 {link}
"""

                        print("MESSAGE ENVOYE")

                        send_telegram_message(text)

                        time.sleep(2)

                time.sleep(30)

            except Exception as e:
                print("ERREUR :", e)
                time.sleep(10)

