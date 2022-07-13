FROM python:3.9-slim

WORKDIR /app
ADD . /app
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD python3 scrape.py