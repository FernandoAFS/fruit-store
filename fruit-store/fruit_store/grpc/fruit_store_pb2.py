# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: fruit_store/grpc/fruit-store.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\"fruit_store/grpc/fruit-store.proto\x12\x0b\x66ruit_store\"\x07\n\x05\x45mpty\"H\n\tSaleEvent\x12\x0c\n\x04\x64\x61te\x18\x01 \x01(\x01\x12\x10\n\x08quantity\x18\x02 \x01(\r\x12\x0c\n\x04item\x18\x03 \x01(\t\x12\r\n\x05price\x18\x04 \x01(\r\"\x19\n\tSaleReply\x12\x0c\n\x04\x63ode\x18\x01 \x01(\x05\"K\n\rReportRequest\x12\x12\n\x05\x64\x61te0\x18\x01 \x01(\x01H\x00\x88\x01\x01\x12\x12\n\x05\x64\x61tef\x18\x02 \x01(\x01H\x01\x88\x01\x01\x42\x08\n\x06_date0B\x08\n\x06_datef\"\x8e\x01\n\x0eReportResponse\x12\x35\n\x05items\x18\x03 \x03(\x0b\x32&.fruit_store.ReportResponse.ItemsEntry\x1a\x45\n\nItemsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12&\n\x05value\x18\x02 \x01(\x0b\x32\x17.fruit_store.ReportItem:\x02\x38\x01\"\xd8\x01\n\nReportItem\x12\x15\n\rtotalQuantity\x18\x01 \x01(\r\x12\x16\n\x0e\x61veragePerSale\x18\x02 \x01(\r\x12\x14\n\x0ctotalRevenue\x18\x03 \x01(\r\x12\x35\n\x07monthly\x18\x04 \x03(\x0b\x32$.fruit_store.ReportItem.MonthlyEntry\x1aN\n\x0cMonthlyEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12-\n\x05value\x18\x02 \x01(\x0b\x32\x1e.fruit_store.ReportItemMonthly:\x02\x38\x01\"X\n\x11ReportItemMonthly\x12\x15\n\rtotalQuantity\x18\x01 \x01(\r\x12\x16\n\x0e\x61veragePerSale\x18\x02 \x01(\r\x12\x14\n\x0ctotalRevenue\x18\x03 \x01(\r2\xbc\x01\n\x06Server\x12\x35\n\x07PutSale\x12\x16.fruit_store.SaleEvent\x1a\x12.fruit_store.Empty\x12\x44\n\tGetReport\x12\x1a.fruit_store.ReportRequest\x1a\x1b.fruit_store.ReportResponse\x12\x35\n\x0bHealthcheck\x12\x12.fruit_store.Empty\x1a\x12.fruit_store.Emptyb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'fruit_store.grpc.fruit_store_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_REPORTRESPONSE_ITEMSENTRY']._options = None
  _globals['_REPORTRESPONSE_ITEMSENTRY']._serialized_options = b'8\001'
  _globals['_REPORTITEM_MONTHLYENTRY']._options = None
  _globals['_REPORTITEM_MONTHLYENTRY']._serialized_options = b'8\001'
  _globals['_EMPTY']._serialized_start=51
  _globals['_EMPTY']._serialized_end=58
  _globals['_SALEEVENT']._serialized_start=60
  _globals['_SALEEVENT']._serialized_end=132
  _globals['_SALEREPLY']._serialized_start=134
  _globals['_SALEREPLY']._serialized_end=159
  _globals['_REPORTREQUEST']._serialized_start=161
  _globals['_REPORTREQUEST']._serialized_end=236
  _globals['_REPORTRESPONSE']._serialized_start=239
  _globals['_REPORTRESPONSE']._serialized_end=381
  _globals['_REPORTRESPONSE_ITEMSENTRY']._serialized_start=312
  _globals['_REPORTRESPONSE_ITEMSENTRY']._serialized_end=381
  _globals['_REPORTITEM']._serialized_start=384
  _globals['_REPORTITEM']._serialized_end=600
  _globals['_REPORTITEM_MONTHLYENTRY']._serialized_start=522
  _globals['_REPORTITEM_MONTHLYENTRY']._serialized_end=600
  _globals['_REPORTITEMMONTHLY']._serialized_start=602
  _globals['_REPORTITEMMONTHLY']._serialized_end=690
  _globals['_SERVER']._serialized_start=693
  _globals['_SERVER']._serialized_end=881
# @@protoc_insertion_point(module_scope)
