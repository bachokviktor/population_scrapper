FROM python:3.14.6-slim-trixie

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt update && apt install -y build-essential binutils libpq-dev

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade pip

RUN pip install -r requirements.txt

COPY . .
