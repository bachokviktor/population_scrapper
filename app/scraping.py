import httpx
from bs4 import BeautifulSoup, Tag
from sqlalchemy import delete

from db import async_session
from models import Country


async def _fetch_info() -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            (
                "https://en.wikipedia.org/w/index.php?title=List_of_countries"
                "_by_population_(United_Nations)&oldid=1215058959"
            ),
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (X11; Linux x86_64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/137.0.0.0 Safari/537.36"
                )
            },
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


async def get_data() -> None:
    """Scrape the data and save it to the database.

    The database table is also cleared every time before
    saving the data.
    """
    data = await _fetch_info()

    soup = BeautifulSoup(data, "html.parser")
    table = soup.select_one("table.wikitable")

    if not table:
        raise Exception("Failed to parse data!")

    rows = table.select("tbody tr")

    countries = _parse_countires(rows)

    async with async_session() as session:
        async with session.begin():
            await session.execute(delete(Country))
            session.add_all(countries)

    print(f"Saved {len(countries)} countries.")
