"""Software feed classes."""

import collections.abc
import ctypes
from typing import NamedTuple, Optional

import nisyscfg.errors
import nisyscfg.types
from nisyscfg._lib import c_string_decode


class SoftwareFeed(NamedTuple):
    """Represents a software feed with its properties."""

    name: str
    """The name of the software feed."""
    uri: str
    """The URI of the software feed."""
    enabled: bool
    """Indicates if the software feed is enabled."""
    trusted: bool
    """Indicates if the software feed is trusted."""


class SoftwareFeedIterator(collections.abc.Iterator):
    """Iterator for traversing software feeds."""

    def __init__(self, handle: Optional[nisyscfg.types.Handle] = None) -> None:
        """Initialize the iterator with a handle to the software feed collection.

        Args:
            handle: The handle to the software feed collection.
        """
        self._handle = handle
        self._library = nisyscfg._library_singleton.get()

    def __del__(self) -> None:
        """Destructor to ensure the handle is closed when the iterator is deleted."""
        self.close()

    def __iter__(self) -> "SoftwareFeedIterator":
        """Return the iterator itself."""
        return self

    def __next__(self) -> SoftwareFeed:
        """Return the next SoftwareFeed in the collection.

        Returns:
            SoftwareFeed: The next software feed in the collection.

        Raises:
            StopIteration: If there are no more software feeds.
        """
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
        nisyscfg.errors.handle_error(None, error_code)
        return SoftwareFeed(
            name=c_string_decode(name.value),
            uri=c_string_decode(uri.value),
            enabled=enabled.value != 0,
            trusted=trusted.value != 0,
        )

    def close(self) -> None:
        """Close the iterator and release any associated resources."""
        if self._handle:
            error_code = self._library.CloseHandle(self._handle)
            nisyscfg.errors.handle_error(None, error_code)
            self._handle = None
