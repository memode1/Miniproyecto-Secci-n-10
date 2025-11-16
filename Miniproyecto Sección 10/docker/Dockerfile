FROM python:3.11

WORKDIR /app

COPY docker/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ /app/

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
