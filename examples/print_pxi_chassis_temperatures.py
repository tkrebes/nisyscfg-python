import nisyscfg


def print_pxi_chassis_temperatures():
    with nisyscfg.Session() as session:
        filter = session.create_filter()
        filter.is_present = True
        filter.is_ni_product = True
        filter.is_chassis = True
        filter.expert_name = "ni-pxi"
        for chassis in session.find_hardware(filter):
            print(chassis.name)
            for name, reading in zip(
                chassis.temperature_name, chassis.temperature_reading
            ):
                print(f"   {name}: {reading}")


if __name__ == "__main__":
    print_pxi_chassis_temperatures()
