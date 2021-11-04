# pull official base image
FROM python:3.8-slim-buster

# set working directory
WORKDIR /project

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# add and install requirements
COPY requirements.txt .

## install dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y librdkafka-dev ca-certificates && \
    apt-get clean && \
    python3 -m pip install -r requirements.txt

COPY chain.pem .
RUN cat chain.pem >> /usr/local/lib/python3.8/site-packages/certifi/cacert.pem

COPY chain.pem /usr/local/share/ca-certificates/chain.crt
RUN update-ca-certificates

COPY . /project/



