from nisyscfg.enums import (
    AccessType,
    AdapterMode,
    AdapterType,
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
    SecurityType,
    ServiceType,
    SwitchState,
)


class Property(object):
    __slots__ = ()


class TypeProperty(Property):

    __slots__ = '_id', '_enum', '_readable', '_writeable'

    def __init__(self, id, enum=None, readable=True, writeable=True):
        self._id = id
        self._enum = enum
        self._readable = readable
        self._writeable = writeable


class BoolProperty(TypeProperty):

    __slots__ = ()

    def get(self, bag):
        value = bag.get_bool_property(self._id)
        if self._enum:
            return self._enum(value)
        return value

    def set(self, bag, value):
        bag.set_bool_property(self._id, value)


class IntProperty(TypeProperty):

    __slots__ = ()

    def get(self, bag):
        value = bag.get_int_property(self._id)
        if self._enum:
            return self._enum(value)
        return value

    def set(self, bag, value):
        bag.set_int_property(self._id, value)


class UnsignedIntProperty(TypeProperty):

    __slots__ = ()

    def get(self, bag):
        value = bag.get_unsigned_int_property(self._id)
        if self._enum:
            return self._enum(value)
        return value

    def set(self, bag, value):
        bag.set_unsigned_int_property(self._id, value)


class BitmaskProperty(TypeProperty):

    __slots__ = ()

    def get(self, bag):
        value = bag.get_unsigned_int_property(self._id)
        if self._enum:
            return [mask for mask in self._enum if value & mask]
        return [value]


class DoubleProperty(TypeProperty):

    __slots__ = ()

    def get(self, bag):
        return bag.get_double_property(self._id)

    def set(self, bag, value):
        bag.set_double_property(self._id, value)


class StringProperty(TypeProperty):

    __slots__ = ()

    def get(self, bag):
        return bag.get_string_property(self._id)

    def set(self, bag, value):
        bag.set_string_property(self._id, value)


class TimestampProperty(TypeProperty):

    __slots__ = ()

    def get(self, bag):
        raise NotImplementedError

    def set(self, bag, value):
        raise NotImplementedError


class IndexedPropertyItems(object):
    def __init__(self, bag, tag):
        self._bag = bag
        self._tag = tag

    def __getitem__(self, key):
        try:
            key + 1
        except TypeError:
            raise KeyError(key)
        if key >= 0 and key < len(self):
            return self._tag.get_index(self._bag, key)
        raise KeyError(key)

    def __len__(self):
        if not hasattr(self, '_len'):
            self._len = self._tag.count_property.get(self._bag)
        return self._len

    def __iter__(self):
        class IndexedPropertyItemsIter(object):

            __slots__ = '_properties', '_index'

            def __init__(self, properties):
                self._properties = properties
                self._index = -1

            def __next__(self):
                self._index += 1
                if self._index == len(self._properties):
                    raise StopIteration()
                return self._properties[self._index]

            def next(self):
                return self.__next__()

        return IndexedPropertyItemsIter(self)


class IndexedProperty(Property):

    __slots__ = '_id', '_count_property', '_enum', '_readable', '_writeable'

    def __init__(self, id, count_property, enum=None, readable=True, writeable=True):
        self._id = id
        self._count_property = count_property
        self._enum = enum
        self._readable = readable
        self._writeable = writeable

    @property
    def count_property(self):
        return self._count_property

    def get(self, bag):
        return IndexedPropertyItems(bag, self)


class IndexedBoolProperty(IndexedProperty):

    __slots__ = ()

    def get_index(self, bag, index):
        value = bag.get_indexed_bool_property(self._id, index)
        if self._enum:
            return self._enum(value)
        return value


class IndexedIntProperty(IndexedProperty):

    __slots__ = ()

    def get_index(self, bag, index):
        value = bag.get_indexed_int_property(self._id, index)
        if self._enum:
            return self._enum(value)
        return value


class IndexedUnsignedIntProperty(IndexedProperty):

    __slots__ = ()

    def get_index(self, bag, index):
        value = bag.get_indexed_unsigned_int_property(self._id, index)
        if self._enum:
            return self._enum(value)
        return value


class IndexedDoubleProperty(IndexedProperty):

    __slots__ = ()

    def get_index(self, bag, index):
        return bag.get_indexed_double_property(self._id, index)


class IndexedStringProperty(IndexedProperty):

    __slots__ = ()

    def get_index(self, bag, index):
        return bag.get_indexed_string_property(self._id, index)


class IndexedTimestampProperty(IndexedProperty):

    __slots__ = ()

    def get_index(self, bag, index):
        raise NotImplementedError


class Resource(object):
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
    SYS_CFG_ACCESS = IntProperty(219504640, enum=AccessType)
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


class IndexedResource(object):
    SERVICE_TYPE = IndexedIntProperty(17014784, Resource.NUMBER_OF_SERVICES, enum=ServiceType)
    AVAILABLE_FIRMWARE_VERSION = IndexedStringProperty(17092608, Resource.NUMBER_OF_AVAILABLE_FIRMWARE_VERSIONS)
    WLAN_AVAILABLE_SSID = IndexedStringProperty(219336704, Resource.NUMBER_OF_DISCOVERED_ACCESS_POINTS)
    WLAN_AVAILABLE_BSSID = IndexedStringProperty(219443200, Resource.NUMBER_OF_DISCOVERED_ACCESS_POINTS)
    WLAN_AVAILABLE_CONNECTION_TYPE = IndexedIntProperty(219340800, Resource.NUMBER_OF_DISCOVERED_ACCESS_POINTS, enum=ConnectionType)
    WLAN_AVAILABLE_SECURITY_TYPE = IndexedIntProperty(219344896, Resource.NUMBER_OF_DISCOVERED_ACCESS_POINTS, enum=SecurityType)
    WLAN_AVAILABLE_LINK_QUALITY = IndexedUnsignedIntProperty(219353088, Resource.NUMBER_OF_DISCOVERED_ACCESS_POINTS)
    WLAN_AVAILABLE_CHANNEL_NUMBER = IndexedUnsignedIntProperty(219357184, Resource.NUMBER_OF_DISCOVERED_ACCESS_POINTS)
    WLAN_AVAILABLE_LINK_SPEED = IndexedIntProperty(219361280, Resource.NUMBER_OF_DISCOVERED_ACCESS_POINTS, enum=LinkSpeed)
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
    TEMPERATURE_LOWER_CRITICAL = IndexedDoubleProperty(17195008, Resource.NUMBER_OF_TEMPERATURE_SENSORS)
    TEMPERATURE_UPPER_CRITICAL = IndexedDoubleProperty(17199104, Resource.NUMBER_OF_TEMPERATURE_SENSORS)
    VOLTAGE_NAME = IndexedStringProperty(17154048, Resource.NUMBER_OF_VOLTAGE_SENSORS)
    VOLTAGE_READING = IndexedDoubleProperty(17158144, Resource.NUMBER_OF_VOLTAGE_SENSORS)
    VOLTAGE_NOMINAL = IndexedDoubleProperty(17162240, Resource.NUMBER_OF_VOLTAGE_SENSORS)
    VOLTAGE_LOWER_CRITICAL = IndexedDoubleProperty(17166336, Resource.NUMBER_OF_VOLTAGE_SENSORS)
    VOLTAGE_UPPER_CRITICAL = IndexedDoubleProperty(17170432, Resource.NUMBER_OF_VOLTAGE_SENSORS)
    USER_LED_NAME = IndexedStringProperty(17285120, Resource.NUMBER_OF_USER_LED_INDICATORS)
    USER_SWITCH_NAME = IndexedStringProperty(17297408, Resource.NUMBER_OF_USER_SWITCHES)
    USER_SWITCH_STATE = IndexedIntProperty(17301504, Resource.NUMBER_OF_USER_SWITCHES, enum=SwitchState)
    USER_LED_STATE = IndexedIntProperty(17289216, Resource.NUMBER_OF_USER_LED_INDICATORS, enum=LedState)
    EXPERT_NAME = IndexedStringProperty(16900096, Resource.NUMBER_OF_EXPERTS)
    EXPERT_RESOURCE_NAME = IndexedStringProperty(16896000, Resource.NUMBER_OF_EXPERTS)
    EXPERT_USER_ALIAS = IndexedStringProperty(16904192, Resource.NUMBER_OF_EXPERTS)


class System(object):
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
    # TODO(tkrebes): Implement
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


class Filter(object):
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
