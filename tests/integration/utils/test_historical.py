from balanced_backend.utils.methods import get_value_from_timestamp


def test_get_value_from_timestamp(loans_historical_context):
    value = get_value_from_timestamp(context=loans_historical_context)

    assert int(round(value, 0)) == 76739382
