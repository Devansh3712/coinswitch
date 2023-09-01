from coinswitch.schemas import Portfolio, Trades


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
