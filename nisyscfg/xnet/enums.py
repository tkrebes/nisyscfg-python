from nisyscfg.enums import BaseEnum


class IntferfaceEnetPortMode(BaseEnum):
    DIRECT = 0
    TAP = 1


class IntferfaceEnetPhyState(BaseEnum):
    SLAVE = 0
    MASTER = 1


class IntferfaceBlink(BaseEnum):
    DISABLE = 0
    ENABLE = 1


class IntferfaceProtocol(BaseEnum):
    CAN = 0
    FLEXRAY = 1
    LIN = 2
    UNKNOWN = -2


class IntferfaceCanTransceiverCapability(BaseEnum):
    HS = 0
    LS = 1
    XS = 3
    XS_WITH_HS_OR_LS = 4


class IntferfaceDongleId(BaseEnum):
    LS_CAN = 1
    HS_CAN = 2
    SW_CAN = 3
    XS_CAN = 4
    LIN = 6
    DONGLELESS_DESIGN = 13
    UNKNOWN = 14


class IntferfaceDongleState(BaseEnum):
    NO_DONGLE_NO_EXTERNAL_POWER = 1
    NO_DONGLE_HAS_EXTERNAL_POWER = 2
    HAS_DONGLE_NO_EXTERNAL_POWER = 3
    READY = 4
    BUSY = 5
    COMM_ERROR = 13
    OVERCURRENT = 14


class IntferfaceEnetLinkSpeed(BaseEnum):
    LINK_DOWN = 0
    HUNDRED_MEGABIT = 1
