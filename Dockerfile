# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY ./webapp/requirements.txt /code/
COPY ./webapp/requirements_dev.txt /code/
RUN pip install -r /code/requirements_dev.txt
COPY . /code/
