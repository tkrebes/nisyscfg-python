"""NI System Configuration Filter classes."""

import ctypes
from typing import Any, Union

import nisyscfg
import nisyscfg.enums
import nisyscfg.errors
import nisyscfg.properties
import nisyscfg.xnet.filter
import nisyscfg.xnet.properties
from nisyscfg._lib import c_string_encode


@nisyscfg.properties.PropertyBag(nisyscfg.properties.Filter)
@nisyscfg.properties.PropertyBag(nisyscfg.xnet.properties.Filter, expert="xnet")
class Filter(object):
    """Represents a hardware filter object that you can use to query for specific resources.

    After creating an instance of this class, set one or more properties to limit the set of
    detected resources.
    """

    def __init__(self, session: nisyscfg.types.Handle) -> None:
        """Initializes a Filter object.

        Args:
            session: The session handle to associate with this filter.
        """
        self._handle = nisyscfg.types.FilterHandle()
        self._library = nisyscfg._library_singleton.get()
        self._property_accessor = nisyscfg.properties.PropertyAccessor(
            setter=self._set_property_with_type
        )
        error_code = self._library.CreateFilter(session, ctypes.pointer(self._handle))
        nisyscfg.errors.handle_error(None, error_code)

    def __del__(self) -> None:
        """Destructor for the Filter object. Ensures resources are released."""
        self.close()

    def close(self) -> None:
        """Closes the filter handle and releases associated resources."""
        if self._handle:
            error_code = self._library.CloseHandle(self._handle)
            nisyscfg.errors.handle_error(None, error_code)
            self._handle = nisyscfg.types.FilterHandle()

    def _set_property_with_type(self, id: int, value: Any, c_type: Any, nisyscfg_type: Any) -> None:
        """Sets a property on the filter with the specified type.

        Args:
            id: The property identifier.
            value: The value to set.
            c_type: The ctypes type of the property.
            nisyscfg_type: The NI System Configuration type of the property.
        """
        if c_type == ctypes.c_char_p:
            value = c_string_encode(value)
        elif issubclass(c_type, nisyscfg.enums._BaseEnum) or issubclass(
            c_type, nisyscfg.enums._BaseFlag
        ):
            value = ctypes.c_int(value)
        else:
            value = c_type(value)

        error_code = self._library.SetFilterPropertyWithType(self._handle, id, nisyscfg_type, value)
        nisyscfg.errors.handle_error(None, error_code)

    @property
    def property_accessor(self) -> nisyscfg.properties.PropertyAccessor:
        """The property accessor."""
        return self._property_accessor

    is_device: Union[nisyscfg.enums.Bool, int]
    """Specifies whether the resource is a device."""
    is_chassis: Union[nisyscfg.enums.Bool, int]
    """Specifies whether the resource is a chassis."""
    service_type: Union[nisyscfg.enums.ServiceType, int]
    """The service type associated with the resource."""
    connects_to_bus_type: Union[nisyscfg.enums.BusType, int]
    """The bus type to which the resource connects."""
    connects_to_link_name: str
    """The link name to which the resource connects."""
    provides_bus_type: Union[nisyscfg.enums.BusType, int]
    """The bus type provided by the resource."""
    vendor_id: int
    """The vendor ID for the resource."""
    product_id: int
    """The product ID for the resource."""
    serial_number: str
    """The serial number for the resource."""
    is_ni_product: Union[nisyscfg.enums.Bool, int]
    """Specifies whether the resource is an NI product."""
    is_simulated: Union[nisyscfg.enums.Bool, int]
    """Specifies whether the resource is simulated."""
    slot_number: int
    """The slot number for the resource."""
    has_driver: Union[nisyscfg.enums.HasDriverType, int]
    """Indicates whether the resource has a driver."""
    is_present: Union[nisyscfg.enums.IsPresentType, int]
    """Indicates whether the resource is present."""
    supports_calibration: Union[nisyscfg.enums.Bool, int]
    """Specifies whether the device supports calibration."""
    supports_firmware_update: Union[nisyscfg.enums.Bool, int]
    """Specifies whether the resource supports firmware update."""
    provides_link_name: str
    """The link name provided by the resource."""
    expert_name: str
    """The expert name for the resource."""
    resource_name: str
    """The resource name."""
    user_alias: str
    """The user alias for the resource."""

    xnet: nisyscfg.xnet.filter.Filter
    """The XNET filter properties."""
