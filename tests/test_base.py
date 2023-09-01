from coinswitch.schemas import Portfolio


def test_ping(coinswitch_object) -> None:
    result: bool = coinswitch_object.ping()
    assert result == True


def test_validate_keys(coinswitch_object) -> None:
    result: bool = coinswitch_object.validate_keys()
    assert result == True


def test_portfolio(coinswitch_object) -> None:
    result: Portfolio = coinswitch_object.portfolio()
    assert len(result.data) == 6
