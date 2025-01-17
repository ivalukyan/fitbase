FROM python:3.10-alpine

WORKDIR /app


COPY ./docker/app/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt


COPY ./src /app

EXPOSE 8000

CMD ["python", "main.py", "run"]
