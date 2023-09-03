from ..base import CoinSwitch, platform
from ..schemas import Ticker as TickerSchema

class Ticker(CoinSwitch):
    def all_pairs(self, exchange: platform) -> TickerSchema: ...
