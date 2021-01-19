import ctypes
import nisyscfg.component_info
import nisyscfg.enums
import nisyscfg.errors
import typing

from nisyscfg._lib import c_string_decode

DependencyInfo = typing.NamedTuple(
    "DependencyInfo",
    [
        ("depender", nisyscfg.component_info.ComponentInfo),
        ("dependee", nisyscfg.component_info.ComponentInfo),
    ],
)


class DependencyInfoIterator(object):
    def __init__(self, handle):
        self._handle = handle
        self._library = nisyscfg._library_singleton.get()

    def __del__(self):
        self.close()

    def __iter__(self):
        return self

    def __next__(self) -> DependencyInfo:
        if not self._handle:
            raise StopIteration()
        depender_id = nisyscfg.types.simple_string()
        depender_version = nisyscfg.types.simple_string()
        depender_title = nisyscfg.types.simple_string()
        c_depender_detailed_description = ctypes.POINTER(ctypes.c_char)()

        dependee_id = nisyscfg.types.simple_string()
        dependee_version = nisyscfg.types.simple_string()
        dependee_title = nisyscfg.types.simple_string()
        c_dependee_detailed_description = ctypes.POINTER(ctypes.c_char)()

        error_code = self._library.NextDependencyInfo(
            self._handle,
            depender_id,
            depender_version,
            depender_title,
            ctypes.pointer(c_depender_detailed_description),
            dependee_id,
            dependee_version,
            dependee_title,
            ctypes.pointer(c_dependee_detailed_description),
        )
        if error_code == nisyscfg.errors.Status.END_OF_ENUM:
            raise StopIteration()
        nisyscfg.errors.handle_error(self, error_code)

        if c_depender_detailed_description:
            depender_detailed_description = c_string_decode(
                ctypes.cast(c_depender_detailed_description, ctypes.c_char_p).value
            )
            error_code = self._library.FreeDetailedString(c_depender_detailed_description)
            nisyscfg.errors.handle_error(self, error_code)
        else:
            depender_detailed_description = ""

        if c_dependee_detailed_description:
            dependee_detailed_description = c_string_decode(
                ctypes.cast(c_dependee_detailed_description, ctypes.c_char_p).value
            )
            error_code = self._library.FreeDetailedString(c_dependee_detailed_description)
            nisyscfg.errors.handle_error(self, error_code)
        else:
            dependee_detailed_description = ""

        return DependencyInfo(
            depender=nisyscfg.component_info.ComponentInfo(
                id=c_string_decode(depender_id),
                version=c_string_decode(depender_version),
                title=c_string_decode(depender_title),
                type=nisyscfg.enums.ComponentType.UNKNOWN,
                details=depender_detailed_description,
            ),
            dependee=nisyscfg.component_info.ComponentInfo(
                id=c_string_decode(dependee_id),
                version=c_string_decode(dependee_version),
                title=c_string_decode(dependee_title),
                type=nisyscfg.enums.ComponentType.UNKNOWN,
                details=dependee_detailed_description,
            ),
        )

    def close(self) -> None:
        if self._handle:
            error_code = self._library.CloseHandle(self._handle)
            nisyscfg.errors.handle_error(self, error_code)
            self._handle = None
