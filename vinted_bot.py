import requests
import time
from bs4 import BeautifulSoup

BOT_TOKEN = "8577522450:AAESsRExdGK-BIlas1lNwn-UHiGQ6vGCW4s"
CHAT_ID = "2146109835"

SEARCH_URL = "https://www.vinted.fr/catalog?search_text=lego+star+wars"

KEYWORDS = [
    "clone trooper",
    "boba fett",
    "dark trooper",
    "minifig",
    "ucs",
    "revan"
]

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, data=data)

print("🚀 Bot Vinted lancé")

send_telegram("✅ BOT CONNECTÉ")

seen = set()

while True:
    try:
        r = requests.get(
            SEARCH_URL,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        soup = BeautifulSoup(r.text, "lxml")

        links = soup.find_all("a")

        for link in links:
            href = link.get("href")

            if not href:
                continue

            if "/items/" not in href:
                continue

            title = link.get_text().lower()

            if not any(
                keyword in title
                for keyword in KEYWORDS
            ):
                continue

            if href in seen:
                continue

            seen.add(href)

            full_link = "https://www.vinted.fr" + href

            print("🔥", title)

            send_telegram(
                f"🔥 LEGO trouvé\n\n{title}\n\n{full_link}"
            )

        time.sleep(60)

    except Exception as e:
        print("Erreur :", e)
        time.sleep(30)
