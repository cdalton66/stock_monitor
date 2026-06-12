import time
import logging
import requests

from prometheus_client import start_http_server, Gauge
import config

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# single gauge with a symbol label to avoid creating many metrics dynamically
stock_gauge = Gauge('stock_price', 'Current stock price for a symbol', ['symbol'])

# normalize config values
STOCK_API_ENDPOINT = config.STOCK_API_ENDPOINT.rstrip('/') + '/'
STOCKS = [s.strip() for s in config.STOCK_LIST if s and str(s).strip()]


def _fetch_price(symbol):
	symbol = str(symbol).strip()
	if not symbol:
		return None
	url = STOCK_API_ENDPOINT + symbol
	logging.debug('Fetching stock price from URL: %s', url)
	headers = {
		'Accept': 'application/json',
		'User-Agent': 'curl/7.86.0',
		'Connection': 'close',
	}
	try:
		resp = requests.get(url, timeout=5, headers=headers)
	except Exception:
		logging.exception('request failed for %s at %s', symbol, url)
		return None

	if resp.status_code != 200:
		logging.warning('Non-200 response for %s: %s %s', symbol, resp.status_code, resp.text.strip()[:200])
		return None

	# Try JSON first
	try:
		j = resp.json()
	except ValueError:
		j = None

	if isinstance(j, (int, float)):
		return float(j)
	if isinstance(j, dict):
		for key in ('price', 'current', 'last', 'value'):
			if key in j:
				try:
					return float(j[key])
				except Exception:
					pass
		# try first numeric value in dict
		for v in j.values():
			try:
				return float(v)
			except Exception:
				continue
	if isinstance(j, list) and j:
		first = j[0]
		if isinstance(first, (int, float)):
			return float(first)
		if isinstance(first, dict):
			for key in ('price', 'current', 'last', 'value'):
				if key in first:
					try:
						return float(first[key])
					except Exception:
						pass

	# fallback: try to parse plain text
	text = resp.text.strip()
	try:
		return float(text)
	except Exception:
		logging.warning('Could not parse price for %s (response length %d)', symbol, len(text))
		return None

def poll_loop(poll_interval=30):
	while True:
		for symbol in STOCKS:
			price = _fetch_price(symbol)
			if price is not None:
				stock_gauge.labels(symbol=symbol).set(price)
				logging.info('Updated %s = %s', symbol, price)
			else:
				logging.debug('No price for %s this cycle', symbol)
		time.sleep(poll_interval)

def main():
	POLL_INTERVAL = round(24 / (config.MAX_API_CALLS_PER_DAY / len(STOCKS))) * 3600  # seconds between calls to stay within daily limit
	start_http_server(config.PROMETHEUS_PORT)
	logging.info('Prometheus metrics server started on port %s', config.PROMETHEUS_PORT)
	poll_loop(POLL_INTERVAL)

if __name__ == '__main__':
	main()
