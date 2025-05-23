"""Constants and enumerations."""

import typing
from enum import IntEnum, IntFlag


class _BaseEnum(IntEnum):
    @classmethod
    def from_param(cls, obj: typing.Any) -> int:
        return int(obj)


class _BaseFlag(IntFlag):
    @classmethod
    def from_param(cls, obj: typing.Any) -> int:
        return int(obj)


class IncludeCachedResults(_BaseEnum):
    """Specifies whether to include cached results."""

    NONE = 0
    """Only return systems discovered from a new scan.

    If you have added a system on a remote subnet to MAX, using NONE for the cached input will not
    return that system because it cannot be detected on the local subnet.
    """
    ONLY_IF_ONLINE = 1
    """Include previously discovered systems if they are online."""
    ALL = 3
    """Include all previously discovered systems, regardless of whether they are online or offline.
    """


class SystemNameFormat(_BaseEnum):
    """Specifies the preferred output format for systems on the network.

    The Initialize function accepts all of these formats.

    Note: In some cases this parameter may return a system that is not in the requested format. For
    example, if you request the default hostname(IP) but an unconfigured system is detected, that
    system is returned as IP(MAC).
    """

    HOSTNAME = 16
    """Includes only the hostname."""
    HOSTNAME_IP = 18
    """Includes the hostname and IP address."""
    HOSTNAME_MAC = 19
    """Includes the hostname and MAC address."""
    IP = 32
    """Includes only the IP address."""
    IP_HOSTNAME = 33
    """Includes the IP address and hostname."""
    IP_MAC = 35
    """Includes the IP address and MAC address."""
    MAC = 48
    """Includes only the MAC address."""
    MAC_HOSTNAME = 49
    """Includes the MAC address and hostname."""
    MAC_IP = 50
    """Includes the MAC address and IP address."""


class FileSystemMode(_BaseEnum):
    """Formats the primary hard drive into a user-selected file system.

    Note: Not all systems support all modes.
    """

    DEFAULT = 0
    """Formats the hard drive into the default format. The default is whatever format the existing
    target is already in.
    """
    FAT = 1
    """Formats the hard drive with the File Allocation Table (FAT) file system."""
    RELIANCE = 2
    """Formats the hard drive in Reliance format.

    Note: Reliance is a transactional file system, developed by Datalight, that is tolerant to
    crashes and power interruptions.
    """
    UBIFS = 16384
    """Formats the hard drive in UBIFS (Unsorted Block Image) format."""
    EXT4 = 32768
    """Formats the hard drive in Ext4 (fourth extended filesystem) format."""


class NetworkInterfaceSettings(_BaseEnum):
    """Specifies wether to preserve or reset network interface settings for a system."""

    RESET_PRIMARY_RESET_OTHERS = 0
    """Resets the primary network adapter to factory settings and disables all other network
    adapters.
    """
    PRESERVE_PRIMARY_RESET_OTHERS = 1
    """Preserves the primary network adapter settings and disables all other network adapters."""
    PRESERVE_PRIMARY_PRESERVE_OTHERS = 2
    """Preserves the primary network adapter settings and preserves all other network adapters."""
    PRESERVE_PRIMARY_APPLY_OTHERS = 3
    """Preserves the settings for the primary network adapter on the target and applies the settings
    from the image to all other network devices.
    """
    APPLY_PRIMARY_RESET_OTHERS = 4
    """Applies the settings from the image to the primary network adapter on the target and disables
    all other network adapters.
    """
    APPLY_PRIMARY_PRESERVE_OTHERS = 5
    """Applies the settings from the image to the primary network adapter on the target and
    preserves all other network adapters.
    """
    APPLY_PRIMARY_APPLY_OTHERS = 6
    """Applies all network settings from the image to all network adapters."""


class ComponentType(_BaseEnum):
    """Describes the type of the component."""

    STANDARD = 0
    """Standard visible component."""
    HIDDEN = 1
    """Hidden component."""
    SYSTEM = 2
    """Required system component (hidden package or base system image installed by the host)."""
    UNKNOWN = 3
    """Unknown component type."""
    STARTUP = 4
    """Start-up component."""
    IMAGE = 5
    """User-defined system image."""
    ESSENTIAL = 6
    """Required visible component."""
    SYSTEM_PACKAGE = 7
    """Base system image installed using a package from feeds on ni.com."""


class IncludeComponentTypes(_BaseEnum):
    """Allows inclusion of hidden software components in the system."""

    ALL_VISIBLE = 0
    """Specifies to return all visible software components. This includes all standard, startup, and
    essential components.
    """
    ALL_VISIBLE_AND_HIDDEN = 1
    """Specifies to return all visible and hidden software components."""
    ONLY_STANDARD = 2
    """Specifies to only return standard software components."""
    ONLY_STARTUP = 3
    """Specifies to only return components that are startup applications."""


class VersionSelectionMode(_BaseEnum):
    """Specifies the version selection mode for a software component."""

    HIGHEST = 0
    """Chooses the highest available version of the component."""
    EXACT = 1
    """Chooses the exact specified version."""


class ImportMode(_BaseEnum):
    """Specifies how to treat existing data at the destination."""

    MERGE_ITEMS = 0
    """Merges the source data in with any existing data at the destination"""
    DELETE_CONFIG_FIRST = 1048576
    """Replaces all configuration data at the destination with the source data."""
    PRESERVE_CONFLICT_ITEMS = 2097152
    """Preserves the original data. The destination wins by default in the case of overwrite
    conflicts.
    """


class ReportType(_BaseEnum):
    """Specifies the type of report to generate."""

    XML = 0
    """Generates a report in XML."""
    HTML = 1
    """Generates a report in HTML."""
    TECHNICAL_SUPPORT_ZIP = 2
    """Generates a report in Technical Support format for sending to NI support staff."""


class BusType(_BaseEnum):
    """ "Specifies the bus type."""

    BUILT_IN = 0
    """Built-in or system bus type."""
    PCI_PXI = 1
    """PCI or PXI bus type."""
    USB = 2
    """USB bus type."""
    GPIB = 3
    """GPIB/IEEE 488.2 bus type."""
    VXI = 4
    """VXI bus type."""
    SERIAL = 5
    """Serial bus type."""
    TCP_IP = 6
    """TCP/IP bus type."""
    COMPACT_RIO = 7
    """Compact RIO bus type."""
    SCXI = 8
    """SCXI bus type."""
    COMPACT_DAQ = 9
    """Compact DAQ bus type."""
    SWITCH_BLOCK = 10
    """Switch block bus type."""
    SCC = 11
    """SCC bus type."""
    FIRE_WIRE = 12
    """FireWire bus type."""
    ACCESSORY = 13
    """Accessory bus type."""
    CAN = 14
    """CAN bus type."""
    SWITCH_BLOCK_DEVICE = 15
    """Switch block device bus type."""
    SLSC = 16
    """SLSC bus type."""


class HasDriverType(_BaseEnum):
    """Specifies whether there is an installed driver for this device."""

    UNKNOWN = -1
    """The driver status is unknown."""
    NOT_INSTALLED = 0
    """The driver is not installed."""
    INSTALLED = 1
    """The driver is installed."""


class IsPresentType(_BaseEnum):
    """Specifies whether this resource is currently present."""

    INITIALIZING = -2
    """The resource is initializing."""
    UNKNOWN = -1
    """The resource status is unknown."""
    NOT_PRESENT = 0
    """The resource is not present."""
    PRESENT = 1
    """The resource is present."""


class IpAddressMode(_BaseEnum):
    """Specifies whether the remote resource its IP address statically or dynamically.

    Not all adapters support all modes. Static and DHCP/Link-Local modes are most commonly
    supported. If the system or device has multiple adapters, this property applies only to the
    primary network card.
    """

    STATIC = 1
    """The IP address is statically assigned."""
    DHCP_OR_LINK_LOCAL = 2
    """The IP address is assigned using DHCP or Link-Local addressing."""
    LINK_LOCAL_ONLY = 4
    """The IP address is assigned using Link-Local addressing only."""
    DHCP_ONLY = 8
    """The IP address is assigned using DHCP only."""


class Bool(_BaseEnum):
    """Specifies a boolean value."""

    FALSE = 0
    """False."""
    TRUE = 1
    """True."""


class Locale(_BaseEnum):
    """Specifies the Windows language ID."""

    DEFAULT = 0
    """Automatically chooses the language based on local Windows settings."""
    CHINESE_SIMPLIFIED = 2052
    """Simplified Chinese - People's Republic of China."""
    ENGLISH = 1033
    """English - United States."""
    FRENCH = 1036
    """French - France."""
    GERMAN = 1031
    """German - Germany."""
    JAPANESE = 1041
    """Japanese - Japan."""
    KOREAN = 1042
    """Korean - Korea."""


class FilterMode(_BaseEnum):
    """Specifies the filter mode for find_hardware."""

    MATCH_VALUES_ALL = 1
    """Includes all of the properties specified in the input filter."""
    MATCH_VALUES_ANY = 2
    """Includes any of the properties specified in the input filter."""
    MATCH_VALUES_NONE = 3
    """Includes none of the properties specified in the input filter."""
    ALL_PROPERTIES_EXIST = 4
    """Includes all of the properties specified in the input filter, regardless of the value of each
    property.
    """


class ServiceType(_BaseEnum):
    """Specifies the service type for the resource.

    Note: Not all resources have a service.
    """

    MDNS_NI_TCP = 0
    """NI Network Resource."""
    MDNS_NI_REALTIME = 1
    """NI Real-Time."""
    MDNS_NI_SYSAPI = 2
    """NI System Configuration."""
    MDNS_NI_HTTP = 3
    """NI Web Interface."""
    LOCAL_SYSTEM = 4
    """Local System."""
    LOCAL_NET_INTERFACE = 5
    """Local Network Interface."""
    LOCAL_TIME_KEEPER = 6
    """Local Time Keeper."""
    LOCAL_TIME_SOURCE = 7
    """Local Time Source."""
    MDNS_LXI = 8
    """LXI Instrument."""
    LOCAL_FPGA = 9
    """Local FPGA."""
    DEVICE_NET_INTERFACE = 10
    """DeviceNet Interface."""


class AdapterType(_BaseEnum):
    """Specifies the type of network adapter."""

    ETHERNET = 1
    """Ethernet adapter."""
    WLAN = 2
    """Wireless LAN adapter."""


class AdapterMode(_BaseEnum):
    """Specifies the mode of the network adapter."""

    DISABLED = 1
    """The network adapter is disabled."""
    TCP_IP_ETHERNET = 2
    """The network adapter is in TCP/IP Ethernet mode."""
    DETERMINISTIC = 4
    """The network adapter is in deterministic mode."""
    ETHER_CAT = 8
    """The network adapter is in EtherCAT mode."""
    TCP_IP_WLAN = 32
    """The network adapter is in TCP/IP WLAN mode."""
    TCP_IP_ACCESS_POINT = 64
    """The network adapter is in TCP/IP Access Point mode."""


class LinkSpeed(_BaseEnum):
    """Specifies the link speed of the network adapter.

    Note: Not all adapters support all link speeds.
    """

    NONE = 0
    """The link speed is not specified."""
    AUTO = 1
    """The link speed is automatically negotiated."""
    TEN_MEGABIT_HALF = 2
    """The link speed is 10 Mbps in half-duplex mode."""
    TEN_MEGABIT_FULL = 4
    """The link speed is 10 Mbps in full-duplex mode."""
    HUNDRED_MEGABIT_HALF = 8
    """The link speed is 100 Mbps in half-duplex mode."""
    HUNDRED_MEGABIT_FULL = 16
    """The link speed is 100 Mbps in full-duplex mode."""
    GIGABIT_HALF = 32
    """The link speed is 1 Gbps in half-duplex mode."""
    GIGABIT_FULL = 64
    """The link speed is 1 Gbps in full-duplex mode."""
    WLAN80211A = 131072
    """The link speed is 802.11a."""
    WLAN80211B = 262144
    """The link speed is 802.11b."""
    WLAN80211G = 524288
    """The link speed is 802.11g."""
    WLAN80211N = 1048576
    """The link speed is 802.11n."""
    WLAN80211N_5GHZ = 2097152
    """The link speed is 802.11n in 5 GHz mode."""


class PacketDetection(_BaseEnum):
    """Specifies the packet detection mode for the network adapter.

    Note: Not all adapters support all packet detection modes.
    """

    NONE = 0
    """The packet detection mode is not specified."""
    LINE_INTERRUPT = 1
    """The packet detection mode is line interrupt."""
    POLLING = 2
    """The packet detection mode is polling."""
    SIGNALED_INTERRUPT = 4
    """The packet detection mode is signaled interrupt (MSI)."""


class ConnectionType(_BaseEnum):
    """Specifies the connection type for the network adapter.

    Note: Not all adapters support all connection types.
    """

    NONE = 0
    """The connection type is not specified."""
    INFRASTRUCTURE = 1
    """The connection type is infrastructure."""
    AD_HOC = 2
    """The connection type is ad-hoc."""


class SecurityType(_BaseEnum):
    """Specifies the security type for the network adapter.

    Note: Not all adapters support all security types.
    """

    NONE = 0
    """The security type is not specified."""
    NOT_SUPPORTED = 1
    """The security type is not supported."""
    OPEN = 2
    """The security type is open."""
    WEP = 4
    """The security type is WEP."""
    WPA_PSK = 8
    """The security type is WPA-PSK."""
    WPA_EAP = 16
    """The security type is WPA-EAP."""
    WPA2_PSK = 32
    """The security type is WPA2-PSK."""
    WPA2_EAP = 64
    """The security type is WPA2-EAP."""


class EapType(_BaseEnum):
    """Specifies the authentication type of the access point."""

    NONE = 0
    """No authentication type."""
    EAP_TLS = 1
    """EAP-TLS."""
    EAP_TTLS = 2
    """EAP-TTLS."""
    EAP_FAST = 4
    """EAP-FAST."""
    LEAP = 8
    """LEAP."""
    PEAP = 16
    """PEAP."""


class FirmwareStatus(_BaseEnum):
    """Specifies the firmware status of the system.

    Negative firmware states are in-progress; the user should continue polling.
    Non-negative firmware states are terminal; no update operation is in progress.
    """

    READY_PENDING_AUTO_RESTART = -4
    """The system is ready and pending an automatic restart."""
    VERIFYING_NEW_IMAGE = -3
    """The system is verifying the new image."""
    WRITING_FLASHING_NEW_IMAGE = -2
    """The system is writing or flashing the new image."""
    UPDATE_MODE_WAITING_FOR_IMAGE = -1
    """The system is waiting for the new image to be loaded."""
    CORRUPT_CANNOT_RUN = 0
    """The system is corrupt and cannot run."""
    NONE_INSTALLED = 1
    """The image was not installed."""
    INSTALLED_NORMAL_OPERATION = 2
    """The image was installed and the system is in normal operation."""
    READY_PENDING_USER_RESTART = 3
    """The system is ready and pending a user restart."""
    READY_PENDING_USER_ACTION = 4
    """The system is ready and pending user action."""
    UPDATE_ATTEMPT_FAILED = 5
    """The update attempt failed."""


class DeleteValidationMode(_BaseEnum):
    """Specifies the conditions under which to delete the specified resource."""

    VALIDATE_BUT_DO_NOT_DELETE = -1
    """Verify whether the resource can be deleted and whether it has dependencies."""
    DELETE_IF_NO_DEPENDENCIES_EXIST = 0
    """Delete the resource if no dependencies exist."""
    DELETE_ITEM_AND_ANY_DEPENDENCIES = 1
    """Delete the resource and any dependencies."""
    DELETE_ITEM_BUT_KEEP_DEPENDENCIES = 2
    """Delete the resource but keep any dependencies."""


class AccessType(_BaseEnum):
    """Specifies the access type for the resource."""

    LOCAL_ONLY = 0
    """The resource is only accessible locally."""
    LOCAL_AND_REMOTE = 1
    """The resource is accessible locally and remotely."""


class LedState(_BaseEnum):
    """Specifies the state of user LED indicators."""

    OFF = 0
    """The LED is off."""
    SOLID_GREEN = 1
    """The LED is solid green."""
    SOLID_YELLOW = 2
    """The LED is solid yellow."""
    SOLID_RED = 16
    """The LED is solid red."""
    BLINKING_GREEN = 4
    """The LED is blinking green."""
    BLINKING_YELLOW = 8
    """The LED is blinking yellow."""
    BLINKING_RED = 32
    """The LED is blinking red."""


class SwitchState(_BaseEnum):
    """Specifies the current state for each user switch.

    For a push-button switch, the disabled (open) state is in the up position and the enabled
    (closed) state is in the down position.
    """

    DISABLED = 0
    """The switch is disabled (open)."""
    ENABLED = 1
    """The switch is enabled (closed)."""


class FirmwareUpdateMode(_BaseEnum):
    """Specifies the mode for performing firmware updates."""

    NONE = 0
    """This resource does not support firmware updates."""
    MANUAL = 1
    """Firmware updates for this resource must be user-initiated. The driver may fail to initialize
    if it is incompatible with the firmware version currently on the device.
    """
    DRIVER_MANAGED = 2
    """The driver for this resource will automatically manage the firmware version, upgrading or
    downgrading it as required. User-initiated attempts to update the firmware from this state will
    fail.
    """


class ModuleProgramMode(_BaseEnum):
    """Specifies the mode for programming a cRIO module."""

    NONE = 0
    """This item is not a module or does not support program modes."""
    REALTIME_CPU = 1
    """This module is controlled by a real-time application running on the CPU."""
    REALTIME_SCAN = 2
    """This module is controlled by the NI Scan Engine, and its data is available to real-time
    applications.
    """
    LABVIEW_FPGA = 4
    """This module is controlled by a LabVIEW FPGA bitfile."""


class PropertyType(_BaseEnum):
    """Specifies the type of property."""

    BOOL = 1
    """Boolean property."""
    INT = 2
    """Integer property."""
    UNSIGNED_INT = 3
    """Unsigned integer property."""
    DOUBLE = 4
    """Double floating-point property."""
    STRING = 6
    """String property."""
    TIMESTAMP = 7
    """Timestamp property."""
