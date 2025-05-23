# flake8: noqa

from __future__ import annotations

import ctypes

simple_string = ctypes.c_char * 1024

UInt64 = ctypes.c_ulonglong
Handle = ctypes.c_void_p
ResourceHandle = Handle
EnumResourceHandle = Handle
EnumSoftwareFeedHandle = Handle
SessionHandle = Handle
class TimestampUTC(ctypes.Array):
    _length_ = 4
    _type_ = ctypes.c_uint
EnumSoftwareComponentHandle = Handle
EnumDependencyHandle = Handle
SoftwareSetHandle = Handle
FilterHandle = Handle
EnumExpertHandle = Handle
EnumSystemHandle = Handle
EnumSoftwareSetHandle = Handle
