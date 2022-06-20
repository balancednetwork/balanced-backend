from balanced_backend.utils.historical import get_value_from_timestamp


def test_get_value_from_timestamp(loans_context):
    value = get_value_from_timestamp(context=loans_context)

    assert int(round(value, 0)) == 76739382
