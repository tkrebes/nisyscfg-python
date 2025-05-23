"""XNET-specific enums for hardware resource and property configuration."""

from nisyscfg.enums import _BaseEnum


class EnetPortMode(_BaseEnum):
    """Automotive Ethernet port mode enumeration."""

    DIRECT = 0
    TAP = 1


class EnetPhyState(_BaseEnum):
    """Automotive Ethernet PHY state enumeration."""

    SLAVE = 0
    MASTER = 1
    AUTO = 2


class Blink(_BaseEnum):
    """Blink LED state enumeration for XNET ports."""

    DISABLE = 0
    ENABLE = 1


class Protocol(_BaseEnum):
    """Protocol type enumeration for XNET ports."""

    CAN = 0
    FLEXRAY = 1
    LIN = 2
    ETHERNET = 3
    UNKNOWN = 0xFFFFFFFE


class CanTransceiverCapability(_BaseEnum):
    """CAN transceiver capability enumeration."""

    HS = 0
    LS = 1
    XS = 3
    XS_WITH_HS_OR_LS = 4
    UNKNOWN = 0xFFFFFFFF


class DongleId(_BaseEnum):
    """Dongle ID enumeration for XNET ports."""

    LS_CAN = 1
    HS_CAN = 2
    SW_CAN = 3
    XS_CAN = 4
    LIN = 6
    DONGLELESS_DESIGN = 13
    UNKNOWN = 14


class DongleState(_BaseEnum):
    """Dongle state enumeration for XNET ports."""

    NO_DONGLE_NO_EXTERNAL_POWER = 1
    NO_DONGLE_HAS_EXTERNAL_POWER = 2
    HAS_DONGLE_NO_EXTERNAL_POWER = 3
    READY = 4
    BUSY = 5
    COMM_ERROR = 13
    OVERCURRENT = 14


class EnetLinkSpeed(_BaseEnum):
    """Automotive Ethernet link speed enumeration."""

    LINK_DOWN = 0
    HUNDRED_MEGABIT = 1
    GIGABIT = 2


class EnetJumboFrames(_BaseEnum):
    """Automotive Ethernet jumbo frames setting enumeration."""

    DISABLE = 0
    ENABLE_9018_BYTES = 1


class EnetInterruptModeration(_BaseEnum):
    """Automotive Ethernet interrupt moderation enumeration."""

    OFF = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class EnetSleepCapability(_BaseEnum):
    """Automotive Ethernet sleep capability enumeration."""

    DISABLED_OR_NOT_AVAILABLE = 0
    ENABLED = 1


class EnetPhyPowerMode(_BaseEnum):
    """Automotive Ethernet PHY power mode enumeration."""

    NORMAL = 0
    SLEEP = 1
