import os

import pytest
from dotenv import load_dotenv

from coinswitch.base import CoinSwitch


@pytest.fixture()
def coinswitch_object():
    load_dotenv()
    api_key = os.environ["COINSWITCH_API_KEY"]
    api_secret_key = os.environ["COINSWITCH_API_SECRET_KEY"]
    return CoinSwitch(api_key, api_secret_key)
