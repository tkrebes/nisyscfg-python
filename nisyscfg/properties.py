"""Properties."""

import collections.abc
import ctypes
from typing import Any, Callable, Iterator, Optional, Protocol, Type, TypeVar

import hightime

import nisyscfg.errors
import nisyscfg.timestamp
import nisyscfg.types
from nisyscfg.enums import (
    AccessType,
    AdapterMode,
    AdapterType,
    Bool,
    BusType,
    ConnectionType,
    EapType,
    FileSystemMode,
    FirmwareUpdateMode,
    HasDriverType,
    IpAddressMode,
    IsPresentType,
    LedState,
    LinkSpeed,
    ModuleProgramMode,
    PacketDetection,
    PropertyType,
    SecurityType,
    ServiceType,
    SwitchState,
)


def _raise_not_supported(*args: Any, **kwargs: Any) -> None:
    """Raise a NotImplementedError."""
    raise NotImplementedError("This method is not supported in this context.")


class PropertyAccessor(object):
    """Provides access to get and set properties on NI System Configuration objects."""

    __slots__ = "_getter", "_setter", "_indexed_getter"

    def __init__(
        self,
        setter: Optional[Callable] = None,
        getter: Optional[Callable] = None,
        indexed_getter: Optional[Callable] = None,
    ):
        """Initializes the PropertyAccessor."""
        self._setter = setter or _raise_not_supported
        self._getter = getter or _raise_not_supported
        self._indexed_getter = indexed_getter or _raise_not_supported

    def set_bool_property(self, id: int, value: bool) -> None:
        """Set a boolean property value."""
        self._setter(id, value, Bool, PropertyType.BOOL)

    def set_int_property(self, id: int, value: int) -> None:
        """Set an integer property value."""
        self._setter(id, value, ctypes.c_int, PropertyType.INT)

    def set_unsigned_int_property(self, id: int, value: int) -> None:
        """Set an unsigned integer property value."""
        self._setter(id, value, ctypes.c_uint, PropertyType.UNSIGNED_INT)

    def set_double_property(self, id: int, value: float) -> None:
        """Set a double property value."""
        self._setter(id, value, ctypes.c_double, PropertyType.DOUBLE)

    def set_string_property(self, id: int, value: str) -> None:
        """Set a string property value."""
        self._setter(id, value, ctypes.c_char_p, PropertyType.STRING)

    def set_timestamp_property(self, id: int, value: hightime.datetime) -> None:
        """Set a timestamp property value."""
        self._setter(id, value, nisyscfg.types.TimestampUTC, PropertyType.TIMESTAMP)

    def get_bool_property(self, id: int) -> bool:
        """Get a boolean property value."""
        return self._getter(id, Bool)  # type: ignore[return-value]

    def get_int_property(self, id: int) -> int:
        """Get an integer property value."""
        return self._getter(id, ctypes.c_int)  # type: ignore[return-value]

    def get_unsigned_int_property(self, id: int) -> int:
        """Get an unsigned integer property value."""
        return self._getter(id, ctypes.c_uint)  # type: ignore[return-value]

    def get_double_property(self, id: int) -> float:
        """Get a double property value."""
        return self._getter(id, ctypes.c_double)  # type: ignore[return-value]

    def get_string_property(self, id: int) -> str:
        """Get a string property value."""
        return self._getter(id, ctypes.c_char_p)  # type: ignore[return-value]

    def get_timestamp_property(self, id: int) -> hightime.datetime:
        """Get a timestamp property value."""
        return self._getter(id, nisyscfg.types.TimestampUTC)

    def get_indexed_bool_property(self, id: int, index: int) -> bool:
        """Get a boolean value from an indexed property."""
        return self._indexed_getter(id, index, Bool)  # type: ignore[return-value]

    def get_indexed_int_property(self, id: int, index: int) -> int:
        """Get an integer value from an indexed property."""
        return self._indexed_getter(id, index, ctypes.c_int)  # type: ignore[return-value]

    def get_indexed_unsigned_int_property(self, id: int, index: int) -> int:
        """Get an unsigned integer value from an indexed property."""
        return self._indexed_getter(id, index, ctypes.c_uint)  # type: ignore[return-value]

    def get_indexed_double_property(self, id: int, index: int) -> float:
        """Get a double value from an indexed property."""
        return self._indexed_getter(id, index, ctypes.c_double)  # type: ignore[return-value]

    def get_indexed_string_property(self, id: int, index: int) -> str:
        """Get a string value from an indexed property."""
        return self._indexed_getter(id, index, ctypes.c_char_p)  # type: ignore[return-value]

    def get_indexed_timestamp_property(self, id: int, index: int) -> hightime.datetime:
        """Get a timestamp value from an indexed property."""
        return self._indexed_getter(id, index, nisyscfg.types.TimestampUTC)


class TypeProperty(object):
    """Base class for type properties used in NI System Configuration."""

    __slots__ = "_id", "_enum", "_readable", "_writeable"

    def __init__(
        self, id: int, enum: Optional[type] = None, *, readable: bool = True, writeable: bool = True
    ):
        """Initializes a TypeProperty."""
        self._id = id
        self._enum = enum
        self._readable = readable
        self._writeable = writeable

    def get(self, accessor: PropertyAccessor) -> Any:
        """Get the property value."""
        raise NotImplementedError

    def set(self, accessor: PropertyAccessor, value: Any) -> None:
        """Set the property value."""
        raise NotImplementedError


class BoolProperty(TypeProperty):
    """Boolean property type for NI System Configuration."""

    __slots__ = ()

    def get(self, accessor: PropertyAccessor) -> bool:
        """Get the boolean property value."""
        value = accessor.get_bool_property(self._id)
        if self._enum:
            return self._enum(value)
        return value

    def set(self, accessor: PropertyAccessor, value: bool) -> None:
        """Set the boolean property value."""
        accessor.set_bool_property(self._id, value)


class IntProperty(TypeProperty):
    """Integer property type for NI System Configuration."""

    __slots__ = ()

    def get(self, accessor: PropertyAccessor) -> int:
        """Get the integer property value."""
        value = accessor.get_int_property(self._id)
        if self._enum:
            return self._enum(value)
        return value

    def set(self, accessor: PropertyAccessor, value: int) -> None:
        """Set the integer property value."""
        accessor.set_int_property(self._id, value)


class UnsignedIntProperty(TypeProperty):
    """Unsigned integer property type for NI System Configuration."""

    __slots__ = ()

    def get(self, accessor: PropertyAccessor) -> int:
        """Get the unsigned integer property value."""
        value = accessor.get_unsigned_int_property(self._id)
        if self._enum:
            return self._enum(value)
        return value

    def set(self, accessor: PropertyAccessor, value: int) -> None:
        """Set the unsigned integer property value."""
        accessor.set_unsigned_int_property(self._id, value)


class DoubleProperty(TypeProperty):
    """Double property type for NI System Configuration."""

    __slots__ = ()

    def get(self, accessor: PropertyAccessor) -> float:
        """Get the double property value."""
        return accessor.get_double_property(self._id)

    def set(self, accessor: PropertyAccessor, value: float) -> None:
        """Set the double property value."""
        accessor.set_double_property(self._id, value)


class StringProperty(TypeProperty):
    """String property type for NI System Configuration."""

    __slots__ = ()

    def get(self, accessor: PropertyAccessor) -> str:
        """Get the string property value."""
        return accessor.get_string_property(self._id)

    def set(self, accessor: PropertyAccessor, value: str) -> None:
        """Set the string property value."""
        accessor.set_string_property(self._id, value)


class TimestampProperty(TypeProperty):
    """Timestamp property type for NI System Configuration."""

    __slots__ = ()

    def get(self, accessor: PropertyAccessor) -> hightime.datetime:
        """Get the timestamp property value."""
        return accessor.get_timestamp_property(self._id)

    def set(self, accessor: PropertyAccessor, value: hightime.datetime) -> None:
        """Set the timestamp property value."""
        accessor.set_timestamp_property(self._id, value)


class IndexedPropertyItems(object):
    """Represents a collection of indexed property items for NI System Configuration."""

    def __init__(self, accessor: PropertyAccessor, tag: "IndexedProperty") -> None:
        """Initializes the IndexedPropertyItems."""
        self._accessor = accessor
        self._tag = tag

    def __getitem__(self, index: int) -> Any:
        """Get the item at the specified index."""
        try:
            index + 1
        except TypeError:
            raise TypeError(index)
        # The index is stored as a 12-bit number in the driver.
        if index < 0 and index >= 4096:
            raise IndexError(index)
        try:
            return self._tag.get_index(self._accessor, index)
        except nisyscfg.errors.LibraryError as err:
            if err.code == nisyscfg.errors.Status.PROP_DOES_NOT_EXIST:
                raise IndexError(index)
            raise

    def __len__(self) -> int:
        """Get the number of items in the indexed property."""
        if not hasattr(self, "_len"):
            try:
                self._len = self._tag.count_property.get(self._accessor)
            # Not all NI System API experts implement the count property. So
            # if it does not exist, explicitly count each index.
            except nisyscfg.errors.LibraryError as err:
                if err.code == nisyscfg.errors.Status.PROP_DOES_NOT_EXIST:
                    self._len = sum(1 for _ in self)
        return self._len

    def __iter__(self) -> Iterator["IndexedPropertyItems"]:
        """Return an iterator over the indexed property items."""

        class IndexedPropertyItemsIter(collections.abc.Iterator):
            __slots__ = "_properties", "_index"

            def __init__(self, properties: IndexedPropertyItems) -> None:
                self._properties = properties
                self._index = -1

            def __next__(self) -> IndexedPropertyItems:
                self._index += 1
                try:
                    return self._properties[self._index]
                except IndexError:
                    raise StopIteration()

            def next(self) -> IndexedPropertyItems:
                return self.__next__()

        return IndexedPropertyItemsIter(self)


class IndexedProperty(TypeProperty):
    """Base class for indexed properties in NI System Configuration."""

    __slots__ = ("_count_property",)

    def __init__(
        self,
        id: int,
        count_property: TypeProperty,
        enum: Optional[type] = None,
        *,
        readable: bool = True,
        writeable: bool = True,
    ):
        """Initializes an IndexedProperty."""
        self._id = id
        self._count_property = count_property
        self._enum = enum
        self._readable = readable
        self._writeable = writeable

    @property
    def count_property(self) -> TypeProperty:
        """The property that counts the number of indexed items."""
        return self._count_property

    def get(self, accessor: PropertyAccessor) -> IndexedPropertyItems:
        """Get the collection of indexed property items."""
        return IndexedPropertyItems(accessor, self)

    def get_index(self, accessor: PropertyAccessor, index: int) -> Any:
        """Get the value at the specified index."""
        raise NotImplementedError


class IndexedBoolProperty(IndexedProperty):
    """Indexed boolean property type for NI System Configuration."""

    __slots__ = ()

    def get_index(self, accessor: PropertyAccessor, index: int) -> bool:
        """Get the boolean value at the specified index."""
        value = accessor.get_indexed_bool_property(self._id, index)
        if self._enum:
            return self._enum(value)
        return value


class IndexedIntProperty(IndexedProperty):
    """Indexed integer property type for NI System Configuration."""

    __slots__ = ()

    def get_index(self, accessor: PropertyAccessor, index: int) -> int:
        """Get the integer value at the specified index."""
        value = accessor.get_indexed_int_property(self._id, index)
        if self._enum:
            return self._enum(value)
        return value


class IndexedUnsignedIntProperty(IndexedProperty):
    """Indexed unsigned integer property type for NI System Configuration."""

    __slots__ = ()

    def get_index(self, accessor: PropertyAccessor, index: int) -> int:
        """Get the unsigned integer value at the specified index."""
        value = accessor.get_indexed_unsigned_int_property(self._id, index)
        if self._enum:
            return self._enum(value)
        return value


class IndexedDoubleProperty(IndexedProperty):
    """Indexed double property type for NI System Configuration."""

    __slots__ = ()

    def get_index(self, accessor: PropertyAccessor, index: int) -> float:
        """Get the double value at the specified index."""
        return accessor.get_indexed_double_property(self._id, index)


class IndexedStringProperty(IndexedProperty):
    """Indexed string property type for NI System Configuration."""

    __slots__ = ()

    def get_index(self, accessor: PropertyAccessor, index: int) -> str:
        """Get the string value at the specified index."""
        return accessor.get_indexed_string_property(self._id, index)


class IndexedTimestampProperty(IndexedProperty):
    """Indexed timestamp property type for NI System Configuration."""

    __slots__ = ()

    def get_index(self, accessor: PropertyAccessor, index: int) -> hightime.datetime:
        """Get the timestamp value at the specified index."""
        return accessor.get_indexed_timestamp_property(self._id, index)


class PropertyGroup(object):
    """Base class for property groups in NI System Configuration."""

    pass


class Resource(PropertyGroup):
    """Property group for NI System Configuration resources."""

    IS_DEVICE = BoolProperty(16781312)
    IS_CHASSIS = BoolProperty(16941056)
    CONNECTS_TO_BUS_TYPE = IntProperty(16785408, enum=BusType)
    VENDOR_ID = UnsignedIntProperty(16789504)
    VENDOR_NAME = StringProperty(16793600)
    PRODUCT_ID = UnsignedIntProperty(16797696)
    PRODUCT_NAME = StringProperty(16801792)
    SERIAL_NUMBER = StringProperty(16805888)
    FIRMWARE_REVISION = StringProperty(16969728)
    IS_NI_PRODUCT = BoolProperty(16809984)
    IS_SIMULATED = BoolProperty(16814080)
    CONNECTS_TO_LINK_NAME = StringProperty(16818176)
    HAS_DRIVER = IntProperty(16920576, enum=HasDriverType)
    IS_PRESENT = IntProperty(16924672, enum=IsPresentType)
    SLOT_NUMBER = IntProperty(16822272)
    SUPPORTS_INTERNAL_CALIBRATION = BoolProperty(16842752)
    INTERNAL_CALIBRATION_LAST_TIME = TimestampProperty(16846848)
    INTERNAL_CALIBRATION_LAST_TEMP = DoubleProperty(16850944)
    SUPPORTS_EXTERNAL_CALIBRATION = BoolProperty(16859136)
    EXTERNAL_CALIBRATION_LAST_TEMP = DoubleProperty(16867328)
    CALIBRATION_COMMENTS = StringProperty(16961536)
    INTERNAL_CALIBRATION_LAST_LIMITED = BoolProperty(17420288)
    EXTERNAL_CALIBRATION_CHECKSUM = StringProperty(17432576)
    CURRENT_TEMP = DoubleProperty(16965632)
    PXI_PCI_BUS_NUMBER = UnsignedIntProperty(16875520)
    PXI_PCI_DEVICE_NUMBER = UnsignedIntProperty(16879616)
    PXI_PCI_FUNCTION_NUMBER = UnsignedIntProperty(16883712)
    PXI_PCI_LINK_WIDTH = IntProperty(16973824)
    PXI_PCI_MAX_LINK_WIDTH = IntProperty(16977920)
    USB_INTERFACE = UnsignedIntProperty(16887808)
    TCP_HOST_NAME = StringProperty(16928768)
    TCP_MAC_ADDRESS = StringProperty(16986112)
    TCP_IP_ADDRESS = StringProperty(16957440)
    TCP_DEVICE_CLASS = StringProperty(17022976)
    GPIB_PRIMARY_ADDRESS = IntProperty(16994304)
    GPIB_SECONDARY_ADDRESS = IntProperty(16998400)
    SERIAL_PORT_BINDING = StringProperty(17076224)
    PROVIDES_BUS_TYPE = IntProperty(16932864, enum=BusType)
    PROVIDES_LINK_NAME = StringProperty(16936960)
    NUMBER_OF_SLOTS = IntProperty(16826368)
    SUPPORTS_FIRMWARE_UPDATE = BoolProperty(17080320)
    FIRMWARE_FILE_PATTERN = StringProperty(17084416)
    RECOMMENDED_CALIBRATION_INTERVAL = IntProperty(17207296)
    SUPPORTS_CALIBRATION_WRITE = BoolProperty(17215488)
    HARDWARE_REVISION = StringProperty(17256448)
    CPU_MODEL_NAME = StringProperty(17313792)
    CPU_STEPPING_REVISION = IntProperty(17317888)
    MODEL_NAME_NUMBER = UnsignedIntProperty(17436672)
    MODULE_PROGRAM_MODE = IntProperty(17440768, enum=ModuleProgramMode)
    CONNECTS_TO_NUM_SLOTS = IntProperty(17072128)
    SLOT_OFFSET_LEFT = UnsignedIntProperty(17276928)
    INTERNAL_CALIBRATION_VALUES_IN_RANGE = BoolProperty(17489920)
    FIRMWARE_UPDATE_MODE = IntProperty(17354752, enum=FirmwareUpdateMode)
    EXTERNAL_CALIBRATION_LAST_TIME = TimestampProperty(16863232)
    RECOMMENDED_NEXT_CALIBRATION_TIME = TimestampProperty(16871424)
    EXTERNAL_CALIBRATION_LAST_LIMITED = BoolProperty(17428480)
    CALIBRATION_CURRENT_PASSWORD = StringProperty(17223680)
    CALIBRATION_NEW_PASSWORD = StringProperty(17227776)
    SYSTEM_CONFIGURATION_WEB_ACCESS = IntProperty(219504640, enum=AccessType)
    ADAPTER_TYPE = IntProperty(219332608, enum=AdapterType)
    MAC_ADDRESS = StringProperty(219168768)
    ADAPTER_MODE = IntProperty(219160576, enum=AdapterMode)
    TCP_IP_REQUEST_MODE = IntProperty(219172864, enum=IpAddressMode)
    TCP_IP_V4_ADDRESS = StringProperty(219181056)
    TCP_IP_V4_SUBNET = StringProperty(219189248)
    TCP_IP_V4_GATEWAY = StringProperty(219193344)
    TCP_IP_V4_DNS_SERVER = StringProperty(219197440)
    TCP_PREFERRED_LINK_SPEED = IntProperty(219213824, enum=LinkSpeed)
    TCP_CURRENT_LINK_SPEED = IntProperty(219222016, enum=LinkSpeed)
    TCP_PACKET_DETECTION = IntProperty(219258880, enum=PacketDetection)
    TCP_POLLING_INTERVAL = UnsignedIntProperty(219262976)
    IS_PRIMARY_ADAPTER = BoolProperty(219308032)
    ETHER_CAT_MASTER_ID = UnsignedIntProperty(219250688)
    ETHER_CAT_MASTER_REDUNDANCY = BoolProperty(219500544)
    WLAN_BSSID = StringProperty(219398144)
    WLAN_CURRENT_LINK_QUALITY = UnsignedIntProperty(219394048)
    WLAN_CURRENT_SSID = StringProperty(219377664)
    WLAN_CURRENT_CONNECTION_TYPE = IntProperty(219381760, enum=ConnectionType)
    WLAN_CURRENT_SECURITY_TYPE = IntProperty(219385856, enum=SecurityType)
    WLAN_CURRENT_EAP_TYPE = IntProperty(219389952, enum=EapType)
    WLAN_COUNTRY_CODE = IntProperty(219406336)
    WLAN_CHANNEL_NUMBER = UnsignedIntProperty(219410432)
    WLAN_CLIENT_CERTIFICATE = StringProperty(219422720)
    WLAN_SECURITY_IDENTITY = StringProperty(219414528)
    WLAN_SECURITY_KEY = StringProperty(219418624)
    SYSTEM_START_TIME = TimestampProperty(17108992)
    CURRENT_TIME = TimestampProperty(219279360)
    TIME_ZONE = StringProperty(219471872)
    USER_DIRECTED_SAFE_MODE_SWITCH = BoolProperty(219537408)
    CONSOLE_OUT_SWITCH = BoolProperty(219541504)
    IP_RESET_SWITCH = BoolProperty(219545600)
    NUMBER_OF_DISCOVERED_ACCESS_POINTS = UnsignedIntProperty(219365376)
    NUMBER_OF_EXPERTS = IntProperty(16891904)
    NUMBER_OF_SERVICES = IntProperty(17010688)
    NUMBER_OF_AVAILABLE_FIRMWARE_VERSIONS = IntProperty(17088512)
    NUMBER_OF_CPUS = IntProperty(17137664)
    NUMBER_OF_FANS = IntProperty(17174528)
    NUMBER_OF_POWER_SENSORS = IntProperty(17448960)
    NUMBER_OF_TEMPERATURE_SENSORS = IntProperty(17186816)
    NUMBER_OF_VOLTAGE_SENSORS = IntProperty(17149952)
    NUMBER_OF_USER_LED_INDICATORS = IntProperty(17281024)
    NUMBER_OF_USER_SWITCHES = IntProperty(17293312)


class IndexedResource(PropertyGroup):
    """Property group for indexed NI System Configuration resources."""

    SERVICE_TYPE = IndexedIntProperty(17014784, Resource.NUMBER_OF_SERVICES, enum=ServiceType)
    AVAILABLE_FIRMWARE_VERSION = IndexedStringProperty(
        17092608, Resource.NUMBER_OF_AVAILABLE_FIRMWARE_VERSIONS
    )
    WLAN_AVAILABLE_SSID = IndexedStringProperty(
        219336704, Resource.NUMBER_OF_DISCOVERED_ACCESS_POINTS
    )
    WLAN_AVAILABLE_BSSID = IndexedStringProperty(
        219443200, Resource.NUMBER_OF_DISCOVERED_ACCESS_POINTS
    )
    WLAN_AVAILABLE_CONNECTION_TYPE = IndexedIntProperty(
        219340800, Resource.NUMBER_OF_DISCOVERED_ACCESS_POINTS, enum=ConnectionType
    )
    WLAN_AVAILABLE_SECURITY_TYPE = IndexedIntProperty(
        219344896, Resource.NUMBER_OF_DISCOVERED_ACCESS_POINTS, enum=SecurityType
    )
    WLAN_AVAILABLE_LINK_QUALITY = IndexedUnsignedIntProperty(
        219353088, Resource.NUMBER_OF_DISCOVERED_ACCESS_POINTS
    )
    WLAN_AVAILABLE_CHANNEL_NUMBER = IndexedUnsignedIntProperty(
        219357184, Resource.NUMBER_OF_DISCOVERED_ACCESS_POINTS
    )
    WLAN_AVAILABLE_LINK_SPEED = IndexedIntProperty(
        219361280, Resource.NUMBER_OF_DISCOVERED_ACCESS_POINTS, enum=LinkSpeed
    )
    CPU_TOTAL_LOAD = IndexedUnsignedIntProperty(17141760, Resource.NUMBER_OF_CPUS)
    CPU_INTERRUPT_LOAD = IndexedUnsignedIntProperty(17145856, Resource.NUMBER_OF_CPUS)
    CPU_SPEED = IndexedUnsignedIntProperty(17309696, Resource.NUMBER_OF_CPUS)
    FAN_NAME = IndexedStringProperty(17178624, Resource.NUMBER_OF_FANS)
    FAN_READING = IndexedUnsignedIntProperty(17182720, Resource.NUMBER_OF_FANS)
    POWER_NAME = IndexedStringProperty(17453056, Resource.NUMBER_OF_POWER_SENSORS)
    POWER_READING = IndexedDoubleProperty(17457152, Resource.NUMBER_OF_POWER_SENSORS)
    POWER_UPPER_CRITICAL = IndexedDoubleProperty(17461248, Resource.NUMBER_OF_POWER_SENSORS)
    TEMPERATURE_NAME = IndexedStringProperty(17190912, Resource.NUMBER_OF_TEMPERATURE_SENSORS)
    TEMPERATURE_READING = IndexedDoubleProperty(16965632, Resource.NUMBER_OF_TEMPERATURE_SENSORS)
    TEMPERATURE_LOWER_CRITICAL = IndexedDoubleProperty(
        17195008, Resource.NUMBER_OF_TEMPERATURE_SENSORS
    )
    TEMPERATURE_UPPER_CRITICAL = IndexedDoubleProperty(
        17199104, Resource.NUMBER_OF_TEMPERATURE_SENSORS
    )
    VOLTAGE_NAME = IndexedStringProperty(17154048, Resource.NUMBER_OF_VOLTAGE_SENSORS)
    VOLTAGE_READING = IndexedDoubleProperty(17158144, Resource.NUMBER_OF_VOLTAGE_SENSORS)
    VOLTAGE_NOMINAL = IndexedDoubleProperty(17162240, Resource.NUMBER_OF_VOLTAGE_SENSORS)
    VOLTAGE_LOWER_CRITICAL = IndexedDoubleProperty(17166336, Resource.NUMBER_OF_VOLTAGE_SENSORS)
    VOLTAGE_UPPER_CRITICAL = IndexedDoubleProperty(17170432, Resource.NUMBER_OF_VOLTAGE_SENSORS)
    USER_LED_NAME = IndexedStringProperty(17285120, Resource.NUMBER_OF_USER_LED_INDICATORS)
    USER_SWITCH_NAME = IndexedStringProperty(17297408, Resource.NUMBER_OF_USER_SWITCHES)
    USER_SWITCH_STATE = IndexedIntProperty(
        17301504, Resource.NUMBER_OF_USER_SWITCHES, enum=SwitchState
    )
    USER_LED_STATE = IndexedIntProperty(
        17289216, Resource.NUMBER_OF_USER_LED_INDICATORS, enum=LedState
    )
    EXPERT_NAME = IndexedStringProperty(16900096, Resource.NUMBER_OF_EXPERTS)
    EXPERT_RESOURCE_NAME = IndexedStringProperty(16896000, Resource.NUMBER_OF_EXPERTS)
    EXPERT_USER_ALIAS = IndexedStringProperty(16904192, Resource.NUMBER_OF_EXPERTS)


class System(PropertyGroup):
    """Property group for NI System Configuration system properties."""

    DEVICE_CLASS = StringProperty(16941057)
    PRODUCT_ID = IntProperty(16941058)
    FILE_SYSTEM = IntProperty(16941060, enum=FileSystemMode)
    FIRMWARE_REVISION = StringProperty(16941061)
    IS_FACTORY_RESET_SUPPORTED = BoolProperty(16941067)
    IS_FIRMWARE_UPDATE_SUPPORTED = BoolProperty(16941068)
    IS_LOCKED = BoolProperty(16941069)
    IS_LOCKING_SUPPORTED = BoolProperty(16941070)
    IS_ON_LOCAL_SUBNET = BoolProperty(16941072)
    IS_RESTART_SUPPORTED = BoolProperty(16941076)
    MAC_ADDRESS = StringProperty(16941077)
    PRODUCT_NAME = StringProperty(16941078)
    OPERATING_SYSTEM = StringProperty(16941079)
    OPERATING_SYSTEM_VERSION = StringProperty(17100800)
    OPERATING_SYSTEM_DESCRIPTION = StringProperty(17104896)
    SERIAL_NUMBER = StringProperty(16941080)
    SYSTEM_STATE = StringProperty(16941082)
    MEMORY_PHYS_TOTAL = DoubleProperty(219480064)
    MEMORY_PHYS_FREE = DoubleProperty(219484160)
    MEMORY_LARGEST_BLOCK = DoubleProperty(219488256)
    MEMORY_VIRT_TOTAL = DoubleProperty(219492352)
    MEMORY_VIRT_FREE = DoubleProperty(219496448)
    PRIMARY_DISK_TOTAL = DoubleProperty(219291648)
    PRIMARY_DISK_FREE = DoubleProperty(219295744)
    # Implemented as a property on nisyscfg.Session
    # SYSTEM_RESOURCE_HANDLE = IntProperty(16941086, enum=ResourceHandle)
    IMAGE_DESCRIPTION = StringProperty(219516928)
    IMAGE_ID = StringProperty(219521024)
    IMAGE_TITLE = StringProperty(219525120)
    IMAGE_VERSION = StringProperty(219529216)
    INSTALLED_API_VERSION = StringProperty(16941087)
    IS_DST = BoolProperty(16941066)
    IS_RESTART_PROTECTED = BoolProperty(16941073)
    HALT_ON_ERROR = BoolProperty(16941074)
    REPOSITORY_LOCATION = StringProperty(16941084)
    SYSTEM_COMMENT = StringProperty(16941081)
    AUTO_RESTART_TIMEOUT = UnsignedIntProperty(16941085)
    DNS_SERVER = StringProperty(16941059)
    GATEWAY = StringProperty(16941062)
    HOSTNAME = StringProperty(16941063)
    IP_ADDRESS = StringProperty(16941064)
    IP_ADDRESS_MODE = IntProperty(16941065, enum=IpAddressMode)
    SUBNET_MASK = StringProperty(16941083)


class Filter(PropertyGroup):
    """Property group for NI System Configuration filter properties."""

    IS_DEVICE = BoolProperty(16781312)
    IS_CHASSIS = BoolProperty(16941056)
    SERVICE_TYPE = IntProperty(17014784, enum=ServiceType)
    CONNECTS_TO_BUS_TYPE = IntProperty(16785408, enum=BusType)
    CONNECTS_TO_LINK_NAME = StringProperty(16818176)
    PROVIDES_BUS_TYPE = IntProperty(16932864, enum=BusType)
    VENDOR_ID = UnsignedIntProperty(16789504)
    PRODUCT_ID = UnsignedIntProperty(16797696)
    SERIAL_NUMBER = StringProperty(16805888)
    IS_NI_PRODUCT = BoolProperty(16809984)
    IS_SIMULATED = BoolProperty(16814080)
    SLOT_NUMBER = IntProperty(16822272)
    HAS_DRIVER = IntProperty(16920576, enum=HasDriverType)
    IS_PRESENT = IntProperty(16924672, enum=IsPresentType)
    SUPPORTS_CALIBRATION = BoolProperty(16908288)
    SUPPORTS_FIRMWARE_UPDATE = BoolProperty(17080320)
    PROVIDES_LINK_NAME = StringProperty(16936960)
    EXPERT_NAME = StringProperty(16900096)
    RESOURCE_NAME = StringProperty(16896000)
    USER_ALIAS = StringProperty(16904192)


class _HasPropertyAccessor(Protocol):
    """Interface for objects that have a property accessor."""

    @property
    def property_accessor(self) -> "nisyscfg.properties.PropertyAccessor":
        """The property accessor."""
        ...


class Property(object):
    """Descriptor for accessing NI System Configuration properties."""

    __slots__ = ("_type_property",)

    def __init__(self, type_property: TypeProperty) -> None:
        """Initializes a Property descriptor."""
        self._type_property = type_property

    def __get__(self, instance: _HasPropertyAccessor, cls: type) -> object:
        """Get the property value from the instance."""
        return self._type_property.get(instance.property_accessor)

    def __set__(self, instance: _HasPropertyAccessor, value: object) -> None:
        """Set the property value on the instance."""
        return self._type_property.set(instance.property_accessor, value)

    def __delete__(self, instance: object) -> None:
        """Delete the property value (not implemented)."""
        raise NotImplementedError


class Expert(object):
    """Descriptor for accessing expert property groups in NI System Configuration."""

    def __init__(self, *property_groups: Type[PropertyGroup]) -> None:
        """Initializes an Expert descriptor."""

        class _ExpertPropertyBag(object):
            def __init__(self, property_bag: PropertyAccessor) -> None:
                self._property_accessor = property_bag

            @property
            def property_accessor(self) -> nisyscfg.properties.PropertyAccessor:
                """The property accessor."""
                return self._property_accessor

        self._expert = PropertyBag(*property_groups)(_ExpertPropertyBag)

    def __get__(self, instance: _HasPropertyAccessor, cls: type) -> object:
        """Get the expert property bag from the instance."""
        return self._expert(instance.property_accessor)

    def __set__(self, instance: object, value: object) -> None:
        """Setting expert property groups is not supported."""
        raise NotImplementedError

    def __delete__(self, instance: object) -> None:
        """Deleting expert property groups is not supported."""
        raise NotImplementedError


_T = TypeVar("_T")


class PropertyBag(object):
    """Container for property groups in NI System Configuration."""

    def __init__(self, *property_groups: Type[PropertyGroup], expert: Optional[str] = None) -> None:
        """Initializes a PropertyBag with the specified property groups."""
        self._property_groups = property_groups
        self._expert = expert

    def __call__(self, session: _T) -> _T:
        """Attach property groups to the session."""
        if self._expert:
            setattr(session, self._expert, Expert(*self._property_groups))
        else:
            for group in self._property_groups:
                for prop in dir(group):
                    type_property = getattr(group, prop)
                    if isinstance(type_property, TypeProperty):
                        setattr(session, prop.lower(), Property(type_property))
        return session
