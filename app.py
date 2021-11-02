from flask import render_template
import json
from config import app
from utils import update_prices, make_summary, update_symbols_id_list_from_coingecko


@app.route('/', methods=['GET'])
def main():
    with open('portfolio.json', 'r', encoding='utf-8') as portf:
        portfolio = json.load(portf)
    return render_template('index.html', portfolio=portfolio)


@app.route('/update/', methods=['GET'])
def update():
    portfolio = update_prices()
    return render_template('index.html', portfolio=portfolio)


@app.route('/summary/', methods=['GET'])
def summary():
    with open('portfolio.json', 'r', encoding='utf-8') as portf:
        portfolio = json.load(portf)
    summary = make_summary(portfolio)
    return render_template('summary.html', portfolio=portfolio, summary=summary)


if __name__ == "__main__":
    update_symbols_id_list_from_coingecko()
    app.run(host='192.168.0.30', port=5005, debug=True)
