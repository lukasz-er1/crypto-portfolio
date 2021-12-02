import pytest
import sys
import os
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)).rstrip("tests"))
from app.utils import get_usd_price_from_coingecko, update_symbols_id_list_from_coingecko
from app.config import APP_DIR


@pytest.fixture(scope="session", autouse=True)
def create_file_coingecko_id_list_json():
    update_symbols_id_list_from_coingecko()


def test_update_symbols_id_list_from_coingecko() -> None:
    """ Check if json file will be updated (modify time check) and if there are
        more than 5'000 ID's (currently there are over 9'000 coins) """
    coingecko_id_list_json = os.path.join(APP_DIR, "coingecko_id_list.json")
    file_before_update = os.stat(coingecko_id_list_json).st_mtime
    update_symbols_id_list_from_coingecko()
    file_after_update = os.stat(coingecko_id_list_json).st_mtime
    with open(coingecko_id_list_json, "r", encoding="utf-8") as id_list_json:
        coins = json.load(id_list_json)

    assert len(coins) > 5_000
    assert file_before_update != file_after_update


def test_get_usd_price_from_coingecko_for_btc() -> None:
    """ Check if coingecko is returning proper value for 'BTC'. """
    btc_price = get_usd_price_from_coingecko('BTC')

    assert btc_price > 100
    assert isinstance(btc_price, int)


def test_get_usd_price_from_coingecko_for_usdt() -> None:
    """ Check if coingecko is returning proper value for 'USDT'. """
    usdt_price = get_usd_price_from_coingecko('USDT')

    assert 1.05 > usdt_price > 0.95
    assert isinstance(usdt_price, float)
