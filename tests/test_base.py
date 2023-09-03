from coinswitch.schemas import ExchangePrecision, OrderBook, Portfolio, Trades


def test_ping(coinswitch_object) -> None:
    result: bool = coinswitch_object.ping()
    assert result == True


def test_validate_keys(coinswitch_object) -> None:
    result: bool = coinswitch_object.validate_keys()
    assert result == True


def test_portfolio(coinswitch_object) -> None:
    result: Portfolio = coinswitch_object.portfolio()
    assert len(result.data) == 6


def test_trades(coinswitch_object) -> None:
    result: Trades = coinswitch_object.trades("coinswitchx", "btc/inr")
    assert len(result.data) == 10


def test_exchange_precision(coinswitch_object) -> None:
    result: ExchangePrecision = coinswitch_object.exchange_precision(
        "coinswitchx", "btc/inr"
    )
    print(result.model_dump_json(indent=4))
    assert len(result.coins) == 1


def test_depth(coinswitch_object) -> None:
    result: OrderBook = coinswitch_object.depth("coinswitchx", "btc/inr")
    assert len(result.asks) == 100
    assert len(result.bids) == 100
