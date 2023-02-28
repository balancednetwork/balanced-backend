# import pytest
# import json
# from google.protobuf.json_format import Parse, ParseDict
#
# # from balanced_backend.streaming.contracts.dex import transform_dex_swap_log
# from balanced_backend.proto.block_pb2 import Block  # noqa
#
# DEX_SWAPS = [
#     'dex-swap-39211113.json',
# ]
#
# @pytest.mark.parametrize("fixture", DEX_SWAPS)
# def test_transform_dex_swap_log(get_fixture, fixture):
#     with open(get_fixture(fixture)) as f:
#         fixture = json.load(f)
#
#     block = ParseDict(fixture, Block())
#     # transform_dex_swap_log(block=block, tx_index=1, log_index=3)
#     print()
#
