import requests
import time
import csv

SET_CODE = "unf"  # March of the Machine set code (lowercase)
BASE_URL = "https://api.scryfall.com/cards/search"

def fetch_mom_cards():
    params = {
        "q": f"e:{SET_CODE}",  # search by set code
        "unique": "prints"
    }
    cards = []
    url = BASE_URL

    while url:
        response = requests.get(url, params=params if url == BASE_URL else None)
        if response.status_code != 200:
            print(f"Failed to fetch data: {response.status_code}")
            break
        data = response.json()
        cards.extend(data.get("data", []))
        url = data.get("next_page")
        params = None  # only send params on first request

        time.sleep(0.1)  # be kind to API

    return cards

def save_cards_to_csv(cards, filename="mom_cards.csv"):
    keys = [
        "name",
        "mana_cost",
        "type_line",
        "rarity",
        "oracle_text",
        "set_name",
        "collector_number",
        "usd",          # price in USD (nonfoil)
        "usd_foil",     # price in USD (foil)
        "usd_etched",   # price in USD (etched foil, if any)
    ]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for card in cards:
            prices = card.get("prices", {})
            row = {
                "name": card.get("name"),
                "mana_cost": card.get("mana_cost"),
                "type_line": card.get("type_line"),
                "rarity": card.get("rarity"),
                "oracle_text": card.get("oracle_text", "").replace("\n", " "),
                "set_name": card.get("set_name"),
                "collector_number": card.get("collector_number"),
                "usd": prices.get("usd"),
                "usd_foil": prices.get("usd_foil"),
                "usd_etched": prices.get("usd_etched"),
            }
            writer.writerow(row)
    print(f"Saved {len(cards)} cards to {filename}")

if __name__ == "__main__":
    cards = fetch_mom_cards()
    save_cards_to_csv(cards)
