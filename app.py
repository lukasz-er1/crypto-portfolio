from flask import render_template
import json
from config import app
from utils import update_prices


@app.route('/', methods=['GET'])
def main():
    with open('portfolio.json', 'r', encoding='utf-8') as portf:
        portfolio = json.load(portf)
    return render_template('index.html', portfolio=portfolio)


@app.route('/update', methods=['GET'])
def update():
    portfolio = update_prices()
    return render_template('index.html', portfolio=portfolio)


if __name__ == "__main__":
    app.run(host='192.168.0.30', port=5005, debug=True)
