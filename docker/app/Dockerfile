FROM python:3.10

WORKDIR /src


COPY ../../docker/app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


COPY ../../src .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
