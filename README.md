# stock_monitor

A small Python service that polls a stock API and exposes current prices as Prometheus metrics. The API it's polling is in another github project under stock_checker.

Features
- Polls symbols specified by `STOCK_LIST` in `config.py`.
- Uses `STOCK_API_ENDPOINT` to fetch per-symbol prices and exposes them on a Prometheus metrics endpoint.

Quickstart

1. Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Configure environment variables (optional):

```bash
export PROMETHEUS_PORT=9090
export STOCK_LIST="AAPL,MSFT,NVDA"
export STOCK_API_ENDPOINT="http://localhost:5001/api/stock/"
```

3. Run the monitor:

```bash
python3 stock_monitor.py
```

4. Check metrics:

```bash
curl http://localhost:9090/metrics
```

CI

This project includes a GitHub Actions workflow that runs a simple syntax check and tests on pushes and pull requests.

Contributing

Contributions welcome — please open an issue or PR.

Docker
------

Build and run the service with Docker:

```bash
docker build -t stock_monitor:latest .
docker run -d --name stock-monitor -p 9090:9090 \
	-e STOCK_API_ENDPOINT="http://host.docker.internal:5001/api/stock/" \
	-e STOCK_LIST="AAPL,AVGO,GOOGL,MSFT,NVDA" \
	stock_monitor:latest
```

Or use Docker Compose (recommended for local development on macOS):

```bash
docker-compose up -d --build
```

Check metrics:

```bash
curl http://localhost:9090/metrics
```
