# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: model.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0bmodel.proto\x12\x05model\"\x14\n\x04Text\x12\x0c\n\x04text\x18\x01 \x01(\t\"[\n\x04Note\x12\x0e\n\x06sender\x18\x01 \x01(\x03\x12\x11\n\trecipient\x18\x02 \x01(\x03\x12\x1a\n\x12logical_clock_time\x18\x03 \x01(\x03\x12\x14\n\x0clength_queue\x18\x04 \x01(\x03\x32o\n\x04\x43hat\x12\x34\n\x16\x63lient_receive_message\x12\x0b.model.Text\x1a\x0b.model.Note\"\x00\x12\x31\n\x13\x63lient_send_message\x12\x0b.model.Note\x1a\x0b.model.Text\"\x00\x42\x36\n\x1bio.grpc.examples.routeguideB\x0fRouteGuideProtoP\x01\xa2\x02\x03RTGb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'model_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\033io.grpc.examples.routeguideB\017RouteGuideProtoP\001\242\002\003RTG'
  _TEXT._serialized_start=22
  _TEXT._serialized_end=42
  _NOTE._serialized_start=44
  _NOTE._serialized_end=135
  _CHAT._serialized_start=137
  _CHAT._serialized_end=248
# @@protoc_insertion_point(module_scope)
