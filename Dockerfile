FROM python:3.10
LABEL authors="Gabriel-Almeida-ECAT"

WORKDIR /usr/src/app
COPY requirements.txt .
RUN pt-get update && \
    apt-get install -y python3-tk libmagickwand-dev && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -r requirements.txt
COPY . .
ENTRYPOINT ["python3", "main.py"]
