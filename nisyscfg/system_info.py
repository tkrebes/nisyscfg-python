import nisyscfg.errors

from nisyscfg._lib import c_string_decode


class SystemInfoIterator(object):
    def __init__(self, handle):
        self._handle = handle
        self._library = nisyscfg._library_singleton.get()

    def __del__(self):
        self.close()

    def __iter__(self):
        return self

    def __next__(self) -> str:
        if not self._handle:
            raise StopIteration()
        system_name = nisyscfg.types.simple_string()
        error_code = self._library.NextSystemInfo(self._handle, system_name)
        if error_code == nisyscfg.errors.Status.END_OF_ENUM:
            raise StopIteration()
        nisyscfg.errors.handle_error(self, error_code)
        return c_string_decode(system_name.value)

    def close(self) -> None:
        if self._handle:
            error_code = self._library.CloseHandle(self._handle)
            nisyscfg.errors.handle_error(self, error_code)
            self._handle = None
