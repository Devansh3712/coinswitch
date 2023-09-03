from coinswitch.schemas import Ticker


def test_all_pairs_coinswitch(ticker_object) -> None:
    result: Ticker = ticker_object.all_pairs("coinswitchx")
    assert len(result.data) == 116


def test_all_pairs_wazirx(ticker_object) -> None:
    result: Ticker = ticker_object.all_pairs("wazirx")
    assert len(result.data) == 36


def test_specific_coin(ticker_object) -> None:
    result: Ticker = ticker_object.specific_coin("coinswitchx", "btc/inr")
    assert len(result.data) == 1
