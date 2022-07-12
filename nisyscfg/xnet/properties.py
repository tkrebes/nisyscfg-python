from nisyscfg.enums import Bool
from nisyscfg.properties import (
    StringProperty,
    UnsignedIntProperty,
    IntProperty,
    PropertyGroup,
)
from nisyscfg.xnet.enums import (
    EnetPortMode,
    EnetPhyState,
    Blink,
    Protocol,
    CanTransceiverCapability,
    DongleId,
    DongleState,
    EnetLinkSpeed,
    EnetJumboFrames,
    EnetInterruptModeration,
    EnetSleepCapability,
    EnetPhyPowerMode
)


class Resource(PropertyGroup):
    # Read-only device properties
    NUMBER_OF_PORTS = UnsignedIntProperty(167780352)
    IP_STACK_INFO_JSON = StringProperty(167882752)
    IP_STACK_INFO_TEXT = StringProperty(167886848)

    # Read-only port properties
    PORT_NUMBER = UnsignedIntProperty(167845888)
    PROTOCOL = UnsignedIntProperty(167796737, Protocol)
    CAN_TERMINATION_CAPABILITY = UnsignedIntProperty(167849984, Bool)
    CAN_TRANSCEIVER_CAPABILITY = UnsignedIntProperty(167792641, CanTransceiverCapability)
    DONGLE_ID = UnsignedIntProperty(167813120, DongleId)
    DONGLE_STATE = UnsignedIntProperty(167809024, DongleState)

    # Write-only port properties
    BLINK = UnsignedIntProperty(167817216, Blink)

    # Read-only Automotive Ethernet port properties
    ENET_MAC_ADDR = StringProperty(167841792)
    ENET_IP_V4_ADDR = StringProperty(167854080)
    ENET_OS_ADAPTER_NAME = StringProperty(167858176)
    ENET_OS_ADAPTER_DESC = StringProperty(167862272)
    ENET_LINK_SPEED = UnsignedIntProperty(167874560, EnetLinkSpeed)
    ENET_SLEEP_CAPABILITY = UnsignedIntProperty(167911424, EnetSleepCapability)
    ENET_PHY_POWER_MODE = UnsignedIntProperty(167915520, EnetPhyPowerMode)

    # Read/Write Automotive Ethernet port properties
    ENET_PHY_STATE = UnsignedIntProperty(167837696, EnetPhyState)
    ENET_PORT_MODE = UnsignedIntProperty(167833600, EnetPortMode)
    ENET_LINK_SPEED_CONFIGURED = UnsignedIntProperty(167866368, EnetLinkSpeed)
    ENET_JUMBO_FRAMES = UnsignedIntProperty(167903232, EnetJumboFrames)
    ENET_INTERRUPT_MODERATION = IntProperty(167878656, EnetInterruptModeration)
    ENET_SLEEP_CAPABILITY_CONFIGURED = UnsignedIntProperty(167907328, EnetSleepCapability)


class Filter(PropertyGroup):
    # Write-only device properties
    NUMBER_OF_PORTS = UnsignedIntProperty(167780352)

    # Write-only port properties
    PORT_NUMBER = UnsignedIntProperty(167845888)
    PROTOCOL = UnsignedIntProperty(167796737, Protocol)
    CAN_TERMINATION_CAPABILITY = UnsignedIntProperty(167849984, Bool)
    CAN_TRANSCEIVER_CAPABILITY = UnsignedIntProperty(167792641, CanTransceiverCapability)
    DONGLE_ID = UnsignedIntProperty(167813120, DongleId)

    # Write-only Automotive Ethernet port properties
    ENET_PHY_STATE = UnsignedIntProperty(167837696, EnetPhyState)
    ENET_PORT_MODE = UnsignedIntProperty(167833600, EnetPortMode)
    ENET_LINK_SPEED_CONFIGURED = UnsignedIntProperty(167866368, EnetLinkSpeed)
