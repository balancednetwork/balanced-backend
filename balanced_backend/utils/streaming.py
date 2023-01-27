from balanced_backend.proto.block_pb2 import Log


def extract_method_from_log(log: Log):
    return log[0].split("(")[0]

