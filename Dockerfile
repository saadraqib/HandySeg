FROM python:3

WORKDIR /app

RUN apt-get update && apt-get install -y python3-pip

COPY requirement.txt /app/handyseg/

# or 
#COPY HandySeg/line_segmentation.py /app/HandySeg/
# COPY HandySeg/preprocessing.py /app/HandySeg/
# COPY HandySeg/word_segmentation.py /app/HandySeg/





