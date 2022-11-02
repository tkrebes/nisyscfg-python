import nisyscfg


def print_primary_expert_alias_and_resource():
    format_string = "{0: <16} {1: <32} {2}"
    with nisyscfg.Session() as session:
        print(format_string.format("Expert", "Alias", "Resource"))
        filter = session.create_filter()
        filter.is_present = True
        filter.is_ni_product = True
        for resource in session.find_hardware(filter):
            # The first user alias in the list is from the primary expert
            print(
                format_string.format(
                    resource.expert_name[0],
                    resource.expert_user_alias[0],
                    resource.expert_resource_name[0],
                )
            )


if __name__ == "__main__":
    print_primary_expert_alias_and_resource()
