#!/usr/local/bin/python3
from bs4 import BeautifulSoup
from typing import Final
import cloudscraper
import json

url: Final[str] = "https://yakkun.com/sv/stats_list.htm"
columns: Final[list[str]] = ["number", "name", "H", "A", "B", "C", "D", "S"]

def main():
    scraper = cloudscraper.create_scraper(delay=10, browser={'custom': 'ScraperBot/1.0',})
    response = scraper.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    data = soup.select('tr[id^=p]')

    results = []

    for row in data:
        pokemon = get_data_from_content_generator(row.contents)
        results.append(pokemon)

    with open("pokemon.json", "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

def get_data_from_content_generator(contents):
    pokemon = { "number": None, "name": None, "H": None, "A": None, "B": None, "C": None, "D": None, "S": None }
    for index, child in enumerate(contents):
        try:
            column = columns[index]
        except IndexError:
            continue
        finally:
            pokemon[column] = child.text
    return pokemon

if __name__ == "__main__":
    main()