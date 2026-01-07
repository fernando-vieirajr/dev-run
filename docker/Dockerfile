FROM python:3.11-slim

WORKDIR /app

COPY src ./src
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p logs

CMD ["python", "src/main.py"]
