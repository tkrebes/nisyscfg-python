import collections
import ctypes

import nisyscfg
import nisyscfg._library_singleton
import nisyscfg.properties
import nisyscfg.pxi.properties
import nisyscfg.xnet.properties

from nisyscfg._lib import c_string_decode
from nisyscfg._lib import c_string_encode


class _NoDefault(object):
    pass


class _Property(object):

    __slots__ = ('_property', )

    def __init__(self, property):
        self._property = property

    def __get__(self, instance, cls):
        return self._property.get(instance._property_bag)

    def __set__(self, instance, value):
        return self._property.set(instance._property_bag, value)

    def __delete__(self, instance):
        raise NotImplementedError


class _Expert(object):

    def __init__(self, *property_groups):
        class _ExpertPropertyBag(object):
            def __init__(self, property_bag):
                self._property_bag = property_bag
        self._expert = _PropertyBag(*property_groups)(_ExpertPropertyBag)

    def __get__(self, instance, cls):
        return self._expert(instance._property_bag)

    def __set__(self, instance, value):
        raise NotImplementedError

    def __delete__(self, instance):
        raise NotImplementedError


class _PropertyBag(object):

    def __init__(self, *property_groups, expert=None):
        self._property_groups = property_groups
        self._expert = expert

    def __call__(self, session):
        if self._expert:
            setattr(session, self._expert, _Expert(*self._property_groups))
        else:
            for group in self._property_groups:
                for prop in dir(group):
                    if not prop.startswith('_'):
                        setattr(session, prop.lower(), _Property(getattr(group, prop)))
        return session


@_PropertyBag(nisyscfg.properties.System)
class Session(object):
    """
    Initializes a system configuration session with a specific system.

    This function communicates to the device at the specified address. If the
    device is no longer online, but it has previously been discovered in
    Measurement & Automation Explorer (MAX), this function succeeds, allowing
    you to retrieve cached information about the device.

    target - Specifies the IP address (ex. "224.102.13.24" ), MAC address
    (ex. "00:80:12:34:56:AB" ), or DNS name (ex. "myhost" ) of the target on a
    local or Real-Time system. The target defaults to the local system. Values
    such as a None, an empty string, and the strings localhost or 127.0.0.1
    also mean the local system.

    username - Specifies the username for the system you are initializing.
    Leave this parameter None if your target is running LabWindows/CVI 2009
    Real-Time Module or earlier or if you are connecting to the local
    system.

    password - Specifies the password for the system you are initializing.
    Leave this parameter None if no password has been set or if you are
    connecting to the local system.

    language - Specifies the language.
    ================== =========================================================
    Language           Description
    ------------------ ---------------------------------------------------------
    DEFAULT            Automatically chooses the language based on local
                       Windows settings.
    ENGLISH            English
    FRENCH             French
    GERMAN             German
    JAPANESE           Japanese
    KOREAN             Korean
    CHINESE_SIMPLIFIED Simplified Chinese
    ================== =========================================================

    force_property_refresh - Forces properties to be refreshed every time they
    are read by default. If FALSE, properties are queried once and cached in
    memory, which can optimize performance.

    timeout - Specifies the time, in milliseconds, that the function waits
    before the operation times out. When the operation succeeds, the session
    handle that is returned is set to the default, which is defined as
    300000 (5 minutes).

    Raises an nisyscfg.errors.LibraryError exception in the event of an error.
    """

    def __init__(self, target=None, username=None, password=None, language=nisyscfg.enums.Locale.DEFAULT, force_property_refresh=True, timeout=60000):
        self._children = []
        self._session = nisyscfg.types.SessionHandle()
        self._library = nisyscfg._library_singleton.get()
        self._property_bag = nisyscfg.properties.PropertyBag(
            setter=self._set_property,
            getter=self._get_property,
        )
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

    @property
    def resource(self):
        """System resource properties"""
        if not hasattr(self, '_resource'):
            resource_handle = self._get_property(16941086, nisyscfg.types.ResourceHandle)
            self._resource = HardwareResource(resource_handle, self._library)
            self._children.append(self._resource)
        return self._resource

    def _get_property(self, id, c_type):
        if c_type == ctypes.c_char_p:
            value = nisyscfg.types.simple_string()
            value_arg = value
        elif issubclass(c_type, nisyscfg.enums.BaseEnum):
            value = ctypes.c_int()
            value_arg = ctypes.pointer(value)
        else:
            value = c_type(0)
            value_arg = ctypes.pointer(value)

        error_code = self._library.GetSystemProperty(self._session, id, value_arg)
        nisyscfg.errors.handle_error(self, error_code)

        if issubclass(c_type, nisyscfg.enums.BaseEnum):
            return c_type(value.value)

        return c_string_decode(value.value)

    def get_property(self, tag, default=_NoDefault()):
        """
        Returns value of system property

        Return the value for system property specified by the tag, else default.
        If default is not given and the property does not exist, this function
        raises an nisyscfg.errors.LibraryError exception.
        """
        try:
            return self[tag]
        except nisyscfg.errors.LibraryError as err:
            if err.code != nisyscfg.errors.Status.PROP_DOES_NOT_EXIST or isinstance(default, _NoDefault):
                raise
            return default

    def _set_property(self, id, value, c_type, nisyscfg_type):
        if c_type == ctypes.c_char_p:
            value = c_string_encode(value)
        elif issubclass(c_type, nisyscfg.enums.BaseEnum):
            value = ctypes.c_int(value)
        else:
            value = c_type(value)

        error_code = self._library.SetSystemProperty(self._session, id, value)
        nisyscfg.errors.handle_error(self, error_code)

    def save_changes(self):
        """
        Saves changes made to systems.

        Returns tuple (restart_required, result)

            restart_required - Specifies whether the changes require a reboot.
            If TRUE, call restart().

            result - A string containing results of any errors that may have
            occurred during execution.

        Raises an nisyscfg.errors.LibraryError exception in the event of an
        error.
        """
        restart_required = ctypes.c_int()
        c_detailed_description = ctypes.POINTER(ctypes.c_char)()
        error_code = self._library.SaveSystemChanges(self._session, restart_required, ctypes.pointer(c_detailed_description))
        if c_detailed_description:
            detailed_description = c_string_decode(ctypes.cast(c_detailed_description, ctypes.c_char_p).value)
            error_code_2 = self._library.FreeDetailedString(c_detailed_description)
        nisyscfg.errors.handle_error(self, error_code)
        nisyscfg.errors.handle_error(self, error_code_2)
        return restart_required.value != 0, detailed_description


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


@_PropertyBag(nisyscfg.properties.Filter)
@_PropertyBag(nisyscfg.xnet.properties.Filter, expert='xnet')
class Filter(object):
    def __init__(self, session, library):
        self._handle = nisyscfg.types.FilterHandle()
        self._library = library
        self._property_bag = nisyscfg.properties.PropertyBag(setter=self._set_property_with_type)
        error_code = self._library.CreateFilter(session, ctypes.pointer(self._handle))
        nisyscfg.errors.handle_error(self, error_code)

    def __del__(self):
        self.close()

    def close(self):
        if self._handle:
            error_code = self._library.CloseHandle(self._handle)
            nisyscfg.errors.handle_error(self, error_code)
            self._handle = None

    def _set_property_with_type(self, id, value, c_type, nisyscfg_type):
        if c_type == ctypes.c_char_p:
            value = c_string_encode(value)
        elif issubclass(c_type, nisyscfg.enums.BaseEnum):
            value = ctypes.c_int(value)
        else:
            value = c_type(value)

        error_code = self._library.SetFilterPropertyWithType(self._handle, id, nisyscfg_type, value)
        nisyscfg.errors.handle_error(self, error_code)


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


@_PropertyBag(nisyscfg.properties.Resource, nisyscfg.properties.IndexedResource)
@_PropertyBag(nisyscfg.pxi.properties.Resource, nisyscfg.pxi.properties.IndexedResource, expert='pxi')
@_PropertyBag(nisyscfg.xnet.properties.Resource, expert='xnet')
class HardwareResource(object):
    def __init__(self, handle, library):
        self._handle = handle
        self._library = library
        self._property_bag = nisyscfg.properties.PropertyBag(
            setter=self._set_property,
            getter=self._get_property,
            indexed_getter=self._get_indexed_property
        )

    def __del__(self):
        self.close()

    def __repr__(self):
        return 'HardwareResource(name={})'.format(self.name)

    @property
    def name(self):
        """
        Returns a name that identifies a resource
        """
        name = self[nisyscfg.IndexedResourceProperties.EXPERT_USER_ALIAS][0]
        # If the resource doesn't have an alias, use the resource name instead
        if not name:
            name = self[nisyscfg.IndexedResourceProperties.EXPERT_RESOURCE_NAME][0]
        return name

    def close(self):
        """
        Closes reference to previously allocated resource.

        Raises an nisyscfg.errors.LibraryError exception in the event of an
        error.
        """
        if self._handle:
            error_code = self._library.CloseHandle(self._handle)
            nisyscfg.errors.handle_error(self, error_code)
            self._handle = None

    def _get_property(self, id, c_type):
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

    def _get_indexed_property(self, id, index, c_type):
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

    def get_property(self, tag, default=_NoDefault()):
        """
        Returns value of hardware resource property

        Return the value for hardware resource property specified by the tag,
        else default. If default is not given and the property does not exist,
        this function raises an nisyscfg.errors.LibraryError exception.
        """
        try:
            return self[tag]
        except nisyscfg.errors.LibraryError as err:
            if err.code != nisyscfg.errors.Status.PROP_DOES_NOT_EXIST or isinstance(default, _NoDefault):
                raise
            return default

    def _set_property(self, id, value, c_type, nisyscfg_type):
        if c_type == ctypes.c_char_p:
            value = c_string_encode(value)
        elif issubclass(c_type, nisyscfg.enums.BaseEnum):
            value = ctypes.c_int(value)
        else:
            value = c_type(value)

        error_code = self._library.SetResourceProperty(self._handle, id, value)
        nisyscfg.errors.handle_error(self, error_code)

    def rename(self, new_name, overwrite_conflict=False, update_dependencies=False):
        """
        Changes the display name of a resource.

        new_name - The user-specified new name for the resource.

        overwrite_conflict - Allows resource name changes to occur if there are
        any naming conflicts. If this value is True, the resource name change
        occurs even if another resource with the same name already exists. If
        this value is False (default), this function raises if another resource
        with the same name already exists. If this value is True and you choose
        a name that is already assigned to an existing resource, this function
        also changes the name of the existing resource.

        update_dependencies - Updates dependencies (for example: a task or
        channel) if the resource being renamed has them. Dependencies will be
        updated to refer to the new name by default. Select FALSE if you do not
        want to update these dependencies.
        Note: If overwrite_conflict is True and an existing resource was also
        renamed due to a conflict, the dependencies for that resource will not
        be updated. This option only affects the dependencies for the resource
        you are currently renaming.

        Returns HardwareResource whose name was overwritten. This will be None
        if no other resource was overwritten.

        Raises an nisyscfg.errors.LibraryError exception in the event of an
        error.
        """
        name_already_existed = ctypes.c_int()
        overwritten_resource_handle = nisyscfg.types.ResourceHandle()
        error_code = self._library.RenameResource(
            self._handle,
            c_string_encode(new_name),
            overwrite_conflict,
            update_dependencies,
            ctypes.pointer(name_already_existed),
            ctypes.pointer(overwritten_resource_handle))
        nisyscfg.errors.handle_error(self, error_code)

        # TODO(tkrebes): Ensure lifetime of HardwareResource does not exceed the
        # session.
        overwritten_resource = (
            overwritten_resource_handle.value
            and HardwareResource(overwritten_resource_handle, self._library)
        )

        # Do not return the bool 'name_already_existed' since it is equivalent
        # to 'overwritten_syscfg_resource == None'.
        return overwritten_resource

    def reset(self, mode=0):
        """
        Executes a reset on a specified resource.

        Raises an nisyscfg.errors.LibraryError exception in the event of an
        error.
        """
        error_code = self._library.ResetHardware(self._handle, mode)
        nisyscfg.errors.handle_error(self, error_code)

    def save_changes(self):
        """
        Writes and saves property changes on a device.

        Returns tuple (restart_required, detailed_description)

            restart_required - Specifies whether the changes require a reboot.
            If True, call restart.

            detailed_description - A string containing results of any errors
            that may have occurred during execution.

        Raises an nisyscfg.errors.LibraryError exception in the event of an
        error.
        """
        restart_required = ctypes.c_int()
        c_detailed_description = ctypes.POINTER(ctypes.c_char)()
        error_code = self._library.SaveResourceChanges(self._handle, restart_required, ctypes.pointer(c_detailed_description))
        if c_detailed_description:
            detailed_description = c_string_decode(ctypes.cast(c_detailed_description, ctypes.c_char_p).value)
            error_code_2 = self._library.FreeDetailedString(c_detailed_description)
        nisyscfg.errors.handle_error(self, error_code)
        nisyscfg.errors.handle_error(self, error_code_2)

        ReturnData = collections.namedtuple(
            'ReturnData',
            'restart_required detailed_description'
        )

        return ReturnData(restart_required.value != 0, detailed_description)

    def self_test(self, mode=0):
        """
        Verifies that system devices are able to perform basic I/O functions.

        No other tasks should run on the system while executing the self test
        because the driver may need exclusive access to some device resources.
        You do not need to disconnect devices from external equipment because
        the state of I/O lines are maintained throughout the test.

        mode - Reserved. This must be 0.

        Returns a string containing results of any errors that may have occurred
        during execution.

        Raises an nisyscfg.errors.LibraryError exception in the event of an
        error.
        """
        c_detailed_result = ctypes.POINTER(ctypes.c_char)()
        error_code = self._library.SelfTestHardware(self._handle, mode, ctypes.pointer(c_detailed_result))
        if c_detailed_result:
            detailed_result = c_string_decode(ctypes.cast(c_detailed_result, ctypes.c_char_p).value)
            error_code_2 = self._library.FreeDetailedString(c_detailed_result)
        nisyscfg.errors.handle_error(self, error_code)
        nisyscfg.errors.handle_error(self, error_code_2)
        return detailed_result

    def upgrade_firmware(self, version=None, filepath=None, auto_stop_task=True, force=False, sync_call=True):
        """
        Updates the firmware on the target.

        version - Specifies the firmware version you want to apply to the
        target. Use '0' to install the latest available firmware.

        filepath - Specifies the firmware file you want to upload to the target.

        Note: Parameters version and filepath are mutually exclusive and you
        must specify one and only one.

        auto_stop_task - Specifies to automatically end all tasks running on the
        target, even if they are incomplete and switch to firmware update mode.
        The default is True.

        force - Specifies to overwrite the destination firmware image even if
        the version is the same as or older than the version of the destination
        firmware image. If False, the function checks the version of the
        firmware returned by the expert and, if the returned version is newer
        than the version you are upgrading, this function returns an error. If
        the firmware version is the same and this parameter is set to False, the
        function does not upgrade the firmware and returns success. If True,
        this function automatically upgrades the firmware, regardless of the
        version of the destination firmware image. The default is False.

        sync_call - Specifies whether to wait for the upgrade operation to
        finish before returning. If False, the upgrade operation may continue
        running even after this function returns. To check the status, query
        the firmware_status property. The default is True.

        Returns tuple (status, detailed_result)

            status - The status of the firmware update. If this output returns
            FirmwareStatus.READY_PENDING_USER_RESTART, call restart. You can
            view more information about additional results in the
            detailed_result output.

            detailed_result - Results of any errors that may have occurred when
            this function completed. This output also may return additional
            information about the value returned from status.

        Raises an nisyscfg.errors.LibraryError exception in the event of an
        error.
        """
        if version and filepath:
            raise ValueError("version and filepath are mutually exclusive parameters")

        firmware_status = ctypes.c_int()
        c_detailed_result = ctypes.POINTER(ctypes.c_char)()
        if version:
            error_code = self._library.UpgradeFirmwareVersion(
                self._handle, c_string_encode(version), auto_stop_task, force, sync_call,
                ctypes.pointer(firmware_status), ctypes.pointer(c_detailed_result))
        elif filepath:
            error_code = self._library.UpgradeFirmwareFromFile(
                self._handle, c_string_encode(filepath), auto_stop_task, force, sync_call,
                ctypes.pointer(firmware_status), ctypes.pointer(c_detailed_result))
        else:
            raise ValueError("upgrade_firmware() requires either version or filepath to be specified")

        if c_detailed_result:
            detailed_result = c_string_decode(ctypes.cast(c_detailed_result, ctypes.c_char_p).value)
            error_code_2 = self._library.FreeDetailedString(c_detailed_result)
        nisyscfg.errors.handle_error(self, error_code)
        nisyscfg.errors.handle_error(self, error_code_2)

        ReturnData = collections.namedtuple(
            'ReturnData',
            'status detailed_result'
        )

        return ReturnData(
            nisyscfg.enums.FirmwareStatus(firmware_status.value),
            detailed_result
        )

    @property
    def firmware_status(self):
        """
        Returns the status of the firmware upgrade in progress.

        Returns tuple (percent_complete, status, detailed_result)

            percent_complete - The status, in percent, of the current step in
            the firmware upgrade. This parameter returns -1 if there is no
            firmware update in progress.

            status - The status of the firmware update. If this output
            returns FirmwareStatus.READY_PENDING_USER_RESTART, call restart. You
            can view more information about additional results in the
            detailed_result output.

            detailed_result - Results of any errors that may have occurred when
            this function completed. This output also may return additional
            information about the value returned from status.

        Raises an nisyscfg.errors.LibraryError exception in the event of an
        error.
        """
        percent_complete = ctypes.c_int()
        firmware_status = ctypes.c_int()
        c_detailed_result = ctypes.POINTER(ctypes.c_char)()
        error_code = self._library.CheckFirmwareStatus(
            self._handle, percent_complete, firmware_status, ctypes.pointer(c_detailed_result))
        if c_detailed_result:
            detailed_result = c_string_decode(ctypes.cast(c_detailed_result, ctypes.c_char_p).value)
            error_code_2 = self._library.FreeDetailedString(c_detailed_result)
        nisyscfg.errors.handle_error(self, error_code)
        nisyscfg.errors.handle_error(self, error_code_2)

        ReturnData = collections.namedtuple(
            'ReturnData',
            'percent_complete status detailed_result'
        )

        return ReturnData(
            percent_complete.value,
            nisyscfg.enums.FirmwareStatus(firmware_status.value),
            detailed_result,
        )

    def delete(self, mode=nisyscfg.enums.DeleteValidationMode.DELETE_IF_NO_DEPENDENCIES_EXIST):
        """
        Permanently removes a hardware resource and its configuration data from
        the system.

        Note: Not all devices can be deleted; consult your product documentation.

        mode - Specifies the conditions under which to delete the specified
        resource.
        ================================= ======================================
        Mode                              Description
        --------------------------------- --------------------------------------
        VALIDATE_BUT_DO_NOT_DELETE        Verify whether the resource can be
                                          deleted and whether it has
                                          dependencies.
        DELETE_IF_NO_DEPENDENCIES_EXIST   Delete the resource only if no
                                          dependencies exist. These could be
                                          tasks or child resources.
        DELETE_ITEM_AND_ANY_DEPENDENCIES  Delete this resource. If any
                                          dependencies exist, delete them too.
        DELETE_ITEM_BUT_KEEP_DEPENDENCIES Delete this resource. If any
                                          dependencies exist, leave them in an
                                          unusable state.
        ================================= ======================================

        Returns tuple (dependent_items_deleted, detailed_result)

            dependent_items_deleted - Returns whether resources other than the
            specified one were deleted. For example, this may happen if the
            resource is a simulated chassis that contained modules.

            detailed_result - A string containing results of any errors that may
            have occurred during execution.

        Raises an nisyscfg.errors.LibraryError exception in the event of an
        error.
        """
        dependent_items_deleted = ctypes.c_int()
        c_detailed_result = ctypes.POINTER(ctypes.c_char)()
        error_code = self._library.DeleteResource(
            self._handle, mode, dependent_items_deleted, ctypes.pointer(c_detailed_result))
        if c_detailed_result:
            detailed_result = c_string_decode(ctypes.cast(c_detailed_result, ctypes.c_char_p).value)
            error_code_2 = self._library.FreeDetailedString(c_detailed_result)
        nisyscfg.errors.handle_error(self, error_code)
        nisyscfg.errors.handle_error(self, error_code_2)

        ReturnData = collections.namedtuple(
            'ReturnData',
            'dependent_items_deleted detailed_result'
        )

        return ReturnData(dependent_items_deleted.value != 0, detailed_result)


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
