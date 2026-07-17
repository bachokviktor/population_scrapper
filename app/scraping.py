import requests
from bs4 import BeautifulSoup, Tag
from sqlalchemy import delete

from db import Session
from models import Country


def _fetch_info() -> str:
    with requests.Session() as session:
        session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/137.0.0.0 Safari/537.36"
            )
        })

        response = session.get(
            (
                "https://en.wikipedia.org/w/index.php?title=List_of_countries"
                "_by_population_(United_Nations)&oldid=1215058959"
             ),
            timeout=10
        )
        response.raise_for_status()

        return response.text


def _parse_countires(rows: list[Tag]) -> list[Country]:
    countries = []
    for row in rows:
        cols = row.find_all("td")
        if not cols:
            continue

        name = cols[0].get_text(strip=True).split("[")[0]
        if name == "World":
            continue

        population_raw = cols[2].get_text(strip=True)
        if population_raw == "N/A":
            continue

        population = int(population_raw.replace(",", ""))

        region = cols[4].get_text(strip=True)

        countries.append(
            Country(
                name=name,
                population=population,
                region=region,
            )
        )

    return countries


def get_data() -> None:
    data = _fetch_info()

    soup = BeautifulSoup(data, "html.parser")
    table = soup.select_one("table.wikitable")

    if not table:
        raise Exception("Failed to parse data!")

    rows = table.select("tbody tr")

    countries = _parse_countires(rows)

    with Session.begin() as session:
        session.execute(delete(Country))
        session.add_all(countries)

    print(f"Saved {len(countries)} countries.")
