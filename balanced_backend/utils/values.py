from typing import List
import ast


def convert_hex_int(hex_string: str) -> int:
    return int(hex_string, 16)


def extract_indexed_log(indexed_log: str, position: int):
    log_list = ast.literal_eval(indexed_log)
    return log_list[position + 1]


def get_total_indexed(
        events: List[dict],
        indexed_position: int,
        decimals: float = 1e18
) -> float:
    fees = 0
    for i in events:
        value = extract_indexed_log(i['indexed'], indexed_position)
        fee = convert_hex_int(value) / decimals
        fees += fee

    return fees
