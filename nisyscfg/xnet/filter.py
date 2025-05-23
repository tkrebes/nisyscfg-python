"""Documentation for XNET Filter properties."""

from typing import Protocol, Union

import nisyscfg.enums
import nisyscfg.xnet.enums


class Filter(Protocol):
    """XNET Filter properties."""

    number_of_ports: int
    """Number of ports on the device."""
    port_number: int
    """Port number."""
    protocol: Union[nisyscfg.xnet.enums.Protocol, int]
    """Protocol type."""
    can_termination_capability: Union[nisyscfg.enums.Bool, int]
    """CAN termination capability."""
    can_transceiver_capability: Union[nisyscfg.xnet.enums.CanTransceiverCapability, int]
    """CAN transceiver capability."""
    dongle_id: Union[nisyscfg.xnet.enums.DongleId, int]
    """Dongle ID."""
    enet_phy_state: Union[nisyscfg.xnet.enums.EnetPhyState, int]
    """Automotive Ethernet PHY state."""
    enet_port_mode: Union[nisyscfg.xnet.enums.EnetPortMode, int]
    """Automotive Ethernet port mode."""
    enet_link_speed_configured: int
    """Configured Automotive Ethernet link speed."""
