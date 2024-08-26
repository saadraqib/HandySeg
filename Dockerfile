FROM python:3

WORKDIR /app

RUN apt-get update && apt-get install -y python3-pip

COPY requirement.txt /app/





