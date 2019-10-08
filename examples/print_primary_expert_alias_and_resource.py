import nisyscfg


def print_primary_expert_alias_and_resource():
    format_string = '{0: <16} {1: <32} {2}'
    with nisyscfg.Session() as session:
        print(format_string.format('Expert', 'Alias', 'Resource'))
        filter = session.create_filter()
        filter[nisyscfg.FilterProperties.IS_PRESENT] = True
        filter[nisyscfg.FilterProperties.IS_NI_PRODUCT] = True
        for resource in session.find_hardware(filter):
            # The first user alias in the list is from the primary expert
            print(format_string.format(
                resource[nisyscfg.IndexedResourceProperties.EXPERT_NAME][0],
                resource[nisyscfg.IndexedResourceProperties.EXPERT_USER_ALIAS][0],
                resource[nisyscfg.IndexedResourceProperties.EXPERT_RESOURCE_NAME][0]))


if __name__ == '__main__':
    print_primary_expert_alias_and_resource()
