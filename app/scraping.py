import os
import httpx
from bs4 import BeautifulSoup
from sqlalchemy import delete

from db import async_session
from models import Country
from parsers import (
    _parse_countires_wikipedia,
    _parse_countires_statisticstimes,
)


SOURCES = {
    "wikipedia": (
        (
            "https://en.wikipedia.org/w/index.php?title=List_of_countries"
            "_by_population_(United_Nations)&oldid=1215058959"
        ),
        _parse_countires_wikipedia,
    ),
    "statisticstimes": (
        (
            "https://statisticstimes.com/demographics"
            "/countries-by-population.php"
        ),
        _parse_countires_statisticstimes,
    ),
}


async def _fetch_info(url: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
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


async def get_data() -> None:
    """Scrape the data and save it to the database.

    The database table is also cleared every time before
    saving the data.
    """
    source = os.getenv("DATA_SOURCE", "wikipedia")

    if source not in SOURCES:
        raise Exception("Invalid data source!")

    url, parser = SOURCES.get(source)

    data = await _fetch_info(url)

    soup = BeautifulSoup(data, "html.parser")

    countries = parser(soup)

    async with async_session() as session:
        async with session.begin():
            await session.execute(delete(Country))
            session.add_all(countries)

    print(f"Saved {len(countries)} countries from {source}.")
