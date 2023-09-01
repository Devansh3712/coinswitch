from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class Currency(BaseModel):
    currency: str
    blocked_balance_deposit: float
    blocked_balance_withdraw: float
    blocked_balance_order: float
    main_balance: float
    blocked_balance_stake: float
    blocked_balance_vault: float
    buy_average_price: float
    invested_value: float
    invested_value_excluding_fee: float
    current_value: float
    sell_rate: float
    buy_rate: float
    is_average_price_available: Optional[bool] = None
    name: str
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
