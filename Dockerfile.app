FROM python:3.9-slim

WORKDIR /app

COPY ./requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY ./main.py /app/
COPY ./schemas.py /app/
COPY ./services.py /app/
COPY ./tasks.py /app/
COPY ./templates /app/templates/
COPY ./static /app/static/

CMD ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8787", "--timeout", "300"]