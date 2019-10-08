import ctypes

import nisyscfg
import nisyscfg._library_singleton

from nisyscfg._lib import c_string_decode
from nisyscfg._lib import c_string_encode


class Session(object):
    def __init__(self, target=None, username=None, password=None, language=nisyscfg.enums.Locale.Default, force_property_refresh=True, timeout=60000):
        self._children = []
        self._session = nisyscfg.types.SessionHandle()
        self._library = nisyscfg._library_singleton.get()
        error_code = self._library.InitializeSession(
            c_string_encode(target),
            c_string_encode(username),
            c_string_encode(password),
            language,
            force_property_refresh,
            timeout,
            None,  # expert_enum_handle
            ctypes.pointer(self._session))
        nisyscfg.errors.handle_error(self, error_code)

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
        nisyscfg.errors.handle_error(self, error_code, is_error_handling=True)
        nisyscfg.errors.handle_error(self, error_code_2, is_error_handling=True)
        return detailed_description

    def close(self):
        self._children.reverse()
        for child in self._children:
            child.close()
        if self._session:
            error_code = self._library.CloseHandle(self._session)
            nisyscfg.errors.handle_error(self, error_code)
            self._session = None

    def get_system_experts(self, expert_names=''):
        expert_handle = nisyscfg.types.EnumExpertHandle()
        if isinstance(expert_names, list):
            expert_names = ','.join(expert_names)
        error_code = self._library.GetSystemExperts(self._session, c_string_encode(expert_names), ctypes.pointer(expert_handle))
        nisyscfg.errors.handle_error(self, error_code)
        iter = ExpertInfoIterator(expert_handle, self._library)
        self._children.append(iter)
        return iter

    def find_hardware(self, filter=None, mode=nisyscfg.enums.FilterMode.MatchValuesAll, expert_names=''):
        if filter is None:
            class DummyFilter(object):
                _handle = None
            filter = DummyFilter()
        resource_handle = nisyscfg.types.EnumResourceHandle()
        if isinstance(expert_names, list):
            expert_names = ','.join(expert_names)
        error_code = self._library.FindHardware(self._session, mode, filter._handle, c_string_encode(expert_names), ctypes.pointer(resource_handle))
        nisyscfg.errors.handle_error(self, error_code)
        iter = HardwareResourceIterator(self._session, resource_handle, self._library)
        self._children.append(iter)
        return iter

    def create_filter(self):
        filter = Filter(self._session, self._library)
        self._children.append(filter)
        return filter

    def restart(self, sync_call=True, install_mode=False, flush_dns=False, timeout=90000):
        new_ip_address = nisyscfg.types.simple_string()
        error_code = self._library.Restart(self._session, sync_call, install_mode, flush_dns, timeout, new_ip_address)
        nisyscfg.errors.handle_error(self, error_code)
        return c_string_decode(new_ip_address.value)

    def get_available_software_components(self, item_types=nisyscfg.enums.IncludeComponentTypes.AllVisible):
        software_component_handle = nisyscfg.types.EnumSoftwareComponentHandle()
        error_code = self._library.GetAvailableSoftwareComponents(self._session, item_types, ctypes.pointer(software_component_handle))
        nisyscfg.errors.handle_error(self, error_code)
        if software_component_handle:
            iter = ComponentInfoIterator(software_component_handle, self._library)
            self._children.append(iter)
            return iter

    def get_installed_software_components(self, item_types=nisyscfg.enums.IncludeComponentTypes.AllVisible, cached=False):
        software_component_handle = nisyscfg.types.EnumSoftwareComponentHandle()
        error_code = self._library.GetInstalledSoftwareComponents(self._session, item_types, cached, ctypes.pointer(software_component_handle))
        nisyscfg.errors.handle_error(self, error_code)
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
        expert_name = nisyscfg.types.simple_string()
        display_name = nisyscfg.types.simple_string()
        version = nisyscfg.types.simple_string()
        error_code = self._library.NextExpertInfo(self._handle, expert_name, display_name, version)
        if error_code == 1:
            raise StopIteration()
        nisyscfg.errors.handle_error(self, error_code)
        return {
            'expert_name': c_string_decode(expert_name.value),
            'display_name': c_string_decode(display_name.value),
            'version': c_string_decode(version.value),
        }

    def close(self):
        if self._handle:
            error_code = self._library.CloseHandle(self._handle)
            nisyscfg.errors.handle_error(self, error_code)
            self._handle = None

    def next(self):
        return self.__next__()


class Filter(object):
    def __init__(self, session, library):
        self.__dict__['_handle'] = nisyscfg.types.FilterHandle()
        self.__dict__['_library'] = library
        error_code = self._library.CreateFilter(session, ctypes.pointer(self._handle))
        nisyscfg.errors.handle_error(self, error_code)

    def __del__(self):
        self.close()

    def close(self):
        if self._handle:
            error_code = self._library.CloseHandle(self._handle)
            nisyscfg.errors.handle_error(self, error_code)
            self._handle = None

    def _set_property(self, id, value, c_type, nisyscfg_type):
        if c_type == ctypes.c_char_p:
            value = c_string_encode(value)
        elif issubclass(c_type, nisyscfg.enums.CtypesEnum):
            value = ctypes.c_int(value)
        else:
            value = c_type(value)

        error_code = self._library.SetFilterPropertyWithType(self._handle, id, nisyscfg_type, value)
        nisyscfg.errors.handle_error(self, error_code)

    def __setitem__(self, tag, value):
        tag.set(self, value)

    def set_bool_property(self, id, value):
        self._set_property(id, value, nisyscfg.enums.Bool, nisyscfg.enums.PropertyType.Bool)

    def set_int_property(self, id, value):
        self._set_property(id, value, ctypes.c_int, nisyscfg.enums.PropertyType.Int)

    def set_unsigned_int_property(self, id, value):
        self._set_property(id, value, ctypes.c_uint, nisyscfg.enums.PropertyType.UnsignedInt)

    def set_double_property(self, id, value):
        self._set_property(id, value, ctypes.c_double, nisyscfg.enums.PropertyType.Double)

    def set_string_property(self, id, value):
        self._set_property(id, value, ctypes.c_char_p, nisyscfg.enums.PropertyType.String)

    def set_timestamp_property(self, id, value):
        raise NotImplementedError


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
        resource_handle = nisyscfg.types.ResourceHandle()
        error_code = self._library.NextResource(self._session, self._handle, ctypes.pointer(resource_handle))
        if error_code == 1:
            raise StopIteration()
        nisyscfg.errors.handle_error(self, error_code)
        resource = HardwareResource(resource_handle, self._library)
        self._children.append(resource)
        return resource

    def close(self):
        self._children.reverse()
        for child in self._children:
            child.close()
        if self._handle:
            error_code = self._library.CloseHandle(self._handle)
            nisyscfg.errors.handle_error(self, error_code)
            self._handle = None

    def next(self):
        return self.__next__()


class _NoDefault(object):
    pass


class HardwareResource(object):
    def __init__(self, handle, library):
        self.__dict__['_handle'] = handle
        self.__dict__['_library'] = library

    def __del__(self):
        self.close()

    def close(self):
        if self._handle:
            error_code = self._library.CloseHandle(self._handle)
            nisyscfg.errors.handle_error(self, error_code)
            self._handle = None

    def _get_resource_property(self, id, c_type):
        if c_type == ctypes.c_char_p:
            value = nisyscfg.types.simple_string()
            value_arg = value
        elif issubclass(c_type, nisyscfg.enums.CtypesEnum):
            value = ctypes.c_int()
            value_arg = ctypes.pointer(value)
        else:
            value = c_type(0)
            value_arg = ctypes.pointer(value)

        error_code = self._library.GetResourceProperty(self._handle, id, value_arg)
        nisyscfg.errors.handle_error(self, error_code)

        if issubclass(c_type, nisyscfg.enums.CtypesEnum):
            return c_type(value.value)

        return c_string_decode(value.value)

    def _get_resource_indexed_property(self, id, index, c_type):
        if c_type == ctypes.c_char_p:
            value = nisyscfg.types.simple_string()
            value_arg = value
        elif issubclass(c_type, nisyscfg.enums.CtypesEnum):
            value = ctypes.c_int()
            value_arg = ctypes.pointer(value)
        else:
            value = c_type()
            value_arg = ctypes.pointer(value)

        error_code = self._library.GetResourceIndexedProperty(self._handle, id, index, value_arg)
        nisyscfg.errors.handle_error(self, error_code)

        if issubclass(c_type, nisyscfg.enums.CtypesEnum):
            return c_type(value.value)

        return c_string_decode(value.value)

    def __getitem__(self, tag):
        return tag.get(self)

    def get_property(self, tag, default=_NoDefault()):
        try:
            return self[tag]
        except nisyscfg.errors.LibraryError as err:
            if err.code != nisyscfg.errors.Status.PropDoesNotExist or isinstance(default, _NoDefault):
                raise
            return default

    def get_bool_property(self, id):
        return self._get_resource_property(id, nisyscfg.enums.Bool)

    def get_int_property(self, id):
        return self._get_resource_property(id, ctypes.c_int)

    def get_unsigned_int_property(self, id):
        return self._get_resource_property(id, ctypes.c_uint)

    def get_double_property(self, id):
        return self._get_resource_property(id, ctypes.c_double)

    def get_string_property(self, id):
        return self._get_resource_property(id, ctypes.c_char_p)

    def get_timestamp_property(self, id):
        raise NotImplementedError

    def get_indexed_bool_property(self, id, index):
        return self._get_resource_indexed_property(id, index, nisyscfg.enums.Bool)

    def get_indexed_int_property(self, id, index):
        return self._get_resource_indexed_property(id, index, ctypes.c_int)

    def get_indexed_unsigned_int_property(self, id, index):
        return self._get_resource_indexed_property(id, index, ctypes.c_uint)

    def get_indexed_double_property(self, id, index):
        return self._get_resource_indexed_property(id, index, ctypes.c_double)

    def get_indexed_string_property(self, id, index):
        return self._get_resource_indexed_property(id, index, ctypes.c_char_p)

    def get_indexed_timestamp_property(self, id, index):
        raise NotImplementedError

    def _set_property(self, id, value, c_type):
        if c_type == ctypes.c_char_p:
            value = c_string_encode(value)
        elif issubclass(c_type, nisyscfg.enums.CtypesEnum):
            value = ctypes.c_int(value)
        else:
            value = c_type(value)

        error_code = self._library.SetResourceProperty(self._handle, id, value)
        nisyscfg.errors.handle_error(self, error_code)

    def __setitem__(self, tag, value):
        tag.set(self, value)

    def set_bool_property(self, id, value):
        self._set_property(id, value, nisyscfg.enums.Bool)

    def set_int_property(self, id, value):
        self._set_property(id, value, ctypes.c_int)

    def set_unsigned_int_property(self, id, value):
        self._set_property(id, value, ctypes.c_uint)

    def set_double_property(self, id, value):
        self._set_property(id, value, ctypes.c_double)

    def set_string_property(self, id, value):
        self._set_property(id, value, ctypes.c_char_p)

    def set_timestamp_property(self, id, value):
        raise NotImplementedError

    def rename(self, new_name, overwrite_conflict=False, update_dependencies=False):
        error_code = self._library.RenameResource(
            self._handle,
            c_string_encode(new_name),
            overwrite_conflict,
            update_dependencies,
            None,
            None)
        nisyscfg.errors.handle_error(self, error_code)

    def reset(self, mode=0):
        error_code = self._library.ResetHardware(self._handle, mode)
        nisyscfg.errors.handle_error(self, error_code)

    def save_changes(self):
        restart_required = ctypes.c_int()
        error_code = self._library.SaveResourceChanges(self._handle, restart_required, None)
        nisyscfg.errors.handle_error(self, error_code)
        return restart_required.value != 0

    def self_test(self, mode=0):
        error_code = self._library.SelfTestHardware(self._handle, mode, None)
        nisyscfg.errors.handle_error(self, error_code)

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

        nisyscfg.errors.handle_error(self, error_code)


class ComponentInfoIterator(object):
    def __init__(self, handle, library):
        self._handle = handle
        self._library = library

    def __del__(self):
        self.close()

    def __iter__(self):
        return self

    def __next__(self):
        id = nisyscfg.types.simple_string()
        version = nisyscfg.types.simple_string()
        title = nisyscfg.types.simple_string()
        item_type = nisyscfg.types.ctypes.c_long()
        error_code = self._library.NextComponentInfo(self._handle, id, version, title, ctypes.pointer(item_type), None)
        if error_code == 1:
            raise StopIteration()
        nisyscfg.errors.handle_error(self, error_code)
        return {
            'id': c_string_decode(id.value),
            'version': c_string_decode(version.value),
            'title': c_string_decode(title.value),
            'type': nisyscfg.types.ComponentType(item_type.value),
            'details': None,  # TODO(tkrebes): Implement
        }

    def close(self):
        if self._handle:
            error_code = self._library.CloseHandle(self._handle)
            nisyscfg.errors.handle_error(self, error_code)
            self._handle = None

    def next(self):
        return self.__next__()
