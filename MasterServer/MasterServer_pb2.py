# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: MasterServer.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='MasterServer.proto',
  package='MasterServer',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x12MasterServer.proto\x12\x0cMasterServer\"\"\n\x05Reply\x12\x0b\n\x03msg\x18\x01 \x01(\t\x12\x0c\n\x04\x63ode\x18\x02 \x01(\x05\"Z\n\x05\x43hunk\x12\n\n\x02id\x18\x01 \x01(\t\x12\n\n\x02ip\x18\x02 \x01(\t\x12\x0c\n\x04port\x18\x03 \x01(\t\x12\x10\n\x08num_keys\x18\x04 \x01(\x05\x12\x0b\n\x03msg\x18\x05 \x01(\t\x12\x0c\n\x04\x63ode\x18\x06 \x01(\x05\"!\n\x03Key\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05\x63hunk\x18\x02 \x01(\t\"Y\n\x07Replace\x12&\n\told_chunk\x18\x01 \x01(\x0b\x32\x13.MasterServer.Chunk\x12&\n\tnew_chunk\x18\x02 \x01(\x0b\x32\x13.MasterServer.Chunk\"1\n\tSecondary\x12\n\n\x02id\x18\x01 \x01(\t\x12\n\n\x02ip\x18\x02 \x01(\t\x12\x0c\n\x04port\x18\x03 \x01(\t\"B\n\tDirectory\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05\x63hunk\x18\x02 \x01(\t\x12\x0b\n\x03msg\x18\x03 \x01(\t\x12\x0c\n\x04\x63ode\x18\x04 \x01(\x05\"#\n\x07Primary\x12\n\n\x02ip\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\t\"\x07\n\x05\x45mpty2\xe1\x04\n\x0cMasterServer\x12\x33\n\x05heart\x12\x13.MasterServer.Empty\x1a\x13.MasterServer.Reply\"\x00\x12\x37\n\tadd_chunk\x12\x13.MasterServer.Chunk\x1a\x13.MasterServer.Reply\"\x00\x12\x35\n\tget_chunk\x12\x11.MasterServer.Key\x1a\x13.MasterServer.Chunk\"\x00\x12\x36\n\ninsert_key\x12\x11.MasterServer.Key\x1a\x13.MasterServer.Chunk\"\x00\x12\x36\n\ndelete_key\x12\x11.MasterServer.Key\x1a\x13.MasterServer.Chunk\"\x00\x12=\n\rreplace_chunk\x12\x15.MasterServer.Replace\x1a\x13.MasterServer.Reply\"\x00\x12?\n\radd_secondary\x12\x17.MasterServer.Secondary\x1a\x13.MasterServer.Reply\"\x00\x12\x42\n\x0esync_directory\x12\x13.MasterServer.Empty\x1a\x17.MasterServer.Directory\"\x00\x30\x01\x12;\n\x0bsync_chunks\x12\x13.MasterServer.Empty\x1a\x13.MasterServer.Chunk\"\x00\x30\x01\x12;\n\x0bget_primary\x12\x13.MasterServer.Empty\x1a\x15.MasterServer.Primary\"\x00\x62\x06proto3'
)




_REPLY = _descriptor.Descriptor(
  name='Reply',
  full_name='MasterServer.Reply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='msg', full_name='MasterServer.Reply.msg', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='code', full_name='MasterServer.Reply.code', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=36,
  serialized_end=70,
)


_CHUNK = _descriptor.Descriptor(
  name='Chunk',
  full_name='MasterServer.Chunk',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='MasterServer.Chunk.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ip', full_name='MasterServer.Chunk.ip', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='port', full_name='MasterServer.Chunk.port', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='num_keys', full_name='MasterServer.Chunk.num_keys', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='msg', full_name='MasterServer.Chunk.msg', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='code', full_name='MasterServer.Chunk.code', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=72,
  serialized_end=162,
)


_KEY = _descriptor.Descriptor(
  name='Key',
  full_name='MasterServer.Key',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='MasterServer.Key.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='chunk', full_name='MasterServer.Key.chunk', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=164,
  serialized_end=197,
)


_REPLACE = _descriptor.Descriptor(
  name='Replace',
  full_name='MasterServer.Replace',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='old_chunk', full_name='MasterServer.Replace.old_chunk', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='new_chunk', full_name='MasterServer.Replace.new_chunk', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=199,
  serialized_end=288,
)


_SECONDARY = _descriptor.Descriptor(
  name='Secondary',
  full_name='MasterServer.Secondary',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='MasterServer.Secondary.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ip', full_name='MasterServer.Secondary.ip', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='port', full_name='MasterServer.Secondary.port', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=290,
  serialized_end=339,
)


_DIRECTORY = _descriptor.Descriptor(
  name='Directory',
  full_name='MasterServer.Directory',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='MasterServer.Directory.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='chunk', full_name='MasterServer.Directory.chunk', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='msg', full_name='MasterServer.Directory.msg', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='code', full_name='MasterServer.Directory.code', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=341,
  serialized_end=407,
)


_PRIMARY = _descriptor.Descriptor(
  name='Primary',
  full_name='MasterServer.Primary',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='ip', full_name='MasterServer.Primary.ip', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='port', full_name='MasterServer.Primary.port', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=409,
  serialized_end=444,
)


_EMPTY = _descriptor.Descriptor(
  name='Empty',
  full_name='MasterServer.Empty',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=446,
  serialized_end=453,
)

_REPLACE.fields_by_name['old_chunk'].message_type = _CHUNK
_REPLACE.fields_by_name['new_chunk'].message_type = _CHUNK
DESCRIPTOR.message_types_by_name['Reply'] = _REPLY
DESCRIPTOR.message_types_by_name['Chunk'] = _CHUNK
DESCRIPTOR.message_types_by_name['Key'] = _KEY
DESCRIPTOR.message_types_by_name['Replace'] = _REPLACE
DESCRIPTOR.message_types_by_name['Secondary'] = _SECONDARY
DESCRIPTOR.message_types_by_name['Directory'] = _DIRECTORY
DESCRIPTOR.message_types_by_name['Primary'] = _PRIMARY
DESCRIPTOR.message_types_by_name['Empty'] = _EMPTY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Reply = _reflection.GeneratedProtocolMessageType('Reply', (_message.Message,), {
  'DESCRIPTOR' : _REPLY,
  '__module__' : 'MasterServer_pb2'
  # @@protoc_insertion_point(class_scope:MasterServer.Reply)
  })
_sym_db.RegisterMessage(Reply)

Chunk = _reflection.GeneratedProtocolMessageType('Chunk', (_message.Message,), {
  'DESCRIPTOR' : _CHUNK,
  '__module__' : 'MasterServer_pb2'
  # @@protoc_insertion_point(class_scope:MasterServer.Chunk)
  })
_sym_db.RegisterMessage(Chunk)

Key = _reflection.GeneratedProtocolMessageType('Key', (_message.Message,), {
  'DESCRIPTOR' : _KEY,
  '__module__' : 'MasterServer_pb2'
  # @@protoc_insertion_point(class_scope:MasterServer.Key)
  })
_sym_db.RegisterMessage(Key)

Replace = _reflection.GeneratedProtocolMessageType('Replace', (_message.Message,), {
  'DESCRIPTOR' : _REPLACE,
  '__module__' : 'MasterServer_pb2'
  # @@protoc_insertion_point(class_scope:MasterServer.Replace)
  })
_sym_db.RegisterMessage(Replace)

Secondary = _reflection.GeneratedProtocolMessageType('Secondary', (_message.Message,), {
  'DESCRIPTOR' : _SECONDARY,
  '__module__' : 'MasterServer_pb2'
  # @@protoc_insertion_point(class_scope:MasterServer.Secondary)
  })
_sym_db.RegisterMessage(Secondary)

Directory = _reflection.GeneratedProtocolMessageType('Directory', (_message.Message,), {
  'DESCRIPTOR' : _DIRECTORY,
  '__module__' : 'MasterServer_pb2'
  # @@protoc_insertion_point(class_scope:MasterServer.Directory)
  })
_sym_db.RegisterMessage(Directory)

Primary = _reflection.GeneratedProtocolMessageType('Primary', (_message.Message,), {
  'DESCRIPTOR' : _PRIMARY,
  '__module__' : 'MasterServer_pb2'
  # @@protoc_insertion_point(class_scope:MasterServer.Primary)
  })
_sym_db.RegisterMessage(Primary)

Empty = _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), {
  'DESCRIPTOR' : _EMPTY,
  '__module__' : 'MasterServer_pb2'
  # @@protoc_insertion_point(class_scope:MasterServer.Empty)
  })
_sym_db.RegisterMessage(Empty)



_MASTERSERVER = _descriptor.ServiceDescriptor(
  name='MasterServer',
  full_name='MasterServer.MasterServer',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=456,
  serialized_end=1065,
  methods=[
  _descriptor.MethodDescriptor(
    name='heart',
    full_name='MasterServer.MasterServer.heart',
    index=0,
    containing_service=None,
    input_type=_EMPTY,
    output_type=_REPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='add_chunk',
    full_name='MasterServer.MasterServer.add_chunk',
    index=1,
    containing_service=None,
    input_type=_CHUNK,
    output_type=_REPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='get_chunk',
    full_name='MasterServer.MasterServer.get_chunk',
    index=2,
    containing_service=None,
    input_type=_KEY,
    output_type=_CHUNK,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='insert_key',
    full_name='MasterServer.MasterServer.insert_key',
    index=3,
    containing_service=None,
    input_type=_KEY,
    output_type=_CHUNK,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='delete_key',
    full_name='MasterServer.MasterServer.delete_key',
    index=4,
    containing_service=None,
    input_type=_KEY,
    output_type=_CHUNK,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='replace_chunk',
    full_name='MasterServer.MasterServer.replace_chunk',
    index=5,
    containing_service=None,
    input_type=_REPLACE,
    output_type=_REPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='add_secondary',
    full_name='MasterServer.MasterServer.add_secondary',
    index=6,
    containing_service=None,
    input_type=_SECONDARY,
    output_type=_REPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='sync_directory',
    full_name='MasterServer.MasterServer.sync_directory',
    index=7,
    containing_service=None,
    input_type=_EMPTY,
    output_type=_DIRECTORY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='sync_chunks',
    full_name='MasterServer.MasterServer.sync_chunks',
    index=8,
    containing_service=None,
    input_type=_EMPTY,
    output_type=_CHUNK,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='get_primary',
    full_name='MasterServer.MasterServer.get_primary',
    index=9,
    containing_service=None,
    input_type=_EMPTY,
    output_type=_PRIMARY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_MASTERSERVER)

DESCRIPTOR.services_by_name['MasterServer'] = _MASTERSERVER

# @@protoc_insertion_point(module_scope)
