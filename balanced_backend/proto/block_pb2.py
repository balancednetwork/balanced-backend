# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: block.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0b\x62lock.proto\"\xc0\x01\n\x05\x42lock\x12\x0e\n\x06number\x18\x01 \x01(\x03\x12\x0c\n\x04hash\x18\x02 \x01(\t\x12\x13\n\x0bparent_hash\x18\x03 \x01(\t\x12\x18\n\x10merkle_root_hash\x18\x04 \x01(\t\x12\x0f\n\x07peer_id\x18\x05 \x01(\t\x12\x11\n\tsignature\x18\x06 \x01(\t\x12\x11\n\ttimestamp\x18\x07 \x01(\x03\x12\x0f\n\x07version\x18\x08 \x01(\t\x12\"\n\x0ctransactions\x18\t \x03(\x0b\x32\x0c.Transaction\"\x8b\x03\n\x0bTransaction\x12\x0c\n\x04hash\x18\x01 \x01(\t\x12\x11\n\ttimestamp\x18\x02 \x01(\x03\x12\x19\n\x11transaction_index\x18\x03 \x01(\x03\x12\r\n\x05nonce\x18\x04 \x01(\t\x12\x0b\n\x03nid\x18\x05 \x01(\t\x12\x14\n\x0c\x66rom_address\x18\x06 \x01(\t\x12\x12\n\nto_address\x18\x07 \x01(\t\x12\r\n\x05value\x18\x08 \x01(\t\x12\x0e\n\x06status\x18\t \x01(\t\x12\x12\n\nstep_price\x18\n \x01(\t\x12\x11\n\tstep_used\x18\x0b \x01(\t\x12\x12\n\nstep_limit\x18\x0c \x01(\t\x12\x1c\n\x14\x63umulative_step_used\x18\r \x01(\t\x12\x12\n\nlogs_bloom\x18\x0e \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x0f \x01(\t\x12\x11\n\tdata_type\x18\x10 \x01(\t\x12\x15\n\rscore_address\x18\x11 \x01(\t\x12\x11\n\tsignature\x18\x12 \x01(\t\x12\x0f\n\x07version\x18\x13 \x01(\t\x12\x12\n\x04logs\x18\x14 \x03(\x0b\x32\x04.Log\"5\n\x03Log\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x01(\t\x12\x0f\n\x07indexed\x18\x02 \x03(\t\x12\x0c\n\x04\x64\x61ta\x18\x03 \x03(\tb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'block_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _BLOCK._serialized_start=16
  _BLOCK._serialized_end=208
  _TRANSACTION._serialized_start=211
  _TRANSACTION._serialized_end=606
  _LOG._serialized_start=608
  _LOG._serialized_end=661
# @@protoc_insertion_point(module_scope)