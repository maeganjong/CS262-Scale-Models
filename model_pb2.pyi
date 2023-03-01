from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Note(_message.Message):
    __slots__ = ["length_queue", "logical_clock_time", "recipient", "sender"]
    LENGTH_QUEUE_FIELD_NUMBER: _ClassVar[int]
    LOGICAL_CLOCK_TIME_FIELD_NUMBER: _ClassVar[int]
    RECIPIENT_FIELD_NUMBER: _ClassVar[int]
    SENDER_FIELD_NUMBER: _ClassVar[int]
    length_queue: int
    logical_clock_time: int
    recipient: int
    sender: int
    def __init__(self, sender: _Optional[int] = ..., recipient: _Optional[int] = ..., logical_clock_time: _Optional[int] = ..., length_queue: _Optional[int] = ...) -> None: ...

class Text(_message.Message):
    __slots__ = ["text"]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    text: str
    def __init__(self, text: _Optional[str] = ...) -> None: ...
