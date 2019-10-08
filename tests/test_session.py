import ctypes
import nisyscfg as nisyscfg
import nisyscfg.enums
import nisyscfg.errors
import nisyscfg.properties
import pytest

try:
    from unittest import mock
except ImportError:
    import mock


def test_import():
    nisyscfg.Session


SESSION_HANDLE = 1
EXPERT_ENUM_HANDLE = 2
RESOURCE_ENUM_HANDLE = 3
FILTER_HANDLE = 4
SOFTWARE_COMPONENT_HANDLE = 5


STATUS_DESCRIPTION = ctypes.c_char_p(b'description')
STATUS_DESCRIPTION_VOID_P = ctypes.cast(STATUS_DESCRIPTION, ctypes.c_void_p)


class CVoidPMatcher(object):
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return ctypes.cast(other, ctypes.c_void_p).value == self.value

    def __repr__(self):
        return 'c_void_p({})'.format(self.value)


class CIntPMatcher(object):
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return other.value == self.value

    def __repr__(self):
        return '{}'.format(ctypes.c_int(self.value))


class CUIntPMatcher(object):
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return other.value == self.value

    def __repr__(self):
        return '{}'.format(ctypes.c_uint(self.value))


class ExpertInfoSideEffect(object):
    def __init__(self, expert_name, display_name, version):
        self.expert_name = expert_name
        self.display_name = display_name
        self.version = version

    def __call__(self, handle, expert_name, display_name, version):
        expert_name.value = self.expert_name
        display_name.value = self.display_name
        version.value = self.version
        return nisyscfg.errors.Status.OK


class NextResourceSideEffect(object):
    def __init__(self, resource_handle):
        self.resource_handle = resource_handle

    def __call__(self, session_handle, resource_enum_handle, resource_handle):
        resource_handle.contents.value = self.resource_handle
        return nisyscfg.errors.Status.OK


def initialize_session_mock(target_name, username, password, language, force_property_refresh,
                            connect_timeout_msec, expert_enum_handle, session_handle):
    session_handle.contents.value = SESSION_HANDLE
    if expert_enum_handle:
        expert_enum_handle.contents.value = EXPERT_ENUM_HANDLE
    return nisyscfg.errors.Status.OK


def _get_status_description_mock(session_handle, status, detailed_description):
    ctypes.cast(detailed_description, ctypes.POINTER(ctypes.c_void_p)).contents.value = STATUS_DESCRIPTION_VOID_P.value
    return nisyscfg.errors.Status.OK


def get_system_experts_mock(session_handle, expert_names, expert_enum_handle):
    expert_enum_handle.contents.value = EXPERT_ENUM_HANDLE
    return nisyscfg.errors.Status.OK


def find_hardware_mock(session_handle, mode, filter_handle, expert_names, resource_enum_handle):
    resource_enum_handle.contents.value = RESOURCE_ENUM_HANDLE
    return nisyscfg.errors.Status.OK


def create_filter_mock(session_handle, filter_handle):
    filter_handle.contents.value = FILTER_HANDLE
    return nisyscfg.errors.Status.OK


def get_available_software_components_mock(session_handle, item_types, software_component_handle):
    software_component_handle.contents.value = SOFTWARE_COMPONENT_HANDLE
    return nisyscfg.errors.Status.OK


def get_installed_software_components_mock(session_handle, item_types, cached, software_component_handle):
    software_component_handle.contents.value = SOFTWARE_COMPONENT_HANDLE
    return nisyscfg.errors.Status.OK


@pytest.fixture(scope='function')
def lib_mock():
    with mock.patch('platform.system') as platform_system_mock:
        with mock.patch('platform.architecture') as platform_architecture_mock:
            with mock.patch('ctypes.CDLL') as ctypes_mock:
                platform_system_mock.return_value = 'Linux'
                platform_architecture_mock.return_value = ('64bit', 'ELF')
                lib = ctypes_mock.return_value
                lib.__enter__.return_value = lib
                lib.NISysCfgInitializeSession.side_effect = initialize_session_mock
                lib.NISysCfgCloseHandle.return_value = nisyscfg.errors.Status.OK
                lib.NISysCfgGetStatusDescription.side_effect = _get_status_description_mock
                lib.NISysCfgFreeDetailedString.return_value = nisyscfg.errors.Status.OK
                lib.NISysCfgGetSystemExperts.side_effect = get_system_experts_mock
                lib.NISysCfgNextExpertInfo.return_value = nisyscfg.errors.Status.EndOfEnum
                lib.NISysCfgFindHardware.side_effect = find_hardware_mock
                lib.NISysCfgNextResource.return_value = nisyscfg.errors.Status.EndOfEnum
                lib.NISysCfgCreateFilter.side_effect = create_filter_mock
                lib.NISysCfgSetFilterProperty.return_value = nisyscfg.errors.Status.OK
                lib.NISysCfgSetFilterPropertyWithType.return_value = nisyscfg.errors.Status.OK
                lib.NISysCfgSetResourceProperty.return_value = nisyscfg.errors.Status.OK
                lib.NISysCfgRestart.return_value = nisyscfg.errors.Status.OK
                lib.NISysCfgGetAvailableSoftwareComponents.side_effect = get_available_software_components_mock
                lib.NISysCfgGetInstalledSoftwareComponents.side_effect = get_installed_software_components_mock
                lib.NISysCfgNextComponentInfo.return_value = nisyscfg.errors.Status.EndOfEnum
                yield ctypes_mock
    nisyscfg._library_singleton._instance = None


@pytest.fixture(scope='function')
def config_next_resource_side_effect_mock(lib_mock):
    side_effect_functions = (
        func for func in
        [
            NextResourceSideEffect(10),
            lambda *x: nisyscfg.errors.Status.EndOfEnum,
        ]
    )

    def next_resource_side_effect(session_handle, resource_enum_handle, resource_handle):
        return next(side_effect_functions)(session_handle, resource_enum_handle, resource_handle)

    lib_mock.return_value.NISysCfgNextResource.side_effect = next_resource_side_effect


@pytest.fixture(scope='function')
def config_get_resource_property_mock(lib_mock, expected_value):
    def get_resource_property_mock(resource_handle, property_id, property_value):
        if property_value.__class__.__name__.startswith('c_char_Array'):
            property_value.value = expected_value.encode('ascii')
        else:
            property_value.contents.value = expected_value
        return nisyscfg.errors.Status.OK

    lib_mock.return_value.NISysCfgGetResourceProperty.side_effect = get_resource_property_mock


def test_open_close_session_invokes_nisyscfg_c_api(lib_mock):
    session = nisyscfg.Session()
    session.close()
    expected_calls = [
        mock.call(mock.ANY),
        mock.call().NISysCfgInitializeSession(mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY),
        mock.call().NISysCfgCloseHandle(CVoidPMatcher(SESSION_HANDLE)),
    ]
    assert lib_mock.mock_calls == expected_calls


def test_session_in_with_statement_invokes_nisyscfg_c_api(lib_mock):
    with nisyscfg.Session():
        pass
    expected_calls = [
        mock.call(mock.ANY),
        mock.call().NISysCfgInitializeSession(mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY),
        mock.call().NISysCfgCloseHandle(CVoidPMatcher(SESSION_HANDLE)),
    ]
    assert lib_mock.mock_calls == expected_calls


def test_session_passes_target_name_to_initialize_session(lib_mock):
    with nisyscfg.Session('localhost'):
        pass
    expected_calls = [
        mock.call().NISysCfgInitializeSession(b'localhost', mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY),
    ]
    assert lib_mock().NISysCfgInitializeSession.mock_calls == expected_calls


def test_session_passes_username_and_password_to_initialize_session(lib_mock):
    with nisyscfg.Session('localhost', 'username', 'password'):
        pass
    expected_calls = [
        mock.call().NISysCfgInitializeSession(mock.ANY, b'username', b'password', mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY),
    ]
    assert lib_mock().NISysCfgInitializeSession.mock_calls == expected_calls


def test__get_status_description(lib_mock):
    with nisyscfg.Session() as session:
        assert 'description' == session._get_status_description(nisyscfg.errors.Status.OutOfMemory)
    expected_calls = [
        mock.call(mock.ANY),
        mock.call().NISysCfgInitializeSession(mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY),
        mock.call().NISysCfgGetStatusDescription(CVoidPMatcher(SESSION_HANDLE), nisyscfg.errors.Status.OutOfMemory, mock.ANY),
        mock.call().NISysCfgFreeDetailedString(CVoidPMatcher(STATUS_DESCRIPTION_VOID_P.value)),
        mock.call().NISysCfgCloseHandle(CVoidPMatcher(SESSION_HANDLE)),
    ]
    assert lib_mock.mock_calls == expected_calls


def test_get_system_experts_with_no_experts(lib_mock):
    with nisyscfg.Session() as session:
        session.get_system_experts()
    expected_calls = [
        mock.call(mock.ANY),
        mock.call().NISysCfgInitializeSession(mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY),
        mock.call().NISysCfgGetSystemExperts(CVoidPMatcher(SESSION_HANDLE), b'', mock.ANY),
        mock.call().NISysCfgCloseHandle(CVoidPMatcher(EXPERT_ENUM_HANDLE)),
        mock.call().NISysCfgCloseHandle(CVoidPMatcher(SESSION_HANDLE)),
    ]
    assert lib_mock.mock_calls == expected_calls


def test_expert_info_iterator_raises_error_after_close(lib_mock):
    with nisyscfg.Session() as session:
        expert_info = session.get_system_experts()
        expert_info.close()
        with pytest.raises(Exception):
            expert_info.next()


def test_get_system_experts_with_two_experts(lib_mock):
    side_effect_functions = (
        func for func in
        [
            ExpertInfoSideEffect(b'sync', b'NI-Sync', b'1.2.0'),
            ExpertInfoSideEffect(b'xnet', b'NI-XNET', b'10.0'),
            lambda *x: nisyscfg.errors.Status.EndOfEnum,
        ]
    )

    def expert_info_side_effect(handle, expert_name, display_name, version):
        return next(side_effect_functions)(handle, expert_name, display_name, version)

    lib_mock.return_value.NISysCfgNextExpertInfo.side_effect = expert_info_side_effect

    with nisyscfg.Session() as session:
        expert_info = list(session.get_system_experts())
    expected_calls = [
        mock.call(mock.ANY),
        mock.call().NISysCfgInitializeSession(mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY),
        mock.call().NISysCfgGetSystemExperts(CVoidPMatcher(SESSION_HANDLE), b'', mock.ANY),
        mock.call().NISysCfgNextExpertInfo(CVoidPMatcher(EXPERT_ENUM_HANDLE), mock.ANY, mock.ANY, mock.ANY),
        mock.call().NISysCfgNextExpertInfo(CVoidPMatcher(EXPERT_ENUM_HANDLE), mock.ANY, mock.ANY, mock.ANY),
        mock.call().NISysCfgNextExpertInfo(CVoidPMatcher(EXPERT_ENUM_HANDLE), mock.ANY, mock.ANY, mock.ANY),
        mock.call().NISysCfgCloseHandle(CVoidPMatcher(EXPERT_ENUM_HANDLE)),
        mock.call().NISysCfgCloseHandle(CVoidPMatcher(SESSION_HANDLE)),
    ]
    assert lib_mock.mock_calls == expected_calls
    assert len(expert_info) == 2
    assert expert_info[0]['expert_name'] == 'sync'
    assert expert_info[0]['display_name'] == 'NI-Sync'
    assert expert_info[0]['version'] == '1.2.0'
    assert expert_info[1]['expert_name'] == 'xnet'
    assert expert_info[1]['display_name'] == 'NI-XNET'
    assert expert_info[1]['version'] == '10.0'


def test_get_system_experts_with_csv_expert_names(lib_mock):
    with nisyscfg.Session() as session:
        session.get_system_experts('xnet,sync')
    expected_calls = [
        mock.call().NISysCfgGetSystemExperts(CVoidPMatcher(SESSION_HANDLE), b'xnet,sync', mock.ANY),
    ]
    assert lib_mock().NISysCfgGetSystemExperts.mock_calls == expected_calls


def test_get_system_experts_with_list_of_expert_names(lib_mock):
    with nisyscfg.Session() as session:
        session.get_system_experts(['xnet', 'sync'])
    expected_calls = [
        mock.call().NISysCfgGetSystemExperts(CVoidPMatcher(SESSION_HANDLE), b'xnet,sync', mock.ANY),
    ]
    assert lib_mock().NISysCfgGetSystemExperts.mock_calls == expected_calls


def test_find_hardware_with_default_arguments(lib_mock):
    with nisyscfg.Session() as session:
        session.find_hardware()
    expected_calls = [
        mock.call(mock.ANY),
        mock.call().NISysCfgInitializeSession(mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY),
        mock.call().NISysCfgFindHardware(CVoidPMatcher(SESSION_HANDLE), nisyscfg.enums.FilterMode.MatchValuesAll, None, b'', mock.ANY),
        mock.call().NISysCfgCloseHandle(CVoidPMatcher(RESOURCE_ENUM_HANDLE)),
        mock.call().NISysCfgCloseHandle(CVoidPMatcher(SESSION_HANDLE)),
    ]
    assert lib_mock.mock_calls == expected_calls


def test_find_hardware_with_filter_properties_specified(lib_mock):
    with nisyscfg.Session() as session:
        filter = session.create_filter()
        filter[nisyscfg.FilterProperties.EXPERT_NAME] = 'my_expert'
        session.find_hardware(filter)
    expected_calls = [
        mock.call(mock.ANY),
        mock.call().NISysCfgInitializeSession(mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY),
        mock.call().NISysCfgCreateFilter(CVoidPMatcher(SESSION_HANDLE), mock.ANY),
        mock.call().NISysCfgSetFilterPropertyWithType(CVoidPMatcher(FILTER_HANDLE), nisyscfg.FilterProperties.EXPERT_NAME._id, nisyscfg.enums.PropertyType.String, b'my_expert'),
        mock.call().NISysCfgFindHardware(CVoidPMatcher(SESSION_HANDLE), nisyscfg.enums.FilterMode.MatchValuesAll, mock.ANY, b'', mock.ANY),
        mock.call().NISysCfgCloseHandle(CVoidPMatcher(RESOURCE_ENUM_HANDLE)),
        mock.call().NISysCfgCloseHandle(CVoidPMatcher(FILTER_HANDLE)),
        mock.call().NISysCfgCloseHandle(CVoidPMatcher(SESSION_HANDLE)),
    ]
    assert lib_mock.mock_calls == expected_calls


def test_find_hardware_with_csv_expert_names(lib_mock):
    with nisyscfg.Session() as session:
        session.find_hardware(expert_names='xnet,sync')
    expected_calls = [
        mock.call().NISysCfgFindHardware(mock.ANY, mock.ANY, mock.ANY, b'xnet,sync', mock.ANY),
    ]
    assert lib_mock().NISysCfgFindHardware.mock_calls == expected_calls


def test_find_hardware_with_list_of_expert_names(lib_mock):
    with nisyscfg.Session() as session:
        session.find_hardware(expert_names=['xnet', 'sync'])
    expected_calls = [
        mock.call().NISysCfgFindHardware(mock.ANY, mock.ANY, mock.ANY, b'xnet,sync', mock.ANY),
    ]
    assert lib_mock().NISysCfgFindHardware.mock_calls == expected_calls


@pytest.mark.parametrize(
    "property_name, property_type, assigned_value, expected_value",
    [
        ('IS_DEVICE', nisyscfg.enums.PropertyType.Bool, True, CIntPMatcher(1)),
        ('IS_CHASSIS', nisyscfg.enums.PropertyType.Bool, False, CIntPMatcher(0)),
        ('EXPERT_NAME', nisyscfg.enums.PropertyType.String, 'my_expert', b'my_expert'),
        ('USER_ALIAS', nisyscfg.enums.PropertyType.String, 'my_alias', b'my_alias'),
        ('VENDOR_ID', nisyscfg.enums.PropertyType.UnsignedInt, 1337, CUIntPMatcher(1337))
    ])
def test_find_hardware_with_passed_filter_properties_specified(lib_mock, property_name, property_type, assigned_value, expected_value):
    with nisyscfg.Session() as session:
        filter = session.create_filter()
        filter[getattr(nisyscfg.FilterProperties, property_name)] = assigned_value
        session.find_hardware(filter)
        property_id = getattr(nisyscfg.FilterProperties, property_name)._id
    expected_calls = [
        mock.call(mock.ANY),
        mock.call().NISysCfgInitializeSession(mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY),
        mock.call().NISysCfgCreateFilter(CVoidPMatcher(SESSION_HANDLE), mock.ANY),
        mock.call().NISysCfgSetFilterPropertyWithType(CVoidPMatcher(FILTER_HANDLE), property_id, property_type, expected_value),
        mock.call().NISysCfgFindHardware(CVoidPMatcher(SESSION_HANDLE), nisyscfg.enums.FilterMode.MatchValuesAll, mock.ANY, b'', mock.ANY),
        mock.call().NISysCfgCloseHandle(CVoidPMatcher(RESOURCE_ENUM_HANDLE)),
        mock.call().NISysCfgCloseHandle(CVoidPMatcher(FILTER_HANDLE)),
        mock.call().NISysCfgCloseHandle(CVoidPMatcher(SESSION_HANDLE)),
    ]
    assert lib_mock.mock_calls == expected_calls


def test_create_filter(lib_mock):
    with nisyscfg.Session() as session:
        session.create_filter()
    expected_calls = [
        mock.call(mock.ANY),
        mock.call().NISysCfgInitializeSession(mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY),
        mock.call().NISysCfgCreateFilter(CVoidPMatcher(SESSION_HANDLE), mock.ANY),
        mock.call().NISysCfgCloseHandle(CVoidPMatcher(FILTER_HANDLE)),
        mock.call().NISysCfgCloseHandle(CVoidPMatcher(SESSION_HANDLE)),
    ]
    assert lib_mock.mock_calls == expected_calls


def test_create_filter_and_set_syscfg_filter_property(lib_mock):
    with nisyscfg.Session() as session:
        filter = session.create_filter()
        filter[nisyscfg.FilterProperties.EXPERT_NAME] = 'my_expert'
    expected_calls = [
        mock.call(mock.ANY),
        mock.call().NISysCfgInitializeSession(mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY),
        mock.call().NISysCfgCreateFilter(CVoidPMatcher(SESSION_HANDLE), mock.ANY),
        mock.call().NISysCfgSetFilterPropertyWithType(CVoidPMatcher(FILTER_HANDLE), nisyscfg.FilterProperties.EXPERT_NAME._id, nisyscfg.enums.PropertyType.String, b'my_expert'),
        mock.call().NISysCfgCloseHandle(CVoidPMatcher(FILTER_HANDLE)),
        mock.call().NISysCfgCloseHandle(CVoidPMatcher(SESSION_HANDLE)),
    ]
    assert lib_mock.mock_calls == expected_calls


def test_restart_with_default_arguments(lib_mock):
    with nisyscfg.Session() as session:
        session.restart()
    expected_calls = [
        mock.call(mock.ANY),
        mock.call().NISysCfgInitializeSession(mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY),
        mock.call().NISysCfgRestart(CVoidPMatcher(SESSION_HANDLE), True, False, False, mock.ANY, mock.ANY),
        mock.call().NISysCfgCloseHandle(CVoidPMatcher(SESSION_HANDLE)),
    ]
    assert lib_mock.mock_calls == expected_calls


def test_get_available_software_components_with_default_arguments(lib_mock):
    with nisyscfg.Session() as session:
        session.get_available_software_components()
    expected_calls = [
        mock.call(mock.ANY),
        mock.call().NISysCfgInitializeSession(mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY),
        mock.call().NISysCfgGetAvailableSoftwareComponents(CVoidPMatcher(SESSION_HANDLE), mock.ANY, mock.ANY),
        mock.call().NISysCfgCloseHandle(CVoidPMatcher(SOFTWARE_COMPONENT_HANDLE)),
        mock.call().NISysCfgCloseHandle(CVoidPMatcher(SESSION_HANDLE)),
    ]
    assert lib_mock.mock_calls == expected_calls


def test_get_installed_software_components_with_default_arguments(lib_mock):
    with nisyscfg.Session() as session:
        session.get_installed_software_components()
    expected_calls = [
        mock.call(mock.ANY),
        mock.call().NISysCfgInitializeSession(mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY),
        mock.call().NISysCfgGetInstalledSoftwareComponents(CVoidPMatcher(SESSION_HANDLE), mock.ANY, False, mock.ANY),
        mock.call().NISysCfgCloseHandle(CVoidPMatcher(SOFTWARE_COMPONENT_HANDLE)),
        mock.call().NISysCfgCloseHandle(CVoidPMatcher(SESSION_HANDLE)),
    ]
    assert lib_mock.mock_calls == expected_calls


def test_interating_over_hardware_resources(lib_mock):
    side_effect_functions = (
        func for func in
        [
            NextResourceSideEffect(10),
            NextResourceSideEffect(11),
            NextResourceSideEffect(12),
            lambda *x: nisyscfg.errors.Status.EndOfEnum,
        ]
    )

    def next_resource_side_effect(session_handle, resource_enum_handle, resource_handle):
        return next(side_effect_functions)(session_handle, resource_enum_handle, resource_handle)

    lib_mock.return_value.NISysCfgNextResource.side_effect = next_resource_side_effect

    with nisyscfg.Session() as session:
        resources = list(session.find_hardware())
        assert len(resources) == 3

    expected_calls = [
        mock.call(mock.ANY),
        mock.call().NISysCfgInitializeSession(mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY),
        mock.call().NISysCfgFindHardware(mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY),
        mock.call().NISysCfgNextResource(CVoidPMatcher(SESSION_HANDLE), CVoidPMatcher(RESOURCE_ENUM_HANDLE), mock.ANY),
        mock.call().NISysCfgNextResource(CVoidPMatcher(SESSION_HANDLE), CVoidPMatcher(RESOURCE_ENUM_HANDLE), mock.ANY),
        mock.call().NISysCfgNextResource(CVoidPMatcher(SESSION_HANDLE), CVoidPMatcher(RESOURCE_ENUM_HANDLE), mock.ANY),
        mock.call().NISysCfgNextResource(CVoidPMatcher(SESSION_HANDLE), CVoidPMatcher(RESOURCE_ENUM_HANDLE), mock.ANY),
        mock.call().NISysCfgCloseHandle(CVoidPMatcher(12)),
        mock.call().NISysCfgCloseHandle(CVoidPMatcher(11)),
        mock.call().NISysCfgCloseHandle(CVoidPMatcher(10)),
        mock.call().NISysCfgCloseHandle(CVoidPMatcher(RESOURCE_ENUM_HANDLE)),
        mock.call().NISysCfgCloseHandle(CVoidPMatcher(SESSION_HANDLE)),
    ]
    assert lib_mock.mock_calls == expected_calls


def test_hardware_resource_raises_error_after_close(lib_mock):
    with nisyscfg.Session() as session:
        resource = session.find_hardware()
        resource.close()
        with pytest.raises(Exception):
            resource.next()


@pytest.mark.parametrize(
    "property_name, expected_value",
    [
        ('IS_DEVICE', True),
        ('IS_CHASSIS', False),
        ('VENDOR_ID', 0x1093),
        ('VENDOR_NAME', 'National Instruments'),
        ('PRODUCT_ID', 0xABC),
        ('PRODUCT_NAME', 'NI-BubbleGum'),
    ])
def test_get_hardware_resource_property(lib_mock, config_next_resource_side_effect_mock, config_get_resource_property_mock, property_name, expected_value):
    with nisyscfg.Session() as session:
        resource = next(session.find_hardware())
        assert expected_value == resource[getattr(nisyscfg.ResourceProperties, property_name)]
        property_id = getattr(nisyscfg.ResourceProperties, property_name)._id

    expected_calls = [
        mock.call(mock.ANY),
        mock.call().NISysCfgInitializeSession(mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY),
        mock.call().NISysCfgFindHardware(mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY),
        mock.call().NISysCfgNextResource(mock.ANY, mock.ANY, mock.ANY),
        mock.call().NISysCfgGetResourceProperty(CVoidPMatcher(10), property_id, mock.ANY),
        mock.call().NISysCfgCloseHandle(CVoidPMatcher(10)),
        mock.call().NISysCfgCloseHandle(CVoidPMatcher(RESOURCE_ENUM_HANDLE)),
        mock.call().NISysCfgCloseHandle(CVoidPMatcher(SESSION_HANDLE)),
    ]
    assert lib_mock.mock_calls == expected_calls


def test_get_hardware_resource_property_catches_prop_does_not_exist_and_raises_attribute_error(lib_mock, config_next_resource_side_effect_mock):
    lib_mock.return_value.NISysCfgGetResourceProperty.return_value = nisyscfg.errors.Status.PropDoesNotExist

    with nisyscfg.Session() as session:
        resource = next(session.find_hardware())
        with pytest.raises(AttributeError):
            getattr(resource, 'IsDevice')


def test_get_hardware_resource_property_raises_library_error_when_error_code_is_not_prop_does_not_exist(lib_mock, config_next_resource_side_effect_mock):
    lib_mock.return_value.NISysCfgGetResourceProperty.return_value = nisyscfg.errors.Status.OutOfMemory

    with nisyscfg.Session() as session:
        resource = next(session.find_hardware())
        with pytest.raises(nisyscfg.errors.LibraryError):
            resource[nisyscfg.ResourceProperties.IS_DEVICE]


@pytest.mark.parametrize(
    "property_name, count_property, expected_values",
    [
        ('EXPERT_NAME', 'NUMBER_OF_EXPERTS', ['xnet', 'sync']),
        ('EXPERT_USER_ALIAS', 'NUMBER_OF_EXPERTS', ['myDevice']),
        ('AVAILABLE_FIRMWARE_VERSION', 'NUMBER_OF_AVAILABLE_FIRMWARE_VERSIONS', ['1.0', '2.1', '3.3.3']),
        ('WLAN_AVAILABLE_CHANNEL_NUMBER', 'NUMBER_OF_DISCOVERED_ACCESS_POINTS', [3, 1, 2]),
        ('WLAN_AVAILABLE_LINK_SPEED', 'NUMBER_OF_DISCOVERED_ACCESS_POINTS', [nisyscfg.enums.LinkSpeed.Auto]),
    ])
def test_get_hardware_index_property(lib_mock, property_name, count_property, expected_values):
    side_effect_functions = (
        func for func in
        [
            NextResourceSideEffect(10),
            lambda *x: nisyscfg.errors.Status.EndOfEnum,
        ]
    )

    def next_resource_side_effect(session_handle, resource_enum_handle, resource_handle):
        return next(side_effect_functions)(session_handle, resource_enum_handle, resource_handle)

    def get_resource_property_mock(resource_handle, property_id, property_value):
        property_value.contents.value = len(expected_values)
        return nisyscfg.errors.Status.OK

    def get_indexed_property_mock(resource_handle, property_id, index, property_value):
        if property_value.__class__.__name__.startswith('c_char_Array'):
            property_value.value = expected_values[index].encode('ascii')
        else:
            property_value.contents.value = expected_values[index]
        return nisyscfg.errors.Status.OK

    lib_mock.return_value.NISysCfgNextResource.side_effect = next_resource_side_effect
    lib_mock.return_value.NISysCfgGetResourceProperty.side_effect = get_resource_property_mock
    lib_mock.return_value.NISysCfgGetResourceIndexedProperty.side_effect = get_indexed_property_mock

    with nisyscfg.Session() as session:
        resource = next(session.find_hardware())
        property = resource[getattr(nisyscfg.IndexedResourceProperties, property_name)]
        assert expected_values == list(property)
        count_property_id = getattr(nisyscfg.ResourceProperties, count_property)._id
        property_id = getattr(nisyscfg.IndexedResourceProperties, property_name)._id

    expected_calls = [
        mock.call(mock.ANY),
        mock.call().NISysCfgInitializeSession(mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY),
        mock.call().NISysCfgFindHardware(mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY),
        mock.call().NISysCfgNextResource(mock.ANY, mock.ANY, mock.ANY),
        mock.call().NISysCfgGetResourceProperty(CVoidPMatcher(10), count_property_id, mock.ANY),
    ]
    expected_calls += [
        mock.call().NISysCfgGetResourceIndexedProperty(CVoidPMatcher(10), property_id, i, mock.ANY)
        for i in range(len(expected_values))
    ]
    expected_calls += [
        mock.call().NISysCfgCloseHandle(CVoidPMatcher(10)),
        mock.call().NISysCfgCloseHandle(CVoidPMatcher(RESOURCE_ENUM_HANDLE)),
        mock.call().NISysCfgCloseHandle(CVoidPMatcher(SESSION_HANDLE)),
    ]
    assert lib_mock.mock_calls == expected_calls
