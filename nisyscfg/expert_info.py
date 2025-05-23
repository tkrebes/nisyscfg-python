"""NI System Configuration Expert classes."""

import collections.abc
from typing import NamedTuple, Optional

import nisyscfg.errors
import nisyscfg.types
from nisyscfg._lib import c_string_decode


class ExpertInfo(NamedTuple):
    """Information about a NI System Configuration expert."""

    expert_name: str
    """The internal name of the expert."""
    display_name: str
    """The display name of the expert."""
    version: str
    """The version string of the expert."""


class ExpertInfoIterator(collections.abc.Iterator):
    """Iterator for traversing NI System Configuration experts."""

    def __init__(self, handle: nisyscfg.types.Handle):
        """Initialize the iterator with a handle.

        Args:
            handle: The handle to the expert info iterator from the library.
        """
        self._handle: Optional[nisyscfg.types.Handle] = handle
        self._library = nisyscfg._library_singleton.get()

    def __del__(self) -> None:
        """Destructor to ensure the handle is closed."""
        self.close()

    def __iter__(self) -> "ExpertInfoIterator":
        """Return the iterator itself.

        Returns:
            ExpertInfoIterator: The iterator instance.
        """
        return self

    def __next__(self) -> ExpertInfo:
        """Return the next ExpertInfo in the iterator.

        Returns:
            ExpertInfo: The next expert information object.

        Raises:
            StopIteration: If there are no more experts.
        """
        if not self._handle:
            # TODO(tkrebes): raise RuntimeError
            raise StopIteration()
        expert_name = nisyscfg.types.simple_string()
        display_name = nisyscfg.types.simple_string()
        version = nisyscfg.types.simple_string()
        error_code = self._library.NextExpertInfo(self._handle, expert_name, display_name, version)
        if error_code == nisyscfg.errors.Status.END_OF_ENUM:
            raise StopIteration()
        nisyscfg.errors.handle_error(None, error_code)
        return ExpertInfo(
            c_string_decode(expert_name.value),
            c_string_decode(display_name.value),
            c_string_decode(version.value),
        )

    def close(self) -> None:
        """Close the iterator and release the handle."""
        if self._handle:
            error_code = self._library.CloseHandle(self._handle)
            nisyscfg.errors.handle_error(None, error_code)
            self._handle = None
