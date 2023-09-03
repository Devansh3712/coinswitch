import json
from typing import Any, Dict, Literal, Optional
from urllib.parse import unquote_plus, urlencode, urlparse

import httpx
from cryptography.hazmat.primitives.asymmetric import ed25519

from .constants import *
from .schemas import Candles, ExchangePrecision, OrderBook, Portfolio, Trades

platform = Literal["coinswitchx", "wazirx"]


class CoinSwitch:
    def __init__(self, api_key: str, api_secret_key: str) -> None:
        self.api_key = api_key
        self.api_secret_key = api_secret_key
        self.headers: Dict[str, str] = {
            "Content-Type": "application/json",
            "X-AUTH-APIKEY": self.api_key,
        }

    def _set_signature_header(
        self,
        method: str,
        endpoint: str,
        payload: Dict[str, Any] = {},
        params: Dict[str, Any] = {},
    ) -> None:
        """To access CoinSwitch APIs we need to generate a signature and pass it as a
        header in every API call.

        Args:
            method (str): Request HTTP method.
            endpoint (str): API endpoint to be called.
            payload (Dict[str, Any], optional): Request JSON body. Defaults to {}.
            params (Dict[str, Any], optional): Reqeust query params. Defaults to {}.
        """
        unqoute_endpoint = endpoint
        if method == GET and len(params) != 0:
            endpoint += ("&", "?")[urlparse(endpoint).query == ""] + urlencode(params)
            unqoute_endpoint = unquote_plus(endpoint)

        signature_message = (
            method
            + unqoute_endpoint
            + json.dumps(payload, separators=(",", ":"), sort_keys=True)
        )
        request_string = bytes(signature_message, "utf-8")
        secret_key_bytes = bytes.fromhex(self.api_secret_key)
        secret_key = ed25519.Ed25519PrivateKey.from_private_bytes(secret_key_bytes)
        signature_bytes = secret_key.sign(request_string)

        self.headers["X-AUTH-SIGNATURE"] = signature_bytes.hex()

    def ping(self) -> bool:
        """Check if our ecosystem has been successfully connected to the CoinSwitch
        ecosystem.

        Returns:
            bool: True if connected else False.
        """
        endpoint = "/trade/api/v2/ping"
        self._set_signature_header(GET, endpoint)
        response = httpx.get(BASE_URL + endpoint, headers=self.headers)
        if response.status_code == 200:
            return True
        return False

    def validate_keys(self) -> bool:
        """Validate CoinSwitch API keys.

        Returns:
            bool: True if keys are valid else False.
        """
        endpoint = "/trade/api/v2/validate/keys"
        self._set_signature_header(GET, endpoint)
        response = httpx.get(BASE_URL + endpoint, headers=self.headers)
        if response.status_code == 200:
            return True
        return False

    def portfolio(self) -> Portfolio:
        """Check the user's portfolio.

        Raises:
            httpx.RequestError: Unable to fetch the portfolio.

        Returns:
            Portfolio: List of cryptocurrencies owned by the user.
        """
        endpoint = "/trade/api/v2/user/portfolio"
        self._set_signature_header(GET, endpoint)
        response = httpx.get(BASE_URL + endpoint, headers=self.headers)
        if response.status_code != 200:
            raise httpx.RequestError("Unable to fetch the portfolio")
        response_json = response.json()
        return Portfolio(**response_json)

    def trades(self, exchange: platform, symbol: str) -> Trades:
        """Get history of all of user's trades.

        Args:
            exchange (platform): Exchange platform, can have value "coinswitchx" or
                                 "wazirx".
            symbol (str): Cryptocurrency symbol (case insensitive).

        Raises:
            httpx.RequestError: Unable to fetch the trade history.

        Returns:
            Trade: List of trades made by a user.
        """
        endpoint = "/trade/api/v2/trades"
        params = {"exchange": exchange, "symbol": symbol}
        self._set_signature_header(GET, endpoint, params=params)
        response = httpx.get(BASE_URL + endpoint, headers=self.headers, params=params)
        if response.status_code != 200:
            raise httpx.RequestError("Unable to fetch the trade history")
        response_json = response.json()
        return Trades(**response_json)

    def exchange_precision(
        self, exchange: platform, symbol: Optional[str] = None
    ) -> ExchangePrecision:
        """Check precision coin and exchange wise.

        Args:
            exchange (platform): Exchange platform, can have value "coinswitchx" or
                                 "wazirx".
            symbol (Optional[str], optional): Cryptocurrency symbol (case insensitive).
                                              Defaults to None.

        Raises:
            httpx.RequestError: Unable to fetch the coin exchange precision.

        Returns:
            ExchangePrecision: Base, limit and quote values for the given coin symbols.
        """
        endpoint = "/trade/api/v2/exchangePrecision"
        payload: Dict[str, Any] = {"exchange": exchange}
        if symbol:
            payload["symbol"] = symbol
        self._set_signature_header(POST, endpoint, payload)
        response = httpx.post(BASE_URL + endpoint, headers=self.headers, json=payload)
        if response.status_code != 200:
            raise httpx.RequestError("Unable to fetch the coin exchange precision")
        response_json = response.json()["data"]
        return ExchangePrecision(**response_json)

    def depth(self, exchange: platform, symbol: str) -> OrderBook:
        """Check the orderbook for a coin.

        Args:
            exchange (platform): Exchange platform, can have value "coinswitchx" or
                                 "wazirx".
            symbol (str): Cryptocurrency symbol (case insensitive).

        Raises:
            httpx.RequestError: Unable to fetch the orderbook.

        Returns:
            OrderBook: List of asks and bids for a coin.
        """
        endpoint = "/trade/api/v2/depth"
        params = {"exchange": exchange, "symbol": symbol}
        self._set_signature_header(GET, endpoint, params=params)
        response = httpx.get(BASE_URL + endpoint, headers=self.headers, params=params)
        if response.status_code != 200:
            raise httpx.RequestError("Unable to fetch the orderbook")
        response_json = response.json()["data"]
        return OrderBook(**response_json)

    def candles(
        self,
        exchange: platform,
        symbol: str,
        interval: int,
        start_time: int,
        end_time: int,
    ) -> Candles:
        """Get candlestick data of an interval.

        Args:
            exchange (platform): Exchange platform, can have value "coinswitchx" or
                                 "wazirx".
            symbol (str): Cryptocurrency symbol (case insensitive).
            interval (int): Duration of candlestick in minutes.
            start_time (int): Timestamp in milliseconds (Unix epoch).
            end_time (int): Timestamp in milliseconds (Unix epoch).

        Raises:
            httpx.RequestError: Unable to fetch the candlesticks.

        Returns:
            Candles: List of candlesticks for the given interval.
        """
        endpoint = "/trade/api/v2/candles"
        params: Dict[str, Any] = {
            "end_time": end_time,
            "start_time": start_time,
            "symbol": symbol,
            "interval": interval,
            "exchange": exchange,
        }
        self._set_signature_header(GET, endpoint, params=params)
        response = httpx.get(BASE_URL + endpoint, headers=self.headers, params=params)
        response_json = response.json()
        if response.status_code != 200:
            raise httpx.RequestError("Unable to fetch the candlesticks")
        return Candles(**response_json)
