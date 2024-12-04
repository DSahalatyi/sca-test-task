FROM python:3.12.7-alpine3.20
LABEL maintainer="dsahalatyi@gmail.com"

RUN apk update && apk add python3-dev gcc libc-dev

WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install setuptools

COPY . .