import json
from typing import Any, Dict
from urllib.parse import unquote_plus, urlencode, urlparse

import httpx
from cryptography.hazmat.primitives.asymmetric import ed25519

from .constants import *


class CoinSwitch:
    def __init__(self, api_key: str, api_secret_key: str) -> None:
        self.api_key = api_key
        self.api_secret_key = api_secret_key
        self.headers: Dict[str, str] = {
            "Content-Type": "application/json",
            "X-AUTH-APIKEY": self.api_key,
        }

    def __set_signature_header(
        self,
        method: str,
        endpoint: str,
        payload: Dict[str, Any] = {},
        params: Dict[str, Any] = {},
    ) -> None:
        """
        To access CoinSwitch APIs we need to generate a signature and pass it as a
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
        """
        Check if our ecosystem has been successfully connected to the CoinSwitch
        ecosystem.

        Returns:
            bool: True if connected else False.
        """
        endpoint = "/trade/api/v2/ping"
        self.__set_signature_header(GET, endpoint)
        response = httpx.get(BASE_URL + endpoint, headers=self.headers)
        if response.status_code == 200:
            return True
        return False

    def validate_keys(self) -> bool:
        """
        Validate CoinSwitch API keys.

        Returns:
            bool: True if keys are valid else False.
        """
        endpoint = "/trade/api/v2/validate/keys"
        self.__set_signature_header(GET, endpoint)
        response = httpx.get(BASE_URL + endpoint, headers=self.headers)
        if response.status_code == 200:
            return True
        return False