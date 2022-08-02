
from balanced_backend.utils.values import extract_indexed_log


def test_extract_indexed_log():
    x = extract_indexed_log(
        '["FeePaid(str,int,str)","bnUSD","0x395ed40634fd7f2","origination"]',
        1,
    )
    assert x == "0x395ed40634fd7f2"
