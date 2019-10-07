import nisyscfg


def print_primary_expert_alias_and_resource():
    format_string = '{0: <16} {1: <32} {2}'
    with nisyscfg.Session() as session:
        print(format_string.format('Expert', 'Alias', 'Resource'))
        for resource in session.find_hardware(IsPresent=True, IsNIProduct=True):
            # The first user alias in the list is from the primary expert
            print(format_string.format(resource.ExpertName[0],
                                       resource.ExpertUserAlias[0],
                                       resource.ExpertResourceName[0]))
