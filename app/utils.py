import requests
import json
from datetime import datetime
from app.config import BITBAY_API_URL, APP_DIR

ignored_items = ["TOTAL_USD", "TOTAL_PLN", "UPDATE_DATE", "SUM", "SUM_short", "XXX"]


def get_usd_price_from_coingecko(symbol):
    with open(f"{APP_DIR}/coingecko_id_list.json", "r", encoding="utf-8") as coingecko_id_list:
        coin_list = json.load(coingecko_id_list)
    r = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coin_list[symbol.lower()]}&vs_currencies=usd", verify=True)
    resp = r.json()

    return resp[coin_list[symbol.lower()]]["usd"]


def update_symbols_id_list_from_coingecko():
    r = requests.get("https://api.coingecko.com/api/v3/coins/list", verify=True)
    coins_list = r.json()
    coins = {}
    for counter, _ in enumerate(coins_list):
        try:
            coins[coins_list[counter]["symbol"]] = coins_list[counter]["id"]
        except:
            continue
    with open(f"{APP_DIR}/coingecko_id_list.json", "w") as f:
        json.dump(coins, f)
    print("Coin list updated from coingecko.")
    


def get_usdt_price(symbol):
    if symbol == "PLN":
        r = requests.get(f"{BITBAY_API_URL}/trading/transactions/USDT-PLN", verify=True)
    else:
        r = requests.get(f"{BITBAY_API_URL}/trading/transactions/{symbol}-USDT", verify=True)
    resp = r.json()
    try:
        price = float(resp["items"][0]["r"])
    except:
        price = get_usd_price_from_coingecko(symbol)

    return price


def update_prices():
    with open(f"{APP_DIR}/coin_list.json", "r", encoding="utf-8") as coin_list:
        portfolio = json.load(coin_list)
    portfolio["TOTAL_USD"] = 0
    for wallet in portfolio:
        if "TOTAL" not in wallet and "XXX" not in wallet:
            portfolio[wallet]["SUM"] = 0
            for item in portfolio[wallet]:
                if "SUM" not in item:
                    price = get_usdt_price(f"{item}")
                    if price > 500:
                        portfolio[wallet][item]["price"] = int(price)
                    elif price > 50:
                        portfolio[wallet][item]["price"] = f"{price:.1f}"
                    elif price > 1:
                        portfolio[wallet][item]["price"] = f"{price:.2f}"
                    elif price > 0.01:
                        portfolio[wallet][item]["price"] = f"{price:.4f}"
                    else:
                        portfolio[wallet][item]["price"] = f"{price:.8f}"
                    value = portfolio[wallet][item]['qty'] * price
                    portfolio[wallet]["SUM"] += value
                    portfolio[wallet][item]["value"] = int(value)
            portfolio[wallet]["SUM_short"] = int(portfolio[wallet]['SUM'])
            portfolio["TOTAL_USD"] += int(portfolio[wallet]["SUM"])
    date = datetime.now()
    portfolio["UPDATE_DATE"] = str(date)[5:16]
    usd_pln_rate = get_usdt_price("PLN")
    portfolio["TOTAL_PLN"] = portfolio["TOTAL_USD"] * usd_pln_rate
    portfolio["XXX"]["ZYSK"] = portfolio["TOTAL_PLN"] - portfolio["XXX"]["PLN"]
    portfolio["XXX"]["PROCENT"] = (portfolio["XXX"]["ZYSK"] / portfolio["XXX"]["PLN"]) * 100
    with open(f"{APP_DIR}/portfolio.json", "w") as f:
        json.dump(portfolio, f)

    return portfolio


def make_summary(portfolio):
    results = {}
    total = 0
    for wallet in portfolio:
        if wallet not in ignored_items:
            for coin in portfolio[wallet]:
                if coin not in ignored_items:
                    total += portfolio[wallet][coin]["value"]
                    if coin in results:
                        results[coin]["value"] += portfolio[wallet][coin]["value"]
                    else:
                        results[coin] = {}
                        results[coin]["value"] = portfolio[wallet][coin]["value"]
    for item in results:
        results[item]["perc"] = (results[item]["value"] / total) * 100

    return results
