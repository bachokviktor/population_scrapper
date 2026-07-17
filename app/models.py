from sqlalchemy import String, Integer, func, select, text
from sqlalchemy.orm import Mapped, mapped_column

from db import Session, Base


class Country(Base):
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[int] = mapped_column(String(120), unique=True)
    population: Mapped[int] = mapped_column(Integer)
    region: Mapped[str] = mapped_column(String(120))

    def __repr__(self) -> str:
        return f"<{self.name} ({self.region}): {self.population}>"


def print_data() -> None:
    query = text("""
    WITH largest AS (
    SELECT
      region,
      name AS largest_country,
      population AS largest_population,
      ROW_NUMBER() OVER (
        PARTITION BY region
        ORDER BY population DESC
      ) AS rn
    FROM countries
    ),
    smallest AS (
    SELECT
      region,
      name AS smallest_country,
      population AS smallest_population,
      ROW_NUMBER() OVER (
        PARTITION BY region
        ORDER BY population ASC
      ) AS rn
    FROM countries
    )
    SELECT
      c.region,
      SUM(c.population) AS region_population,
      l.largest_country,
      l.largest_population,
      s.smallest_country,
      s.smallest_population
    FROM countries AS c
    JOIN largest AS l ON c.region = l.region AND l.rn = 1
    JOIN smallest AS s ON c.region = s.region AND s.rn = 1
    GROUP BY
      c.region,
      l.largest_country,
      l.largest_population,
      s.smallest_country,
      s.smallest_population
    ORDER BY c.region;
    """)

    with Session() as session:
        print(
            "Region | Population | Largest Country | "
            "Largest Population | Smallest Country | Smallest Population"
        )
        print("-"*100)

        for row in session.execute(query):
            print(
                f"{row.region} | "
                f"{row.region_population} | "
                f"{row.largest_country} | "
                f"{row.largest_population} | "
                f"{row.smallest_country} | "
                f"{row.smallest_population}"
            )
