# syntax=docker/dockerfile:1
FROM python:3.10-alpine

COPY ./requirements.txt /tmp/requirements.txt
RUN apk update && apk add gcc libc-dev make git libffi-dev openssl-dev python3-dev libxml2-dev libxslt-dev
# install dependencies
RUN pip install --upgrade pip && pip install -r /tmp/requirements.txt

COPY ./ /

