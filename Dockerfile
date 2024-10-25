FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /pressure_monitor
WORKDIR /pressure_monitor

COPY ./requirements /pressure_monitor/requirements

RUN pip install --upgrade pip && pip install -r requirements/prod.txt

COPY . /pressure_monitor