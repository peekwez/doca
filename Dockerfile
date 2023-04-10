FROM python:3.11-slim

LABEL author="Kwesi P Apponsah" author-email="kwesiparry@gmail.com"

WORKDIR /app

# add directories
ADD ./ /app
RUN pip install --upgrade pip
RUN pip install .
RUN rm -fr /app/*
RUN mkdir -p /app/secrets
RUN mkdir -p /app/settings