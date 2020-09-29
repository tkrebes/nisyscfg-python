from nisyscfg.enums import BaseEnum


class EnetPortMode(BaseEnum):
    DIRECT = 0
    TAP = 1


class EnetPhyState(BaseEnum):
    SLAVE = 0
    MASTER = 1


class Blink(BaseEnum):
    DISABLE = 0
    ENABLE = 1


class Protocol(BaseEnum):
    CAN = 0
    FLEXRAY = 1
    LIN = 2
    UNKNOWN = -2


class CanTransceiverCapability(BaseEnum):
    HS = 0
    LS = 1
    XS = 3
    XS_WITH_HS_OR_LS = 4


class DongleId(BaseEnum):
    LS_CAN = 1
    HS_CAN = 2
    SW_CAN = 3
    XS_CAN = 4
    LIN = 6
    DONGLELESS_DESIGN = 13
    UNKNOWN = 14


class DongleState(BaseEnum):
    NO_DONGLE_NO_EXTERNAL_POWER = 1
    NO_DONGLE_HAS_EXTERNAL_POWER = 2
    HAS_DONGLE_NO_EXTERNAL_POWER = 3
    READY = 4
    BUSY = 5
    COMM_ERROR = 13
    OVERCURRENT = 14


class EnetLinkSpeed(BaseEnum):
    LINK_DOWN = 0
    HUNDRED_MEGABIT = 1
    GIGABIT = 2


class EnetJumboFrames(BaseEnum):
    DISABLE = 0
    ENABLE_9018_BYTES = 1


class EnetInterruptModeration(BaseEnum):
    OFF = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
