"""Documentation for XNET HardwareResource properties."""

from typing import Protocol, Union

import nisyscfg.enums
import nisyscfg.xnet.enums


class HardwareResource(Protocol):
    """XNET HardwareResource properties."""

    number_of_ports: int
    """Number of ports on the device."""
    ip_stack_info_json: str
    """IP stack information in JSON format."""
    ip_stack_info_text: str
    """IP stack information as plain text."""
    port_number: int
    """Port number."""
    protocol: Union[nisyscfg.xnet.enums.Protocol, int]
    """Protocol type for the port."""
    can_termination_capability: Union[nisyscfg.enums.Bool, int]
    """CAN termination capability."""
    can_transceiver_capability: Union[nisyscfg.xnet.enums.CanTransceiverCapability, int]
    """CAN transceiver capability."""
    dongle_id: Union[nisyscfg.xnet.enums.DongleId, int]
    """Dongle ID."""
    dongle_state: Union[nisyscfg.xnet.enums.DongleState, int]
    """Dongle state."""
    blink: Union[nisyscfg.xnet.enums.Blink, int]
    """Blink property for the port."""
    enet_mac_addr: str
    """Automotive Ethernet MAC address."""
    enet_ip_v4_addr: str
    """Automotive Ethernet IPv4 address."""
    enet_os_adapter_name: str
    """OS adapter name for Automotive Ethernet."""
    enet_os_adapter_desc: str
    """OS adapter description for Automotive Ethernet."""
    enet_link_speed: Union[nisyscfg.xnet.enums.EnetLinkSpeed, int]
    """Automotive Ethernet link speed."""
    enet_sleep_capability: Union[nisyscfg.xnet.enums.EnetSleepCapability, int]
    """Automotive Ethernet sleep capability."""
    enet_phy_power_mode: Union[nisyscfg.xnet.enums.EnetPhyPowerMode, int]
    """Automotive Ethernet PHY power mode."""
    enet_phy_state: Union[nisyscfg.xnet.enums.EnetPhyState, int]
    """Automotive Ethernet PHY state."""
    enet_port_mode: Union[nisyscfg.xnet.enums.EnetPortMode, int]
    """Automotive Ethernet port mode."""
    enet_link_speed_configured: Union[nisyscfg.xnet.enums.EnetLinkSpeed, int]
    """Configured Automotive Ethernet link speed."""
    enet_jumbo_frames: Union[nisyscfg.xnet.enums.EnetJumboFrames, int]
    """Automotive Ethernet jumbo frames setting."""
    enet_interrupt_moderation: Union[nisyscfg.xnet.enums.EnetInterruptModeration, int]
    """Automotive Ethernet interrupt moderation."""
    enet_sleep_capability_configured: Union[nisyscfg.xnet.enums.EnetSleepCapability, int]
    """Configured Automotive Ethernet sleep capability."""
