from sqlalchemy import String, Integer, func, select
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
    largest = (
        select(
            Country.region,
            Country.name.label("largest_country"),
            Country.population.label("largest_population"),
            func.row_number().over(
                partition_by=Country.region,
                order_by=Country.population.desc(),
            ).label("rn"),
        )
    ).subquery()

    smallest = (
        select(
            Country.region,
            Country.name.label("smallest_country"),
            Country.population.label("smallest_population"),
            func.row_number()
            .over(
                partition_by=Country.region,
                order_by=Country.population.asc(),
            )
            .label("rn"),
        )
    ).subquery()

    query = (
        select(
            Country.region,
            func.sum(Country.population).label("region_population"),
            largest.c.largest_country,
            largest.c.largest_population,
            smallest.c.smallest_country,
            smallest.c.smallest_population,
        )
        .join(
            largest,
            (Country.region == largest.c.region) & (largest.c.rn == 1),
        )
        .join(
            smallest,
            (Country.region == smallest.c.region) & (smallest.c.rn == 1),
        )
        .group_by(
            Country.region,
            largest.c.largest_country,
            largest.c.largest_population,
            smallest.c.smallest_country,
            smallest.c.smallest_population,
        )
        .order_by(Country.region)
    )

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
