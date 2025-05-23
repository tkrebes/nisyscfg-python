"""Script to assign a user alias (port name) to an NI-XNET port using nisyscfg."""

import sys

import nisyscfg
import nisyscfg.xnet


class DeviceNotFoundError(Exception):
    """Exception raised when a device with the specified serial number is not found."""

    pass


class PortNotFoundError(Exception):
    """Exception raised when a port with the specified number is not found on the device."""

    pass


def nixnet_assign_port_name(serial_number: str, port_number: int, port_name: str) -> None:
    """Assign a user alias (port name) to an NI-XNET port.

    Args:
        serial_number (str): Serial number of the NI-XNET device.
        port_number (int): Port number on the device.
        port_name (str): New user alias to assign to the port.

    Raises:
        DeviceNotFoundError: If no device with the specified serial number is found.
        PortNotFoundError: If the device does not have the specified port number.
    """
    with nisyscfg.Session() as session:
        # Search for the NI-XNET device with the specified serial number.
        device_filter = session.create_filter()
        device_filter.is_device = True
        device_filter.serial_number = serial_number

        try:
            # Assume only one device will be found
            device = next(session.find_hardware(filter=device_filter, expert_names="xnet"))
        except StopIteration:
            raise DeviceNotFoundError(
                'Could not find a device with serial number "{}"'.format(serial_number)
            )

        # Search for the interface connected to the NI-XNET device with the
        # specified port number.
        interface_filter = session.create_filter()
        interface_filter.is_device = False
        interface_filter.connects_to_link_name = device.provides_link_name
        interface_filter.xnet.port_number = port_number

        try:
            # Assume only one interface will be found
            interface = next(session.find_hardware(filter=interface_filter, expert_names="xnet"))
        except StopIteration:
            raise PortNotFoundError(
                'Device with serial number "{}" does not have port number {}'.format(
                    serial_number, port_number
                )
            )

        interface.rename(port_name)


if "__main__" == __name__:
    if len(sys.argv) != 4:
        print("Usage: {} <serial_number> <port_number> <port_name>".format(sys.argv[0]))
        sys.exit(1)

    serial_number = sys.argv[1].upper()
    port_number = int(sys.argv[2])
    port_name = sys.argv[3]
    nixnet_assign_port_name(serial_number, port_number, port_name)
