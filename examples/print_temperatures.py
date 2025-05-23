"""Example script to print device and chassis temperature readings using nisyscfg."""

import itertools

import nisyscfg


def print_resource_temperature(
    resource: nisyscfg.hardware_resource.HardwareResource, indent: str
) -> None:
    """Print temperature readings for a resource.

    Args:
        resource: The resource object with temperature_name and temperature_reading attributes.
        indent (str): String to prepend to each printed line for indentation.
    """
    for name, reading in itertools.zip_longest(
        resource.temperature_name, resource.temperature_reading
    ):
        print(indent + "{}: {}".format(name or "Temperature", reading))


def print_device_temperatures(
    session: "nisyscfg.Session", provides_link_name: str, indent: str = ""
) -> None:
    """Print temperature readings for all devices connected to a link.

    Args:
        session: nisyscfg.Session object.
        provides_link_name (str): Link name to filter devices.
        indent (str, optional): Indentation for output. Defaults to "".
    """
    print(indent + "Devices:")
    filter = session.create_filter()
    filter.is_present = True
    filter.is_ni_product = True
    filter.is_device = True
    filter.connects_to_link_name = provides_link_name
    for device in session.find_hardware(filter):
        print(indent + "    {}: {}".format(device.product_name, device.name))
        print_resource_temperature(device, indent + "        ")


def print_chassis_temperatures(session: "nisyscfg.Session") -> None:
    """Print temperature readings for all chassis and their devices.

    Args:
        session: nisyscfg.Session object.
    """
    print("Chassis:")
    filter = session.create_filter()
    filter.is_present = True
    filter.is_ni_product = True
    filter.is_chassis = True
    for chassis in session.find_hardware(filter):
        print("    " + chassis.name)
        print_resource_temperature(chassis, indent="        ")
        print_device_temperatures(session, chassis.provides_link_name, indent="        ")


def print_temperatures() -> None:
    """Print all device and chassis temperature readings for the current system."""
    with nisyscfg.Session() as session:
        print_device_temperatures(session, provides_link_name="")
        print_chassis_temperatures(session)


if __name__ == "__main__":
    print_temperatures()
