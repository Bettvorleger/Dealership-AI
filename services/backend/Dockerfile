FROM python:3.9-buster

RUN mkdir app
WORKDIR /app

ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONPATH=.

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# for migrations
COPY migrations ./src
COPY pyproject.toml ./src
COPY main.py .

COPY src ./src

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]