import requests
import json
from datetime import datetime
from config import BITBAY_API_URL


def get_usdt_price(symbol):
    if symbol == "PLN":
        r = requests.get(f"{BITBAY_API_URL}/trading/transactions/USDT-PLN", verify=True)
    else:
        r = requests.get(f"{BITBAY_API_URL}/trading/transactions/{symbol}-USDT", verify=True)
    resp = r.json()
    try:
        price = float(resp['items'][0]['r'])
    except:
        price = 1.00001
    return price


def update_prices():
    with open('coin_list.json', 'r', encoding='utf-8') as coin_list:
        portfolio = json.load(coin_list)
    portfolio["TOTAL_USD"] = 0
    for wallet in portfolio:
        if "TOTAL" not in wallet:
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
                    else:
                        portfolio[wallet][item]["price"] = f"{price:.4f}"
                    value = portfolio[wallet][item]['qty'] * price
                    portfolio[wallet]["SUM"] += value
                    portfolio[wallet][item]["value"] = int(value)
            portfolio[wallet]["SUM_short"] = int(portfolio[wallet]['SUM'])
            portfolio["TOTAL_USD"] += int(portfolio[wallet]["SUM"])
    date = datetime.now()
    portfolio["UPDATE_DATE"] = str(date)[5:16]
    usd_pln_rate = get_usdt_price("PLN")
    portfolio["TOTAL_PLN"] = portfolio["TOTAL_USD"] * usd_pln_rate
    with open("portfolio.json", "w") as f:
        json.dump(portfolio, f)
    return portfolio
