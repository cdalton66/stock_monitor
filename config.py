import os

PROMETHEUS_PORT = int(os.getenv('PROMETHEUS_PORT', 9090))
STOCK_LIST = os.getenv('STOCK_LIST', 'AAPL,AVGO,GOOGL,MSFT,NVDA').split(',')
STOCK_API_ENDPOINT = os.getenv('STOCK_API_ENDPOINT', 'http://localhost:5001/api/stock/')
MAX_API_CALLS_PER_DAY = int(os.getenv('MAX_API_CALLS_PER_DAY', 25))