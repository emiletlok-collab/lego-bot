FAKE_KEYWORDS = [
    "inspiré",
    "inspi",
    "replica",
    "réplique",
    "fake",
    "copie",
    "aaa",
    "1:1",
    "contre façon",
    "contrefaçon",
    "dhgate",
    "aliexpress"
]

GOOD_WORDS = [
    "facture",
    "authentique",
    "receipt",
    "certificat",
    "boite",
    "box",
    "dustbag",
    "garantie"
]

def score_item(item, brand):

    title = item["title"].lower()

    score = 50
    risk = 0

    for word in GOOD_WORDS:
        if word in title:
            score += 10

    for word in FAKE_KEYWORDS:
        if word in title:
            risk += 40
            score -= 20

    price = item["price"]

    if price < brand["max_price"] * 0.2:
        risk += 30

    if price < brand["max_price"] * 0.1:
        risk += 50

    score = max(0, min(score, 100))
    risk = max(0, min(risk, 100))

    return score, risk
