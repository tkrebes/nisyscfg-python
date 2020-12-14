import itertools

import nisyscfg


def print_resource_temperature(resource, indent):
    for name, reading in itertools.zip_longest(
        resource.temperature_name, resource.temperature_reading
    ):
        print(f"{indent}{name or 'Temperature'}: {reading}")


def print_device_temperatures(session, provides_link_name, indent=""):
    print(f"{indent}Devices:")
    filter = session.create_filter()
    filter.is_present = True
    filter.is_ni_product = True
    filter.is_device = True
    filter.connects_to_link_name = provides_link_name
    for device in session.find_hardware(filter):
        print(f"{indent}    {device.product_name}: {device.name}")
        print_resource_temperature(device, f"{indent}    ")


def print_chassis_temperatures(session):
    print("Chassis:")
    filter = session.create_filter()
    filter.is_present = True
    filter.is_ni_product = True
    filter.is_chassis = True
    for chassis in session.find_hardware(filter):
        print(f"    {chassis.name}")
        print_resource_temperature(chassis, indent="        ")
        print_device_temperatures(
            session, chassis.provides_link_name, indent="        "
        )


def print_temperatures():
    with nisyscfg.Session() as session:
        print_device_temperatures(session, provides_link_name="")
        print_chassis_temperatures(session)


if __name__ == "__main__":
    print_temperatures()
