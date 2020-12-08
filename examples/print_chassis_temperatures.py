import nisyscfg


def print_chassis_temperatures():
    with nisyscfg.Session() as session:
        filter = session.create_filter()
        filter.is_present = True
        filter.is_ni_product = True
        filter.is_chassis = True
        for chassis in session.find_hardware(filter):
            print(chassis.name)

            # Devices drivers may implement the indexed temperature sensor
            # properties, so try to retieve information via these APIs first.
            try:
                for name, reading in zip(
                    chassis.temperature_name, chassis.temperature_reading
                ):
                    print(f"   {name}: {reading}")

            # Otherwise, just check the current temperature property.
            except nisyscfg.errors.LibraryError as err:
                if err.code == nisyscfg.errors.Status.PROP_DOES_NOT_EXIST:
                    print(
                        "   Temperature: {}".format(
                            chassis.get_property("current_temp", "N/A")
                        )
                    )
                else:
                    raise


if __name__ == "__main__":
    print_chassis_temperatures()
