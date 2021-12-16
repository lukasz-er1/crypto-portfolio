from flask import render_template
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)).rstrip("app"))
from app.config import app, APP_DIR
from app.utils import update_prices, make_summary, update_symbols_id_list_from_coingecko


@app.route("/", methods=["GET"])
def main():
    with open(os.path.join(APP_DIR, "portfolio.json"), "r", encoding="utf-8") as portf:
        portfolio = json.load(portf)
    return render_template("index.html", portfolio=portfolio)


@app.route("/update/", methods=["GET"])
def update():
    portfolio = update_prices()
    return render_template("index.html", portfolio=portfolio)


@app.route("/summary/", methods=["GET"])
def summary():
    with open(os.path.join(APP_DIR, "portfolio.json"), "r", encoding="utf-8") as portf:
        portfolio = json.load(portf)
    summary = make_summary(portfolio)
    return render_template("summary.html", portfolio=portfolio, summary=summary)


if __name__ == "__main__":
    update_symbols_id_list_from_coingecko()
    # app.run(host="127.0.0.1", port=5000, debug=True)
    app.run(host="192.168.0.30", port=80, debug=True)
