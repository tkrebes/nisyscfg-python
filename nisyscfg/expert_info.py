import nisyscfg.errors
import typing

from nisyscfg._lib import c_string_decode


ExpertInfo = typing.NamedTuple(
    "ExpertInfo",
    [
        ("expert_name", str),
        ("display_name", str),
        ("version", str),
    ],
)


class ExpertInfoIterator(object):
    def __init__(self, handle):
        self._handle = handle
        self._library = nisyscfg._library_singleton.get()

    def __del__(self):
        self.close()

    def __iter__(self):
        return self

    def __next__(self) -> ExpertInfo:
        if not self._handle:
            # TODO(tkrebes): raise RuntimeError
            raise StopIteration()
        expert_name = nisyscfg.types.simple_string()
        display_name = nisyscfg.types.simple_string()
        version = nisyscfg.types.simple_string()
        error_code = self._library.NextExpertInfo(self._handle, expert_name, display_name, version)
        if error_code == nisyscfg.errors.Status.END_OF_ENUM:
            raise StopIteration()
        nisyscfg.errors.handle_error(self, error_code)
        return ExpertInfo(
            c_string_decode(expert_name.value),
            c_string_decode(display_name.value),
            c_string_decode(version.value),
        )

    def close(self) -> None:
        if self._handle:
            error_code = self._library.CloseHandle(self._handle)
            nisyscfg.errors.handle_error(self, error_code)
            self._handle = None
