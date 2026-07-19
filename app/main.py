import sys
import asyncio

from scraping import get_data
from db import engine, Base
from models import print_data


async def main(operation: str) -> None:
    """The main coroutine.

    It creates all the tables that don't yet exist, and then
    calls the coroutine corresponding to the specified operation.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    if operation == "get_data":
        try:
            await get_data()
        except Exception as exc:
            print(f"Failed to get data! Exception: {exc}")
    elif operation == "print_data":
        try:
            await print_data()
        except Exception as exc:
            print(f"Failed to print data! Exception: {exc}")
    else:
        print("Invalid operation!")


if __name__ == "__main__":
    try:
        operation = sys.argv[1]
    except Exception:
        print("Usage: python3 main.py <get_data | print_data>")
    else:
        asyncio.run(main(operation))
