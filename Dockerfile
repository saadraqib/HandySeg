FROM python:3

WORKDIR /app

RUN apt-get update && apt-get install -y python3-pip

COPY requirement.txt /app/

RUN pip install -r requirement.txt

RUN pip3 install jupyter


ENTRYPOINT ["jupyter","notebook", "--ip=0.0.0.0"]



