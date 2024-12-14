FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN python3 -m venv /venv

ENV PYTHONBUFFERED = 1 \
    PATH='/venv/bin/:$PATH'

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN alembic upgrade head

CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]