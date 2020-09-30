import ctypes
import nisyscfg.errors
import typing

from nisyscfg._lib import c_string_decode


ComponentInfo = typing.NamedTuple(
    'ComponentInfo', [
        ('id', str),
        ('version', str),
        ('title', str),
        ('type', str),
        ('details', str),
    ]
)


class ComponentInfoIterator(object):
    def __init__(self, handle):
        self._handle = handle
        self._library = nisyscfg._library_singleton.get()

    def __del__(self):
        self.close()

    def __iter__(self):
        return self

    def __next__(self) -> ComponentInfo:
        if not self._handle:
            raise StopIteration()
        id = nisyscfg.types.simple_string()
        version = nisyscfg.types.simple_string()
        title = nisyscfg.types.simple_string()
        item_type = nisyscfg.types.ctypes.c_long()
        c_details = ctypes.POINTER(ctypes.c_char)()
        error_code = self._library.NextComponentInfo(self._handle, id, version, title, ctypes.pointer(item_type), c_details)
        if error_code == 1:
            raise StopIteration()
        nisyscfg.errors.handle_error(self, error_code)

        if c_details:
            details = c_string_decode(ctypes.cast(c_details, ctypes.c_char_p).value)
            error_code = self._library.FreeDetailedString(c_details)
            nisyscfg.errors.handle_error(self, error_code)
        else:
            details = None

        return ComponentInfo(
            id=c_string_decode(id.value),
            version=c_string_decode(version.value),
            title=c_string_decode(title.value),
            type=nisyscfg.enums.ComponentType(item_type.value),
            details=details,
        )

    def close(self) -> None:
        if self._handle:
            error_code = self._library.CloseHandle(self._handle)
            nisyscfg.errors.handle_error(self, error_code)
            self._handle = None
