from nisyscfg.enums import Bool
from nisyscfg.properties import (
    UnsignedIntProperty,
    StringProperty,
)
from nisyscfg.xnet.enums import (
    IntferfaceEnetPortMode,
    IntferfaceEnetPhyState,
    IntferfaceBlink,
    IntferfaceProtocol,
    IntferfaceCanTransceiverCapability,
    IntferfaceDongleId,
    IntferfaceDongleState,
    IntferfaceEnetLinkSpeed,
)


class Resource(object):
    # Read-only device properties
    NUMBER_OF_PORTS = UnsignedIntProperty(167780352)

    # Read-only port properties
    PORT_NUMBER = UnsignedIntProperty(167845888)
    PROTOCOL = UnsignedIntProperty(167796737, IntferfaceProtocol)
    CAN_TERMINATION_CAPABILITY = UnsignedIntProperty(167849984, Bool)
    CAN_TRANSCEIVER_CAPABILITY = UnsignedIntProperty(167792641, IntferfaceCanTransceiverCapability)
    DONGLE_ID = UnsignedIntProperty(167813120, IntferfaceDongleId)
    DONGLE_STATE = UnsignedIntProperty(167809024, IntferfaceDongleState)

    # Write-only port properties
    BLINK = UnsignedIntProperty(167817216, IntferfaceBlink)

    # Read-only Automotive Ethernet port properties
    ENET_MAC_ADDR = StringProperty(167841792)
    ENET_IP_V4_ADDR = StringProperty(167854080)
    ENET_OS_ADAPTER_NAME = StringProperty(167858176)
    ENET_OS_ADAPTER_DESC = StringProperty(167862272)
    ENET_LINK_SPEED = UnsignedIntProperty(167874560, IntferfaceEnetLinkSpeed)
    ENET_LINK_SPEED_CONFIGURED = UnsignedIntProperty(167866368, IntferfaceEnetLinkSpeed)

    # Read/Write Automotive Ethernet port properties
    ENET_PHY_STATE = UnsignedIntProperty(167837696, IntferfaceEnetPhyState)
    ENET_PORT_MODE = UnsignedIntProperty(167833600, IntferfaceEnetPortMode)


class Filter(object):
    # Write-only device properties
    NUMBER_OF_PORTS = UnsignedIntProperty(167780352)

    # Write-only port properties
    PORT_NUMBER = UnsignedIntProperty(167845888)
    PROTOCOL = UnsignedIntProperty(167796737, IntferfaceProtocol)
    CAN_TERMINATION_CAPABILITY = UnsignedIntProperty(167849984, Bool)
    CAN_TRANSCEIVER_CAPABILITY = UnsignedIntProperty(167792641, IntferfaceCanTransceiverCapability)

    # Write-only Automotive Ethernet port properties
    ENET_PHY_STATE = UnsignedIntProperty(167837696, IntferfaceEnetPhyState)
    ENET_PORT_MODE = UnsignedIntProperty(167833600, IntferfaceEnetPortMode)
    ENET_LINK_SPEED_CONFIGURED = UnsignedIntProperty(167866368, IntferfaceEnetLinkSpeed)
