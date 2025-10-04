import re
import pytest
from balanced_backend.cron.token_stats import PROBLEM_ADDRESS_RE


@pytest.mark.parametrize(
    "address,expected",
    [
        ("cx0000000000000000000000000000000000000002", True),
        ("cx0000000000000000000000000000000000000011", True),
        ("cx0000000000000000000000000000000000000001", False),
        ("cx1234567890abcdef1234567890abcdef12345678", False),
        ("cx0000000000000000000000000000000000000000", False),
        ("cx0000000000000000000000000000000000000001", False),
        ("hx1234567890abcdef1234567890abcdef12345678", False),
    ],
)
def test_cron_problem_re(address, expected):
    assert bool(re.match(PROBLEM_ADDRESS_RE, address)) == expected
