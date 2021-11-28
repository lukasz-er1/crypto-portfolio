import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)).rstrip("\\tests"))
from app.utils import get_usd_price_from_coingecko


def test_get_usd_price_from_coingecko_for_btc():
    """ Check if coingecko is returning proper value for 'BTC'. """
    btc_price = get_usd_price_from_coingecko('BTC')
    assert btc_price > 100
    assert isinstance(btc_price, int)

def test_get_usd_price_from_coingecko_for_usdt():
    """ Check if coingecko is returning proper value for 'USDT'. """
    usdt_price = get_usd_price_from_coingecko('USDT')
    assert 1.05 > usdt_price > 0.95
    assert isinstance(usdt_price, float)
