FROM python:3

RUN apt-get update && apt-get install -y python3-pip

COPY requirement.txt .

RUN pip install -r requirement.txt

RUN pip3 install jupyter

RUN useradd -ms /bin/bash demo

USER demo

WORKDIR /home/demo

ENTRYPOINT ["jupyter","notebook", "--ip=0.0.0.0"]
