import nisyscfg
import nisyscfg.xnet
import sys


class PortNotFoundError(Exception):
    pass


def nixnet_blink_port_led(port_name, mode):
    with nisyscfg.Session() as session:
        # Search for the NI-XNET interface with port name.
        interface_filter = session.create_filter()
        interface_filter[nisyscfg.FilterProperties.IS_DEVICE] = False
        interface_filter[nisyscfg.FilterProperties.USER_ALIAS] = port_name

        try:
            # Assume only one interface will be found
            interface = next(session.find_hardware(filter=interface_filter, expert_names='xnet'))
        except StopIteration:
            raise PortNotFoundError('Could not find a port "{}"'.format(port_name))

        # Set blink property and apply changes.
        interface[nisyscfg.xnet.ResourceProperties.BLINK] = mode
        interface.save_changes()


if '__main__' == __name__:
    if len(sys.argv) != 3:
        print("Usage: {} <port_name> on|off".format(sys.argv[0]))
        sys.exit(1)

    port_name = sys.argv[1]
    mode = {
        'on': nisyscfg.xnet.enums.IntferfaceBlink.ENABLE,
        'off': nisyscfg.xnet.enums.IntferfaceBlink.DISABLE,
    }[sys.argv[2].lower()]
    nixnet_blink_port_led(port_name, mode)
