FROM python:3.10

WORKDIR /src

COPY ../../docker/bot/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ../../src /src

CMD ["python", "bot/main.py", "run"]
