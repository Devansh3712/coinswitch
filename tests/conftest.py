import os

import pytest
from dotenv import load_dotenv

from coinswitch.base import CoinSwitch
from coinswitch.ticker import Ticker

load_dotenv()
API_KEY = os.environ["COINSWITCH_API_KEY"]
API_SECRET_KEY = os.environ["COINSWITCH_API_SECRET_KEY"]


@pytest.fixture()
def coinswitch_object() -> CoinSwitch:
    return CoinSwitch(API_KEY, API_SECRET_KEY)


@pytest.fixture()
def ticker_object() -> Ticker:
    return Ticker(API_KEY, API_SECRET_KEY)
