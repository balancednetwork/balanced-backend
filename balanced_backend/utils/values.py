from typing import List, TYPE_CHECKING
import ast


if TYPE_CHECKING:
    from balanced_backend.models.volumes_base import VolumeIntervalBase

def convert_hex_int(hex_string: str) -> int:
    return int(hex_string, 16)


def extract_indexed_log(indexed_log: str, position: int):
    log_list = ast.literal_eval(indexed_log)
    try:
        return log_list[position + 1]
    except IndexError as e:
        raise Exception(str(e) + f"Index error at position={position} on indexed_log={indexed_log}")


def extract_non_indexed_log(data: str, position: int):
    log_list = ast.literal_eval(data)
    try:
        return log_list[position]
    except IndexError as e:
        raise Exception(str(e) + f"Index error at position={position} on indexed_log={data}")


def get_total_indexed(
        events: List[dict],
        indexed_position: int,
        decimals: float = 1e18
) -> float:
    fees = 0
    for i in events:
        value = extract_indexed_log(indexed_log=i['indexed'], position=indexed_position)
        fee = convert_hex_int(value) / decimals
        fees += fee

    return fees


def get_total_non_indexed(
        events: List[dict],
        non_indexed_position: int,
        decimals: float = 1e18
) -> float:
    fees = 0
    for i in events:
        value = extract_non_indexed_log(data=i['indexed'], position=non_indexed_position)
        fee = convert_hex_int(value) / decimals
        fees += fee

    return fees


def get_total_volume(events: List[dict], context: 'VolumeIntervalBase') -> float:
    if context.indexed_position is None:
        return get_total_non_indexed(
            events, context.non_indexed_position, context.decimals)
    return get_total_indexed(events, context.indexed_position, context.decimals)