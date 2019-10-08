import ctypes

from nisyscfg import _library_singleton
from nisyscfg import _properties
from nisyscfg import errors

from nisyscfg.enums import *  # noqa: F403
from nisyscfg.types import *  # noqa: F403

from nisyscfg._lib import c_string_decode
from nisyscfg._lib import c_string_encode


class Session(object):
    def __init__(self, target=None, username=None, password=None, language=Locale.Default, force_property_refresh=True, timeout=60000):  # noqa: F405
        self._children = []
        self._session = SessionHandle()  # noqa: F405
        self._library = _library_singleton.get()
        error_code = self._library.InitializeSession(
            c_string_encode(target),
            c_string_encode(username),
            c_string_encode(password),
            language,
            force_property_refresh,
            timeout,
            None,  # expert_enum_handle
            ctypes.pointer(self._session))
        errors.handle_error(self, error_code)

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def _get_status_description(self, status):
        c_detailed_description = ctypes.POINTER(ctypes.c_char)()
        error_code = self._library.GetStatusDescription(self._session, status, ctypes.pointer(c_detailed_description))
        if c_detailed_description:
            detailed_description = c_string_decode(ctypes.cast(c_detailed_description, ctypes.c_char_p).value)
            error_code_2 = self._library.FreeDetailedString(c_detailed_description)
        errors.handle_error(self, error_code, is_error_handling=True)
        errors.handle_error(self, error_code_2, is_error_handling=True)
        return detailed_description

    def close(self):
        self._children.reverse()
        for child in self._children:
            child.close()
        if self._session:
            error_code = self._library.CloseHandle(self._session)
            errors.handle_error(self, error_code)
            self._session = None

    def get_system_experts(self, expert_names=''):
        expert_handle = EnumExpertHandle()  # noqa: F405
        if isinstance(expert_names, list):
            expert_names = ','.join(expert_names)
        error_code = self._library.GetSystemExperts(self._session, c_string_encode(expert_names), ctypes.pointer(expert_handle))
        errors.handle_error(self, error_code)
        iter = ExpertInfoIterator(expert_handle, self._library)
        self._children.append(iter)
        return iter

    def find_hardware(self, filter=None, mode=FilterMode.MatchValuesAll, expert_names='', **filter_properties):  # noqa: F405
        if filter is None:
            if filter_properties:
                filter = self.create_filter()
            else:
                class DummyFilter(object):
                    _handle = None
                filter = DummyFilter()
        for property, value in filter_properties.items():
            setattr(filter, property, value)
        resource_handle = EnumResourceHandle()  # noqa: F405
        if isinstance(expert_names, list):
            expert_names = ','.join(expert_names)
        error_code = self._library.FindHardware(self._session, mode, filter._handle, c_string_encode(expert_names), ctypes.pointer(resource_handle))
        errors.handle_error(self, error_code)
        iter = HardwareResourceIterator(self._session, resource_handle, self._library)
        self._children.append(iter)
        return iter

    def create_filter(self):
        filter = Filter(self._session, self._library)
        self._children.append(filter)
        return filter

    def restart(self, sync_call=True, install_mode=False, flush_dns=False, timeout=90000):
        new_ip_address = simple_string()  # noqa: F405
        error_code = self._library.Restart(self._session, sync_call, install_mode, flush_dns, timeout, new_ip_address)
        errors.handle_error(self, error_code)
        return c_string_decode(new_ip_address.value)

    def get_available_software_components(self, item_types=IncludeComponentTypes.AllVisible):  # noqa: F405
        software_component_handle = EnumSoftwareComponentHandle()  # noqa: F405
        error_code = self._library.GetAvailableSoftwareComponents(self._session, item_types, ctypes.pointer(software_component_handle))
        errors.handle_error(self, error_code)
        if software_component_handle:
            iter = ComponentInfoIterator(software_component_handle, self._library)
            self._children.append(iter)
            return iter

    def get_installed_software_components(self, item_types=IncludeComponentTypes.AllVisible, cached=False):  # noqa: F405
        software_component_handle = EnumSoftwareComponentHandle()  # noqa: F405
        error_code = self._library.GetInstalledSoftwareComponents(self._session, item_types, cached, ctypes.pointer(software_component_handle))
        errors.handle_error(self, error_code)
        if software_component_handle:
            iter = ComponentInfoIterator(software_component_handle, self._library)
            self._children.append(iter)
            return iter


class ExpertInfoIterator(object):
    def __init__(self, handle, library):
        self._handle = handle
        self._library = library

    def __del__(self):
        self.close()

    def __iter__(self):
        return self

    def __next__(self):
        if not self._handle:
            # TODO(tkrebes): raise RuntimeError
            raise StopIteration()
        expert_name = simple_string()  # noqa: F405
        display_name = simple_string()  # noqa: F405
        version = simple_string()  # noqa: F405
        error_code = self._library.NextExpertInfo(self._handle, expert_name, display_name, version)
        if error_code == 1:
            raise StopIteration()
        errors.handle_error(self, error_code)
        return {
            'expert_name': c_string_decode(expert_name.value),
            'display_name': c_string_decode(display_name.value),
            'version': c_string_decode(version.value),
        }

    def close(self):
        if self._handle:
            error_code = self._library.CloseHandle(self._handle)
            errors.handle_error(self, error_code)
            self._handle = None

    def next(self):
        return self.__next__()


class FilterPropertyWrapper(object):
    def __init__(self, name):
        self._name = name

    @property
    def c_type(self):
        return _properties.filter[self._name]

    @property
    def syscfg_type(self):
        return None

    @property
    def id(self):
        return getattr(FilterProperty, self._name)  # noqa: F405


def get_filter_property(name):
    if name in _properties.filter:
        return FilterPropertyWrapper(name)


class Filter(object):
    def __init__(self, session, library):
        self.__dict__['_handle'] = FilterHandle()  # noqa: F405
        self.__dict__['_library'] = library
        error_code = self._library.CreateFilter(session, ctypes.pointer(self._handle))
        errors.handle_error(self, error_code)

    def __del__(self):
        self.close()

    def close(self):
        if self._handle:
            error_code = self._library.CloseHandle(self._handle)
            errors.handle_error(self, error_code)
            self._handle = None

    def __getattr__(self, name):
        import nisyscfg.addons
        if hasattr(nisyscfg.addons, name):
            return getattr(nisyscfg.addons, name).HardwareFilter(self)

        raise AttributeError(name)

    def _set_property(self, property, value):
        if property.c_type == ctypes.c_char_p:
            value = c_string_encode(value)
        elif issubclass(property.c_type, CtypesEnum):  # noqa: F405
            value = ctypes.c_int(value)
        else:
            value = property.c_type(value)
        if property.syscfg_type:
            error_code = self._library.SetFilterPropertyWithType(self._handle, property.id, property.syscfg_type, value)
        else:
            error_code = self._library.SetFilterProperty(self._handle, property.id, value)
        errors.handle_error(self, error_code)

    def __setattr__(self, name, value):
        if name in self.__dict__:
            self.__dict__[name] = value
        else:
            property = get_filter_property(name)
            if property is not None:
                self._set_property(property, value)


class HardwareResourceIterator(object):
    def __init__(self, session, handle, library):
        self._children = []
        self._session = session
        self._handle = handle
        self._library = library

    def __del__(self):
        self.close()

    def __iter__(self):
        return self

    def __next__(self):
        if not self._handle:
            # TODO(tkrebes): raise RuntimeError
            raise StopIteration()
        resource_handle = ResourceHandle()  # noqa: F405
        error_code = self._library.NextResource(self._session, self._handle, ctypes.pointer(resource_handle))
        if error_code == 1:
            raise StopIteration()
        errors.handle_error(self, error_code)
        resource = HardwareResource(resource_handle, self._library)
        self._children.append(resource)
        return resource

    def close(self):
        self._children.reverse()
        for child in self._children:
            child.close()
        if self._handle:
            error_code = self._library.CloseHandle(self._handle)
            errors.handle_error(self, error_code)
            self._handle = None

    def next(self):
        return self.__next__()


class ResourcePropertyWrapper(object):
    def __init__(self, name):
        self._name = name

    @property
    def indexed(self):
        return False

    @property
    def name(self):
        return self._name

    @property
    def c_type(self):
        return _properties.resource[self._name]

    @property
    def id(self):
        return getattr(ResourceProperty, self._name)  # noqa: F405


class IndexedPropertyWrapper(object):
    def __init__(self, name):
        self._name = name

    @property
    def indexed(self):
        return True

    @property
    def name(self):
        return self._name

    @property
    def c_type(self):
        return _properties.indexed[self._name]

    @property
    def id(self):
        return getattr(IndexedProperty, self._name)  # noqa: F405


def get_hardware_property(name):
    if name in _properties.resource:
        return ResourcePropertyWrapper(name)
    if name in _properties.indexed:
        return IndexedPropertyWrapper(name)


class HardwareResource(object):
    def __init__(self, handle, library):
        self.__dict__['_handle'] = handle
        self.__dict__['_library'] = library

    def __del__(self):
        self.close()

    def close(self):
        if self._handle:
            error_code = self._library.CloseHandle(self._handle)
            errors.handle_error(self, error_code)
            self._handle = None

    def _get_resource_property(self, property):
        if property.c_type == ctypes.c_char_p:
            value = simple_string()  # noqa: F405
            value_arg = value
        elif issubclass(property.c_type, CtypesEnum):  # noqa: F405
            value = ctypes.c_int()
            value_arg = ctypes.pointer(value)
        else:
            value = property.c_type(0)
            value_arg = ctypes.pointer(value)

        error_code = self._library.GetResourceProperty(self._handle, property.id, value_arg)
        errors.handle_error(self, error_code)

        if issubclass(property.c_type, CtypesEnum):  # noqa: F405
            return property.c_type(value.value)

        return c_string_decode(value.value)

    def _get_resource_indexed_property(self, property, index):
        if property.c_type == ctypes.c_char_p:
            value = simple_string()  # noqa: F405
            value_arg = value
        elif issubclass(property.c_type, CtypesEnum):  # noqa: F405
            value = ctypes.c_int()
            value_arg = ctypes.pointer(value)
        else:
            value = property.c_type()
            value_arg = ctypes.pointer(value)

        error_code = self._library.GetResourceIndexedProperty(self._handle, property.id, index, value_arg)
        errors.handle_error(self, error_code)

        if issubclass(property.c_type, CtypesEnum):  # noqa: F405
            return property.c_type(value.value)

        return c_string_decode(value.value)

    def _get_property(self, property):
        try:
            if property.indexed:
                return IndexProperties(self, property)
            else:
                return self._get_resource_property(property)
        except errors.LibraryError as err:
            if err.code == errors.Status.PropDoesNotExist:
                raise AttributeError(property.name)
            raise

    def __getattr__(self, name):
        property = get_hardware_property(name)
        if property is None:
            import nisyscfg.addons
            if hasattr(nisyscfg.addons, name):
                return getattr(nisyscfg.addons, name).HardwareResource(self)
        else:
            return self._get_property(property)

        # TODO(tkrebes): add error message
        raise AttributeError(name)

    def _set_resource_property(self, property, value):
        if property.c_type == ctypes.c_char_p:
            value = c_string_encode(value)
        elif issubclass(property.c_type, CtypesEnum):  # noqa: F405
            value = ctypes.c_int(value)
        else:
            value = property.c_type(value)

        error_code = self._library.SetResourceProperty(self._handle, property.id, value)
        errors.handle_error(self, error_code)

    def _set_property(self, property, value):
        if not property.indexed:
            return self._set_resource_property(property, value)

    def __setattr__(self, name, value):
        if name in self.__dict__:
            self.__dict__[name] = value
        else:
            property = get_hardware_property(name)
            if property is not None:
                self._set_property(property, value)

    def rename(self, new_name, overwrite_conflict=False, update_dependencies=False):
        error_code = self._library.RenameResource(
            self._handle,
            c_string_encode(new_name),
            overwrite_conflict,
            update_dependencies,
            None,
            None)
        errors.handle_error(self, error_code)

    def reset(self, mode=0):
        error_code = self._library.ResetHardware(self._handle, mode)
        errors.handle_error(self, error_code)

    def save_changes(self):
        restart_required = ctypes.c_int()
        error_code = self._library.SaveResourceChanges(self._handle, restart_required, None)
        errors.handle_error(self, error_code)
        return restart_required.value != 0

    def self_test(self, mode=0):
        error_code = self._library.SelfTestHardware(self._handle, mode, None)
        errors.handle_error(self, error_code)

    def upgrade_firmware(self, version=None, filepath=None, auto_stop_task=False, force=False, sync_call=True):
        if version and filepath:
            raise ValueError("version and filepath are mutually exclusive parameters")

        if version:
            error_code = self._library.UpgradeFirmwareVersion(
                self._handle, c_string_encode(version), auto_stop_task, force, sync_call, None, None)
        elif filepath:
            error_code = self._library.UpgradeFirmwareFromFile(
                self._handle, c_string_encode(filepath), auto_stop_task, force, sync_call, None, None)
        else:
            raise ValueError("upgrade_firmware() requires either version or filepath to be specified")

        errors.handle_error(self, error_code)


class IndexProperties(object):
    def __init__(self, session, property):
        self._session = session
        self._property = property

    def __getitem__(self, key):
        try:
            key + 1
        except TypeError:
            raise KeyError(key)
        if key >= 0 and key < len(self):
            return self._session._get_resource_indexed_property(self._property, key)
        raise KeyError(key)

    def __len__(self):
        if not hasattr(self, '_len'):
            self._len = 1
            try:
                for prefix, count_property in [
                    ('WlanAvailable',            'NumberOfDiscoveredAccessPoints'),  # noqa: E241
                    ('Expert',                   'NumberOfExperts'),  # noqa: E241
                    ('Service',                  'NumberOfServices'),  # noqa: E241
                    ('AvailableFirmwareVersion', 'NumberOfAvailableFirmwareVersions'), ]:  # noqa: E241
                    if self._property.name.startswith(prefix):
                        # TODO(tkrebes): Figure out why GetResourceProperty throws an error
                        self._len = getattr(self._session, count_property)
            except errors.Error:
                pass
        return self._len

    def __iter__(self):
        class IndexPropertiesIter(object):
            def __init__(self, properties):
                self._properties = properties
                self._index = -1

            def __next__(self):
                self._index += 1
                if self._index == len(self._properties):
                    raise StopIteration()
                return self._properties[self._index]

            def next(self):
                return self.__next__()

        return IndexPropertiesIter(self)


class ComponentInfoIterator(object):
    def __init__(self, handle, library):
        self._handle = handle
        self._library = library

    def __del__(self):
        self.close()

    def __iter__(self):
        return self

    def __next__(self):
        id = simple_string()  # noqa: F405
        version = simple_string()  # noqa: F405
        title = simple_string()  # noqa: F405
        item_type = ctypes.c_long()  # noqa: F405
        error_code = self._library.NextComponentInfo(self._handle, id, version, title, ctypes.pointer(item_type), None)
        if error_code == 1:
            raise StopIteration()
        errors.handle_error(self, error_code)
        return {
            'id': c_string_decode(id.value),
            'version': c_string_decode(version.value),
            'title': c_string_decode(title.value),
            'type': ComponentType(item_type.value),  # noqa: F405
            'details': None,  # TODO(tkrebes): Implement
        }

    def close(self):
        if self._handle:
            error_code = self._library.CloseHandle(self._handle)
            errors.handle_error(self, error_code)
            self._handle = None

    def next(self):
        return self.__next__()
