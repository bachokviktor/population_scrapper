from bs4 import BeautifulSoup

from models import Country


def _parse_countires_wikipedia(soup: BeautifulSoup) -> list[Country]:
    table = soup.select_one("table.wikitable")

    if not table:
        raise Exception("Failed to parse data!")

    rows = table.select("tbody tr")

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


def _parse_countires_statisticstimes(soup: BeautifulSoup) -> list[Country]:
    table = soup.select_one("table#table_id")

    if not table:
        raise Exception("Failed to parse data!")

    rows = table.select("tbody tr")

    countries = []
    for row in rows:
        cols = row.find_all("td")
        if not cols:
            continue

        name = cols[0].get_text(strip=True)

        population = int(cols[3].get_text(strip=True).replace(",", ""))

        region = cols[8].get_text(strip=True)

        countries.append(
            Country(
                name=name,
                population=population,
                region=region,
            )
        )

    return countries
