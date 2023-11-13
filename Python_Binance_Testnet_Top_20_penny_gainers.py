import ccxt
from prettytable import PrettyTable

# Set the API key and secret key as environment variables
import os
api_key = os.environ.get('KEY')
api_secret = os.environ.get('SECRET')

# Create a Binance exchange object with the testnet option
exchange = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
    'options': {
        'defaultType': 'spot', # use the spot API
        'adjustForTimeDifference': True, # sync the timestamp with the server
        'testnet': True # use the testnet endpoint
    }
})

# Fetch the tickers for all the symbols
tickers = exchange.fetch_tickers()

# Filter the tickers to include only those containing "USDT" in the symbol, have a price less than 0.01 USDT, and have a percentage gain greater than 1%
usdt_tickers = [ticker for ticker in tickers.values() if "USDT" in ticker['symbol'] and ticker['last'] is not None and ticker['last'] < 0.01  and ticker['percentage'] > 1]

# Sort the tickers by the percentage change in the last 24 hours
sorted_tickers = sorted(usdt_tickers, key=lambda x: x['percentage'], reverse=True)

# Print the top penny gainers
table = PrettyTable()
table.field_names = ["Symbol", "Price", "Percentage Change"]

for ticker in sorted_tickers:
    table.add_row([ticker['symbol'], ticker['last'], ticker['percentage']])

print(table)
