import ctypes
import nisyscfg.errors
import typing

from nisyscfg._lib import c_string_decode

SoftwareFeed = typing.NamedTuple(
    "SoftwareFeed",
    [
        ("name", str),
        ("uri", str),
        ("enabled", bool),
        ("trusted", bool),
    ],
)


class SoftwareFeedIterator(object):
    def __init__(self, handle):
        self._handle = handle
        self._library = nisyscfg._library_singleton.get()

    def __del__(self):
        self.close()

    def __iter__(self):
        return self

    def __next__(self) -> SoftwareFeed:
        if not self._handle:
            raise StopIteration()
        name = nisyscfg.types.simple_string()
        uri = nisyscfg.types.simple_string()
        enabled = ctypes.c_int()
        trusted = ctypes.c_int()
        error_code = self._library.NextSoftwareFeed(
            self._handle, name, uri, ctypes.pointer(enabled), ctypes.pointer(trusted)
        )
        if error_code == nisyscfg.errors.Status.END_OF_ENUM:
            raise StopIteration()
        nisyscfg.errors.handle_error(self, error_code)
        return SoftwareFeed(
            name=c_string_decode(name.value),
            uri=c_string_decode(uri.value),
            enabled=enabled.value != 0,
            trusted=trusted.value != 0,
        )

    def close(self) -> None:
        if self._handle:
            error_code = self._library.CloseHandle(self._handle)
            nisyscfg.errors.handle_error(self, error_code)
            self._handle = None
