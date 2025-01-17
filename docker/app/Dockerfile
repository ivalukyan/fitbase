FROM python:3.10-buster

WORKDIR /bot

COPY ../requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ../bot .

CMD ["python", "bot.py"]