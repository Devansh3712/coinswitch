from datetime import datetime
from typing import Dict, List, Optional, Union

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, field_validator


class Currency(BaseModel):
    currency: str
    name: str
    main_balance: float
    blocked_balance_deposit: float
    blocked_balance_withdraw: float
    blocked_balance_order: float
    blocked_balance_stake: float
    blocked_balance_vault: float
    buy_average_price: float
    invested_value: float
    invested_value_excluding_fee: float
    current_value: float
    sell_rate: float
    buy_rate: float
    is_average_price_available: Optional[bool] = None
    is_delisted_coin: Optional[bool] = None


class Portfolio(BaseModel):
    data: List[Currency]


class Trade(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    event_time: datetime = Field(alias="E")
    side: str = Field(alias="S")
    buyer_order_id: str = Field(alias="a")
    seller_order_id: str = Field(alias="b")
    is_buyer_maker: bool = Field(alias="m")
    price: float = Field(alias="p")
    quantity: float = Field(alias="q")
    symbol: str = Field(alias="s")
    trade_id: str = Field(alias="t")
    exchange: str = Field(alias="e")


class Trades(BaseModel):
    data: List[Trade]


class ExchangePrecisionData(BaseModel):
    base: int
    quote: int
    limit: int


class ExchangePrecision(BaseModel):
    coins: Dict[str, ExchangePrecisionData] = Field(
        validation_alias=AliasChoices("coinswitchx", "wazirx")
    )


class OrderBook(BaseModel):
    timestamp: datetime
    bids: List[List[float]]
    asks: List[List[float]]
    symbol: str


class CandleData(BaseModel):
    start_time: datetime
    close_time: datetime
    symbol: str
    open: float = Field(alias="o")
    high: float = Field(alias="h")
    low: float = Field(alias="l")
    close: float = Field(alias="c")
    interval: int
    volume: float


class Candles(BaseModel):
    data: List[CandleData]


class TickerData(BaseModel):
    symbol: str
    base_asset: str = Field(alias="baseAsset")
    quote_asset: str = Field(alias="quoteAsset")
    open_price: float = Field(alias="openPrice")
    low_price: float = Field(alias="lowPrice")
    high_price: float = Field(alias="highPrice")
    last_price: float = Field(alias="lastPrice")
    base_volume: float = Field(alias="baseVolume")
    quoute_volume: float = Field(alias="quoteVolume")
    percentage_change: float = Field(alias="percentageChange")
    bid: Optional[float] = Field(None, alias="bidPrice")
    ask: Optional[float] = Field(None, alias="askPrice")
    at: datetime

    @field_validator("bid", "ask", mode="before")
    @classmethod
    def empty_to_None(cls, value: str) -> Union[float, None]:
        if value == "":
            return None
        return float(value)


class Ticker(BaseModel):
    data: Dict[str, TickerData]
