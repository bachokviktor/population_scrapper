from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


engine = create_engine(
    "postgresql+psycopg://postgres:postgres@db:5432/postgres"
)

Session = sessionmaker(engine)


class Base(DeclarativeBase):
    pass
