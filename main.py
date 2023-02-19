#!/usr/local/bin/python3
from bs4 import BeautifulSoup
from typing import Final
import cloudscraper
import urllib.request
import json

def main():
    data = get_base_stats()
    set_type_data(data)

    with open("pokemon.json", "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_base_stats():
    url: Final[str] = "https://yakkun.com/sv/stats_list.htm?mode=all"

    scraper = cloudscraper.create_scraper(delay=10, browser={'custom': 'ScraperBot/1.0',})
    response = scraper.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    data = soup.select('tr[id^=p]')

    results = []

    for row in data:
        pokemon = get_data_from_content_generator(row.contents)
        results.append(pokemon)
    return results

def get_data_from_content_generator(contents):
    columns: Final[list[str]] = ["number", "name", "H", "A", "B", "C", "D", "S"]
    pokemon = { "number": None, "name": None, "H": None, "A": None, "B": None, "C": None, "D": None, "S": None }
    for index, child in enumerate(contents):
        try:
            column = columns[index]
            pokemon[column] = child.text
        except IndexError:
            continue
    return pokemon

def set_type_data(data):
    for d in data:
        number = int(d["number"])
        url = "https://pokeapi.co/api/v2/pokemon/{0}".format(number)
        request = urllib.request.Request(url)
        request.add_header('User-Agent',"cheese")

        with urllib.request.urlopen(request) as response:
            body = json.loads(response.read())
            if (response.getcode() != 200):
                continue
            types = [type.get("type").get("name") for type in body["types"]]
            d["types"] = types

if __name__ == "__main__":
    main()