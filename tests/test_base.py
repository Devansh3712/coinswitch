def test_ping(coinswitch_object):
    result = coinswitch_object.ping()
    assert result == True


def test_validate_keys(coinswitch_object):
    result = coinswitch_object.validate_keys()
    assert result == True
