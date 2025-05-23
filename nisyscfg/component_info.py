"""Software component information classes."""

import collections.abc
import ctypes
from typing import NamedTuple, Optional

import nisyscfg.enums
import nisyscfg.errors
import nisyscfg.types
from nisyscfg._lib import c_string_decode, c_string_encode


class ComponentInfo(NamedTuple):
    """Class representing software component information."""

    id: str
    """ID of the component."""
    version: str
    """Version of the component."""
    title: str
    """Title of the component."""
    type: nisyscfg.enums.ComponentType
    """Type of the component."""
    details: str
    """Detailed description of the component."""


class ComponentInfoIterator(collections.abc.Iterator):
    """Iterator for traversing software component information objects."""

    def __init__(self, handle: Optional[nisyscfg.types.Handle] = None) -> None:
        """Initialize the iterator with a handle to the component enumeration resource.

        Args:
            handle: Handle to the component enumeration resource.
        """
        self._handle = handle
        self._library = nisyscfg._library_singleton.get()

    def __del__(self) -> None:
        """Release resources associated with the iterator upon deletion."""
        self.close()

    def __iter__(self) -> "ComponentInfoIterator":
        """Return the iterator object itself.

        Returns:
            ComponentInfoIterator: The iterator object itself.
        """
        return self

    def __next__(self) -> ComponentInfo:
        """Return the next ComponentInfo object in the enumeration.

        Returns:
            ComponentInfo: The next software component information object.

        Raises:
            StopIteration: If there are no more components.
            nisyscfg.errors.LibraryError: If an error occurs in the library.
        """
        if not self._handle:
            raise StopIteration()
        id = nisyscfg.types.simple_string()
        version = nisyscfg.types.simple_string()
        title = nisyscfg.types.simple_string()
        item_type = nisyscfg.types.ctypes.c_int()
        c_details = ctypes.POINTER(ctypes.c_char)()
        error_code = self._library.NextComponentInfo(
            self._handle, id, version, title, ctypes.pointer(item_type), c_details
        )
        if error_code == nisyscfg.errors.Status.END_OF_ENUM:
            raise StopIteration()
        nisyscfg.errors.handle_error(None, error_code)

        if c_details:
            details = c_string_decode(ctypes.cast(c_details, ctypes.c_char_p).value)
            error_code = self._library.FreeDetailedString(c_details)
            nisyscfg.errors.handle_error(None, error_code)
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
        """Close the iterator and release associated resources."""
        if self._handle:
            error_code = self._library.CloseHandle(self._handle)
            nisyscfg.errors.handle_error(None, error_code)
            self._handle = None


class EnumSoftwareComponent(object):
    """Class for enumerating and managing software components."""

    def __init__(self) -> None:
        """Initialize the software component enumerator and allocate resources."""
        self._handle: Optional[nisyscfg.types.EnumSoftwareComponentHandle] = (
            nisyscfg.types.EnumSoftwareComponentHandle()
        )
        self._library = nisyscfg._library_singleton.get()
        error_code = self._library.CreateComponentsEnum(ctypes.pointer(self._handle))
        nisyscfg.errors.handle_error(None, error_code)

    def __del__(self) -> None:
        """Release resources associated with the enumerator upon deletion."""
        self.close()

    def close(self) -> None:
        """Close the enumerator and release associated resources."""
        if self._handle:
            error_code = self._library.CloseHandle(self._handle)
            nisyscfg.errors.handle_error(None, error_code)
            self._handle = None

    def add_component(
        self,
        id: str,
        version: str = "",
        mode: nisyscfg.enums.VersionSelectionMode = nisyscfg.enums.VersionSelectionMode.HIGHEST,
    ) -> None:
        """Adds a software component.

        Args:
            id (str): ID of the software component to be added to the enumeration.
            version (str, optional): Desired version of the software component being added to the
                enumeration. This field is optional as long as the version selection
                mode is set to Highest.
            mode (nisyscfg.enums.VersionSelectionMode, optional): Choose whether an exact version
                or the highest version of the software component specified by id should be added
                to the enumeration.

        Raises:
            nisyscfg.errors.LibraryError: In the event of an error.
        """
        error_code = self._library.AddComponentToEnum(
            self._handle, c_string_encode(id), c_string_encode(version), mode
        )
        nisyscfg.errors.handle_error(None, error_code)
