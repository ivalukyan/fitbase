FROM python:3.10-alpine

WORKDIR /bot

COPY ./src/bot/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src /bot

CMD ["python", "bot.py", "run"]
