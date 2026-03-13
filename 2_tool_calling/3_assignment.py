import requests

# Mapping from ticker to CoinGecko coin IDs
TICKER_TO_ID = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "ADA": "cardano",
    "DOGE": "dogecoin",
    "XRP": "ripple"
}


def get_crypto_price(ticker: str):
    ticker = ticker.upper()

    if ticker not in TICKER_TO_ID:
        raise ValueError(f"Ticker {ticker} not supported in mapping")

    coin_id = TICKER_TO_ID[ticker]

    url = "https://api.coingecko.com/api/v3/simple/price"

    params = {
        "ids": coin_id,
        "vs_currencies": "usd"
    }

    response = requests.get(url, params=params)
    data = response.json()

    price = data[coin_id]["usd"]
    return price


ticker = input("Enter crypto ticker (e.g. BTC): ")

try:
    price = get_crypto_price(ticker)
    print(f"The current price of {ticker} is ${price}")
except Exception as e:
    print("Error:", e)