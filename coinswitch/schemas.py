from typing import List, Optional

from pydantic import BaseModel


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
