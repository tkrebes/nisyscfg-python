import nisyscfg
import nisyscfg.xnet
import sys


class DeviceNotFoundError(Exception):
    pass


class PortNotFoundError(Exception):
    pass


def nixnet_assign_port_name(serial_number, port_number, port_name):
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
