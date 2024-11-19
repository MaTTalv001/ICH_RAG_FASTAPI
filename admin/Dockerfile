FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
  build-essential \
  && rm -rf /var/lib/apt/lists/*

# requirements.txtをadmin/直下からコピー
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN mkdir -p /vectorstore/ich_db

# アプリケーションコードをコピー
COPY app/ .

EXPOSE 8501