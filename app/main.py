import sys

from scraping import get_data
from db import engine, Base
from models import print_data


def main(operation: str):
    Base.metadata.create_all(engine)

    if operation == "get_data":
        try:
            get_data()
        except Exception as exc:
            print(f"Failed to get data! Exception: {exc}")
    elif operation == "print_data":
        try:
            print_data()
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
        main(operation)
