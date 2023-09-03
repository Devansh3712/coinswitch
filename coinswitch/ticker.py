import httpx

from .base import CoinSwitch, platform
from .constants import *
from .schemas import Ticker as TickerSchema


class Ticker(CoinSwitch):
    def all_pairs(self, exchange: platform) -> TickerSchema:
        """Get the 24 hour ticker for all coins.

        Args:
            exchange (platform): Exchange platform, can have value "coinswitchx" or
                                 "wazirx".

        Raises:
            httpx.RequestError: Unable to fetch the tickers.

        Returns:
            TickerSchema: Ticker of all coins in the past 24 hours.
        """
        endpoint = "/trade/api/v2/24hr/all-pairs/ticker"
        params = {"exchange": exchange}
        self._set_signature_header(GET, endpoint, params=params)
        response = httpx.get(BASE_URL + endpoint, headers=self.headers, params=params)
        if response.status_code != 200:
            raise httpx.RequestError("Unable to fetch the tickers")
        response_json = response.json()
        return TickerSchema(**response_json)
