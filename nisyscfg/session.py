import ctypes

import nisyscfg
import nisyscfg._library_singleton

from nisyscfg._lib import c_string_decode
from nisyscfg._lib import c_string_encode


class Session(object):
    def __init__(self, target=None, username=None, password=None, language=nisyscfg.enums.Locale.DEFAULT, force_property_refresh=True, timeout=60000):
        """
        Initializes a system configuration session with a specific system.

        This function communicates to the device at the specified address. If
        the device is no longer online, but it has previously been discovered in
        Measurement & Automation Explorer (MAX), this function succeeds,
        allowing you to retrieve cached information about the device.

        target - Specifies the IP address (ex. "224.102.13.24" ), MAC address
        (ex. "00:80:12:34:56:AB" ), or DNS name (ex. "myhost" ) of the target on
        a local or Real-Time system. The target defaults to the local system.
        Values such as a None, an empty string, and the strings localhost or
        127.0.0.1 also mean the local system.

        username - Specifies the username for the system you are initializing.
        Leave this parameter None if your target is running LabWindows/CVI 2009
        Real-Time Module or earlier or if you are connecting to the local
        system.

        password - Specifies the password for the system you are initializing.
        Leave this parameter None if no password has been set or if you are
        connecting to the local system.

        language - Specifies the language.
        ================== =====================================================
        Language           Description
        ------------------ -----------------------------------------------------
        DEFAULT            Automatically chooses the language based on local
                           Windows settings.
        ENGLISH            English
        FRENCH             French
        GERMAN             German
        JAPANESE           Japanese
        KOREAN             Korean
        CHINESE_SIMPLIFIED Simplified Chinese
        ================== =====================================================

        force_property_refresh - Forces properties to be refreshed every time
        they are read by default. If FALSE, properties are queried once and
        cached in memory, which can optimize performance.

        timeout - Specifies the time, in milliseconds, that the function waits
        before the operation times out. When the operation succeeds, the session
        handle that is returned is set to the default, which is defined as
        300000 (5 minutes).

        Raises an nisyscfg.errors.LibraryError exception in the event of an
        error.
        """
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
        """
        Closes references to previously allocated session, filters, resources,
        and enumerators.

        Raises an nisyscfg.errors.LibraryError exception in the event of an
        error.
        """
        self._children.reverse()
        for child in self._children:
            child.close()
        if self._session:
            error_code = self._library.CloseHandle(self._session)
            nisyscfg.errors.handle_error(self, error_code)
            self._session = None

    def get_system_experts(self, expert_names=''):
        """
        Returns the experts available on the system.

        expert_names - This is a case-insensitive comma-separated string
        specifying which experts to query. If None or empty string, all
        supported experts are queried.

        Raises an nisyscfg.errors.LibraryError exception in the event of an
        error.
        """
        expert_handle = nisyscfg.types.EnumExpertHandle()
        if isinstance(expert_names, list):
            expert_names = ','.join(expert_names)
        error_code = self._library.GetSystemExperts(self._session, c_string_encode(expert_names), ctypes.pointer(expert_handle))
        nisyscfg.errors.handle_error(self, error_code)
        iter = ExpertInfoIterator(expert_handle, self._library)
        self._children.append(iter)
        return iter

    def find_hardware(self, filter=None, mode=nisyscfg.enums.FilterMode.MATCH_VALUES_ALL, expert_names=''):
        """
        Returns an iterator of hardware in a specified system.

        filter - Specifies a filter you can use to limit the results to hardware
        matching specific properties. The default is no filter.

        mode - The enumerated list of filter modes.
        ==================== ===================================================
        Mode                 Description
        -------------------- ---------------------------------------------------
        MATCH_VALUES_ALL     (default) includes all of the properties specified
                             in the input filter.
        MATCH_VALUES_ANY     includes any of the properties specified in the
                             input filter.
        MATCH_VALUES_NONE    includes none of the properties specified in the
                             input filter.
        ALL_PROPERTIES_EXIST includes all of the properties specified in the
                             input filter, regardless of the value of each
                             property.
        ==================== ===================================================

        expert_names - This is a case-insensitive comma-separated string
        specifying which experts to query. If None or empty-string, all
        supported experts are queried.

        Raises an nisyscfg.errors.LibraryError exception in the event of an
        error.
        """
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
        """
        Creates a hardware filter object that is used to query for specific
        resources in a system. After creating a filter, set one or more
        properties to limit the set of  detected resources.

        Raises an nisyscfg.errors.LibraryError exception in the event of an
        error.
        """
        filter = Filter(self._session, self._library)
        self._children.append(filter)
        return filter

    def restart(self, sync_call=True, install_mode=False, flush_dns=False, timeout=90000):
        """
        Reboots a system or network device.

        sync_call - Waits until the reboot has finished before the function
        operation is completed, by default. Select FALSE to not wait until the
        reboot is finished before the function completes its operation.

        install_mode - Does not reboot the system into install mode by default.
        To reboot into install mode, select TRUE. The default is FALSE, reboot
        into normal mode.

        flush_dns - Does not clear the DNS cache by default. DNS clients
        temporarily store system hostnames. Flushing the DNS allows you to clear
        those names from memory. This parameter applies to the local Windows
        system.

        timeout - The time, in milliseconds, that the function waits to
        establish a connection before it returns an error. The default is
        90,000 ms (90 s).

        Returns the new IP address of the rebooted system. This IP address may
        differ from the previous IP address if the system acquires a different
        IP address from the DHCP server.

        Raises an nisyscfg.errors.LibraryError exception in the event of an
        error.
        """
        new_ip_address = nisyscfg.types.simple_string()
        error_code = self._library.Restart(self._session, sync_call, install_mode, flush_dns, timeout, new_ip_address)
        nisyscfg.errors.handle_error(self, error_code)
        return c_string_decode(new_ip_address.value)

    def get_available_software_components(self, item_types=nisyscfg.enums.IncludeComponentTypes.ALL_VISIBLE):
        """
        Retrieves a list of software components on the local system that are
        available for installation to the specified target.

        item_types - Allows inclusion of hidden software installed on the target
        when ALL_VISIBLE_AND_HIDDEN is selected. Hidden software is not listed
        by default.
        ====================== =================================================
        Item Types             Description
        ---------------------- -------------------------------------------------
        ALL_VISIBLE            Specifies to return all visible software
                               components. This includes all standard, startup,
                               and essential components.
        ALL_VISIBLE_AND_HIDDEN Specifies to return all visible and hidden
                               software components.
        ONLY_STANDARD          Specifies to only return standard software
                               components.
        ONLY_STARTUP           Specifies to only return components that are
                               startup applications.
        ====================== =================================================

        Raises an nisyscfg.errors.LibraryError exception in the event of an
        error.
        """
        software_component_handle = nisyscfg.types.EnumSoftwareComponentHandle()
        error_code = self._library.GetAvailableSoftwareComponents(self._session, item_types, ctypes.pointer(software_component_handle))
        nisyscfg.errors.handle_error(self, error_code)
        if software_component_handle:
            iter = ComponentInfoIterator(software_component_handle, self._library)
            self._children.append(iter)
            return iter

    def get_installed_software_components(self, item_types=nisyscfg.enums.IncludeComponentTypes.ALL_VISIBLE, cached=False):
        """
        Retrieves a list of software components installed on a system.

        item_types - Allows inclusion of hidden software installed on the target
        when ALL_VISIBLE_AND_HIDDEN is selected. Hidden software is not listed
        by default.
        ====================== =================================================
        Item Types             Description
        ---------------------- -------------------------------------------------
        ALL_VISIBLE            Specifies to return all visible software
                               components. This includes all standard, startup,
                               and essential components.
        ALL_VISIBLE_AND_HIDDEN Specifies to return all visible and hidden
                               software components.
        ONLY_STANDARD          Specifies to only return standard software
                               components.
        ONLY_STARTUP           Specifies to only return components that are
                               startup applications.
        ====================== =================================================

        cached - Returns information that has already been read from the
        specified real-time system if TRUE. The system is contacted again for
        the information by default.

        Raises an nisyscfg.errors.LibraryError exception in the event of an
        error.
        """
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
        elif issubclass(c_type, nisyscfg.enums.BaseEnum):
            value = ctypes.c_int(value)
        else:
            value = c_type(value)

        error_code = self._library.SetFilterPropertyWithType(self._handle, id, nisyscfg_type, value)
        nisyscfg.errors.handle_error(self, error_code)

    def __setitem__(self, tag, value):
        tag.set(self, value)

    def set_bool_property(self, id, value):
        self._set_property(id, value, nisyscfg.enums.Bool, nisyscfg.enums.PropertyType.BOOL)

    def set_int_property(self, id, value):
        self._set_property(id, value, ctypes.c_int, nisyscfg.enums.PropertyType.INT)

    def set_unsigned_int_property(self, id, value):
        self._set_property(id, value, ctypes.c_uint, nisyscfg.enums.PropertyType.UNSIGNED_INT)

    def set_double_property(self, id, value):
        self._set_property(id, value, ctypes.c_double, nisyscfg.enums.PropertyType.DOUBLE)

    def set_string_property(self, id, value):
        self._set_property(id, value, ctypes.c_char_p, nisyscfg.enums.PropertyType.STRING)

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
        elif issubclass(c_type, nisyscfg.enums.BaseEnum):
            value = ctypes.c_int()
            value_arg = ctypes.pointer(value)
        else:
            value = c_type(0)
            value_arg = ctypes.pointer(value)

        error_code = self._library.GetResourceProperty(self._handle, id, value_arg)
        nisyscfg.errors.handle_error(self, error_code)

        if issubclass(c_type, nisyscfg.enums.BaseEnum):
            return c_type(value.value)

        return c_string_decode(value.value)

    def _get_resource_indexed_property(self, id, index, c_type):
        if c_type == ctypes.c_char_p:
            value = nisyscfg.types.simple_string()
            value_arg = value
        elif issubclass(c_type, nisyscfg.enums.BaseEnum):
            value = ctypes.c_int()
            value_arg = ctypes.pointer(value)
        else:
            value = c_type()
            value_arg = ctypes.pointer(value)

        error_code = self._library.GetResourceIndexedProperty(self._handle, id, index, value_arg)
        nisyscfg.errors.handle_error(self, error_code)

        if issubclass(c_type, nisyscfg.enums.BaseEnum):
            return c_type(value.value)

        return c_string_decode(value.value)

    def __getitem__(self, tag):
        return tag.get(self)

    def get_property(self, tag, default=_NoDefault()):
        try:
            return self[tag]
        except nisyscfg.errors.LibraryError as err:
            if err.code != nisyscfg.errors.Status.PROP_DOES_NOT_EXIST or isinstance(default, _NoDefault):
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
        elif issubclass(c_type, nisyscfg.enums.BaseEnum):
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
