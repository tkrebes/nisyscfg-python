import nisyscfg
import sys


class DeviceNotFoundError(Exception):
    pass


def nixnet_upgrade_firmware(serial_number):
    with nisyscfg.Session() as session:
        # Search for the NI-XNET device with the specified serial number.
        device_filter = session.create_filter()
        device_filter[nisyscfg.FilterProperties.IS_DEVICE] = True
        device_filter[nisyscfg.FilterProperties.SERIAL_NUMBER] = serial_number

        try:
            # Assume only one device will be found
            device = next(session.find_hardware(filter=device_filter, expert_names='xnet'))
        except StopIteration:
            raise DeviceNotFoundError('Could not find a device with serial number "{}"'.format(serial_number))

        print('Starting firmware upgrade')
        device.upgrade_firmware(version='0')
        print('Completed firmware upgrade')


if '__main__' == __name__:
    if len(sys.argv) != 2:
        print("Usage: {} <serial_number>".format(sys.argv[0]))
        sys.exit(1)

    serial_number = sys.argv[1].upper()
    nixnet_upgrade_firmware(serial_number)
