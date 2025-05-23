"""System Information classes."""

import collections.abc
from typing import Optional

import nisyscfg.errors
import nisyscfg.types
from nisyscfg._lib import c_string_decode


class SystemInfoIterator(collections.abc.Iterator):
    """Iterator for system information handles in nisyscfg."""

    def __init__(self, handle: nisyscfg.types.Handle) -> None:
        """Initialize the iterator with a system info handle."""
        self._handle: Optional[nisyscfg.types.Handle] = handle
        self._library = nisyscfg._library_singleton.get()

    def __del__(self) -> None:
        """Destructor to ensure the handle is closed when the iterator is deleted."""
        self.close()

    def __iter__(self) -> "SystemInfoIterator":
        """Return the iterator object itself."""
        return self

    def __next__(self) -> str:
        """Return the next system name in the enumeration."""
        if not self._handle:
            raise StopIteration()
        system_name = nisyscfg.types.simple_string()
        error_code = self._library.NextSystemInfo(self._handle, system_name)
        if error_code == nisyscfg.errors.Status.END_OF_ENUM:
            raise StopIteration()
        nisyscfg.errors.handle_error(None, error_code)
        return c_string_decode(system_name.value)

    def close(self) -> None:
        """Close the system info handle if it is open."""
        if self._handle:
            error_code = self._library.CloseHandle(self._handle)
            nisyscfg.errors.handle_error(None, error_code)
            self._handle = None
