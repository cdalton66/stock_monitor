FROM python:3.11-slim

WORKDIR /app

# Install system deps (if any) and pip packages
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . /app

ENV PROMETHEUS_PORT=9090
EXPOSE 9090

CMD ["python", "stock_monitor.py"]
