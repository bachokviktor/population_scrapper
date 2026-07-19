# Population Scrapper

Asynchronous web scrapper built with sqlalchemy, httpx, and beautifulsoup4.

This application collects the data about the population of the world's countries and saves them to a database. It also can aggregate a summary across regions.

Information is collected from:

- [List of countries and dependencies by population (United Nations)](https://en.wikipedia.org/w/index.php?title=List_of_countries_by_population_(United_Nations)&oldid=1215058959)
- [List of countries by population 2025](https://statisticstimes.com/demographics/countries-by-population.php)

## Quickstart

Build the images

``` shell
docker compose build
```

Collect the data

``` shell
docker compose up get_data
```

Get a summary

``` shell
docker compose up print_data
```

You can also change the source of data using the `DATA_SOURCE` environment variable

Available sources: `wikipedia`, `statisticstimes`

``` shell
DATA_SOURCE='statisticstimes' docker compose up get_data
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
