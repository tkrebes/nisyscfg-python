import ctypes
import nisyscfg.enums
import nisyscfg.errors
import typing

from nisyscfg._lib import c_string_decode
from nisyscfg._lib import c_string_encode


ComponentInfo = typing.NamedTuple(
    "ComponentInfo",
    [
        ("id", str),
        ("version", str),
        ("title", str),
        ("type", str),
        ("details", str),
    ],
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
        error_code = self._library.NextComponentInfo(
            self._handle, id, version, title, ctypes.pointer(item_type), c_details
        )
        if error_code == nisyscfg.errors.Status.END_OF_ENUM:
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


class EnumSoftwareComponent(object):
    def __init__(self):
        self._handle = nisyscfg.types.EnumSoftwareComponentHandle()
        self._library = nisyscfg._library_singleton.get()
        error_code = self._library.CreateComponentsEnum(ctypes.pointer(self._handle))
        nisyscfg.errors.handle_error(self, error_code)

    def __del__(self):
        self.close()

    def close(self) -> None:
        if self._handle:
            error_code = self._library.CloseHandle(self._handle)
            nisyscfg.errors.handle_error(self, error_code)
            self._handle = None

    def add_component(
        self,
        id: str,
        version: str = "",
        mode: nisyscfg.enums.VersionSelectionMode = nisyscfg.enums.VersionSelectionMode.HIGHEST,
    ) -> None:
        """
        Adds a software component

        id - ID of the software component to be added to the enumeration.

        version - Desired version of the software component being added to the
        enumeration. This field is optional as long as the version selection
        mode is set to Highest.

        mode - Choose whether an exact version or the highest version of the
        software component specified by id should be added to the enumeration.

        Raises an nisyscfg.errors.LibraryError exception in the event of an error.
        """
        error_code = self._library.AddComponentToEnum(
            self._handle, c_string_encode(id), c_string_encode(version), mode
        )
        nisyscfg.errors.handle_error(self, error_code)
