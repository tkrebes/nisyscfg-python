import ctypes

import nisyscfg
import nisyscfg._library_singleton
import nisyscfg.component_info
import nisyscfg.dependency_info
import nisyscfg.expert_info
import nisyscfg.filter
import nisyscfg.hardware_resource
import nisyscfg.properties
import nisyscfg.pxi.properties
import nisyscfg.software_feed
import nisyscfg.xnet.properties

from nisyscfg._lib import c_string_decode
from nisyscfg._lib import c_string_encode

from typing import NamedTuple, Union


class _NoDefault(object):
    pass


@nisyscfg.properties.PropertyBag(nisyscfg.properties.System)
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

    timeout - Specifies the time, in seconds, that the function waits before the
    operation times out. When the operation succeeds, the session handle that is
    returned is set to the default, which is defined as 300 (5 minutes).

    Raises an nisyscfg.errors.LibraryError exception in the event of an error.
    """

    def __init__(self, target=None, username=None, password=None, language=nisyscfg.enums.Locale.DEFAULT, force_property_refresh=True, timeout=300.0):
        self._children = []
        self._session = nisyscfg.types.SessionHandle()
        self._library = nisyscfg._library_singleton.get()
        self._property_accessor = nisyscfg.properties.PropertyAccessor(
            setter=self._set_property,
            getter=self._get_property,
        )
        error_code = self._library.InitializeSession(
            c_string_encode(target),
            c_string_encode(username),
            c_string_encode(password),
            language,
            force_property_refresh,
            int(timeout * 1000),
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
        iter = nisyscfg.expert_info.ExpertInfoIterator(expert_handle)
        self._children.append(iter)
        return iter

    def find_hardware(
        self,
        filter: Union[None, nisyscfg.filter.Filter] = None,
        mode: nisyscfg.enums.FilterMode = nisyscfg.enums.FilterMode.MATCH_VALUES_ALL,
        expert_names: str = ''
    ) -> nisyscfg.hardware_resource.HardwareResourceIterator:
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
        iter = nisyscfg.hardware_resource.HardwareResourceIterator(self._session, resource_handle)
        self._children.append(iter)
        return iter

    def create_filter(self) -> nisyscfg.filter.Filter:
        """
        Creates a hardware filter object that is used to query for specific
        resources in a system. After creating a filter, set one or more
        properties to limit the set of  detected resources.

        Raises an nisyscfg.errors.LibraryError exception in the event of an
        error.
        """
        filter = nisyscfg.filter.Filter(self._session)
        self._children.append(filter)
        return filter

    def restart(self, sync_call=True, install_mode=False, flush_dns=False, timeout=90.0):
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

        timeout - The time, in seconds, that the function waits to establish a
        connection before it returns an error. The default is 90 s.

        Returns the new IP address of the rebooted system. This IP address may
        differ from the previous IP address if the system acquires a different
        IP address from the DHCP server.

        Raises an nisyscfg.errors.LibraryError exception in the event of an
        error.
        """
        new_ip_address = nisyscfg.types.simple_string()
        error_code = self._library.Restart(self._session, sync_call, install_mode, flush_dns, int(timeout * 1000), new_ip_address)
        nisyscfg.errors.handle_error(self, error_code)
        return c_string_decode(new_ip_address.value)

    def get_filtered_base_system_images(
        self,
        repository_path: Union[None, str] = None,
        device_class: Union[None, str] = None,
        os: Union[None, str] = None,
        product_id: int = 0
    ) -> nisyscfg.component_info.ComponentInfoIterator:
        """
        Retrieves a collection of base system images available from a
        repository path.

        These include a base operating system and are intended to be used
        with format().

        repository_path - Specifies the location that contains installable
        components.

        device_class - Specifies the type of device for which you are
        searching. Common values are PXI and cRIO. To specify multiple classes,
        use a comma to separate the values.

        os - Specifies the operating system.

        product_id - Specifies the bus-specific product identifier code. This
        is not the product's sellable model number.

        Raises an nisyscfg.errors.LibraryError exception in the event of an
        error.
        """
        software_component_handle = nisyscfg.types.EnumSoftwareComponentHandle()
        error_code = self._library.GetFilteredBaseSystemImages(
            c_string_encode(repository_path),
            c_string_encode(device_class),
            c_string_encode(os),
            ctypes.c_uint(product_id),
            ctypes.pointer(software_component_handle))
        nisyscfg.errors.handle_error(self, error_code)
        if software_component_handle:
            iter = nisyscfg.component_info.ComponentInfoIterator(software_component_handle)
            self._children.append(iter)
            return iter

    def format(
        self,
        auto_restart: bool = True,
        file_system: nisyscfg.enums.FileSystemMode = nisyscfg.enums.FileSystemMode.DEFAULT,
        network_settings: nisyscfg.enums.NetworkInterfaceSettings = nisyscfg.enums.NetworkInterfaceSettings.RESET_PRIMARY_RESET_OTHERS,
        system_image_id: Union[None, str] = None,
        system_image_version: Union[None, str] = None,
        timeout: float = 90.0
    ) -> None:
        """
        Erases all data from the primary hard drive of a system and formats it
        with the base system image, network settings, and filesystem specified.
        The operation will fail if you choose not to restart the target
        automatically and the target's boot flow requires it to be in safe mode
        or restart after the operation. Refer to the the definition of safe
        mode to understand the differences between safe mode for different
        target boot flows. This function can only be used to format Real-Time
        systems.

        auto_restart - Restarts the system before and/or after the operation as
        required by the target's boot flow. The operation will fail if you
        choose not to restart the target automatically and the target's boot
        flow requires it to be in safe mode or restart after the operation.

        file_system - Formats the primary hard drive into a user-selected file
        system. Not all systems support all modes.
        ========= ==============================================================
        Mode      Description
        --------- --------------------------------------------------------------
        DEFAULT   Formats the hard drive into the default format. The default
                  is whatever format the existing target is already in.
        FAT       Formats the hard drive with the File Allocation Table (FAT)
                  file system.
        RELIANCE  Formats the hard drive with the Reliance file system. Reliance
                  is a transactional file system, developed by Datalight, that
                  is tolerant to crashes and power interruptions.
        UBIFS     Formats the hard drive with the Unsorted Block Image File
                  System (UBIFS).
        EXT4      Formats the hard drive with the Ext4 file system.
        ========= ==============================================================

        network_settings - Resets the primary network adapter and disables
        secondary adapters by default.
        ================================ =======================================
        Mode                             Description
        -------------------------------- ---------------------------------------
        RESET_PRIMARY_RESET_OTHERS       Resets the primary network adapter to
                                         factory settings and disables all other
                                         network adapters.
        PRESERVE_PRIMARY_RESET_OTHERS    Preserves the existing settings on the
                                         primary network adapter and disables
                                         all other network adapters. This option
                                         may not be supported for targets on a
                                         remote subnet.
        PRESERVE_PRIMARY_PRESERVE_OTHERS Preserves the settings for all network
                                         adapters. This option may not be
                                         supported for targets on a remote
                                         subnet.
        ================================ =======================================

        system_image_id - The system image ID.

        system_image_version - The system image version.

        timeout - The time, in seconds, that the function waits for the format
        to time out. The default is 90 s. If restart after format is TRUE, the
        default increases by 90 s. If the system is not in safe mode, the
        default increases by another 90 s.

        Raises an nisyscfg.errors.LibraryError exception in the event of an
        error.
        """
        error_code = self._library.FormatWithBaseSystemImage(
            self._session,
            nisyscfg.enums.Bool(auto_restart),
            file_system,
            network_settings,
            c_string_encode(system_image_id),
            c_string_encode(system_image_version),
            ctypes.c_uint(int(timeout * 1000)))
        nisyscfg.errors.handle_error(self, error_code)

    def get_available_software_components(
        self,
        item_types: nisyscfg.enums.IncludeComponentTypes = nisyscfg.enums.IncludeComponentTypes.ALL_VISIBLE
    ) -> nisyscfg.component_info.ComponentInfoIterator:
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
            iter = nisyscfg.component_info.ComponentInfoIterator(software_component_handle)
            self._children.append(iter)
            return iter

    def get_installed_software_components(
        self,
        item_types: nisyscfg.enums.IncludeComponentTypes = nisyscfg.enums.IncludeComponentTypes.ALL_VISIBLE,
        cached: bool = False
    ) -> nisyscfg.component_info.ComponentInfoIterator:
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
            iter = nisyscfg.component_info.ComponentInfoIterator(software_component_handle)
            self._children.append(iter)
            return iter

    def add_software_feed(self, name: str, uri: str, enabled: bool, trusted: bool):
        """
        Adds a software feed to the system.

        Note: This requires Secure Shell Server (sshd) to be enabled on the
        target.

        name - Name of the feed for identification purposes.

        uri - Location of the feed, such as "file://..." or "http://...". NI
        feeds often start with "http://download.ni.com/".

        enabled - Whether the feed is enabled.

        trusted - Whether the feed is trusted. A trusted feed will not be
        cryptographically verified by the package manager to be a safe and
        secure source of packages. Feeds are not trusted by default. A system
        administrator may have reason to trust the feed regardless.

        Raises an nisyscfg.errors.LibraryError exception in the event of an
        error.
        """
        error_code = self._library.AddSoftwareFeed(
            self._session,
            c_string_encode(name),
            c_string_encode(uri),
            nisyscfg.enums.Bool(enabled),
            nisyscfg.enums.Bool(trusted))
        nisyscfg.errors.handle_error(self, error_code)

    def modify_software_feed(self, old_name: str, new_name: str, uri: str, enabled: bool, trusted: bool):
        """
        Modifies an existing software feed by name.

        Note: This requires Secure Shell Server (sshd) to be enabled on the
        target.

        old_name - Name of the feed to modify. This feed must exist on the system.

        new_name - New name of the feed. This feed must not exist on the
        system. If not specified, the feed name will remain unchanged.

        uri - New location of the feed, such as "file://..." or "http://...".
        NI feeds often start with "http://download.ni.com/".

        enabled - New enabled state.

        trusted - New trusted state. A trusted feed will not be
        cryptographically verified by the package manager to be a safe and
        secure source of packages. Feeds are not trusted by default. A system
        administrator may have reason to trust the feed regardless.

        Raises an nisyscfg.errors.LibraryError exception in the event of an
        error.
        """
        error_code = self._library.ModifySoftwareFeed(
            self._session,
            c_string_encode(old_name),
            c_string_encode(new_name),
            c_string_encode(uri),
            nisyscfg.enums.Bool(enabled),
            nisyscfg.enums.Bool(trusted))
        nisyscfg.errors.handle_error(self, error_code)

    def remove_software_feed(self, name: str):
        """
        Removes an existing software feed by name.

        Note: This requires Secure Shell Server (sshd) to be enabled on the
        target.

        name - Name of the feed to remove. This feed must exist on the system.

        Raises an nisyscfg.errors.LibraryError exception in the event of an
        error.
        """
        error_code = self._library.RemoveSoftwareFeed(self._session, c_string_encode(name))
        nisyscfg.errors.handle_error(self, error_code)

    def install_all(self, auto_restart: bool = True, deselect_conflicts: bool = True):
        """
        Installs software on a Real-Time system.

        auto_restart - Restarts the system into install mode by default before
        the operation is performed, and restarts back to a running state after
        the operation is complete. If you choose not to restart automatically,
        the operation will fail if the system is not already in install mode.

        deselect_conflicts - Indicates whether to deselect conflicting software
        components automatically. Select True to deselect the conflicting
        software components. If False, installation will fail if the system
        has conflicting software components.

        Returns tuple (installed_components, broken_dependencies)

            installed_components - An iterator to get information about each
            component that was just installed.

            broken_dependencies - An iterator to get a list of broken
            dependencies, which are specific software components that cannot
            operate without another software component installed.

        Raises an nisyscfg.errors.LibraryError exception in the event of an
        error.
        """
        installed_component_handle = nisyscfg.types.EnumSoftwareFeedHandle()
        broken_dependency_handle = nisyscfg.types.EnumDependencyHandle()
        error_code = self._library.InstallAll(
            self._session,
            auto_restart,
            deselect_conflicts,
            ctypes.pointer(installed_component_handle),
            ctypes.pointer(broken_dependency_handle))
        nisyscfg.errors.handle_error(self, error_code)

        ReturnValue = NamedTuple(
            "ReturnValue", [
                ('installed_components', nisyscfg.component_info.ComponentInfoIterator),
                ('broken_dependencies', nisyscfg.dependency_info.DependencyInfoIterator),
            ]
        )

        result = ReturnValue(
            installed_components=nisyscfg.component_info.ComponentInfoIterator(installed_component_handle),
            broken_dependencies=nisyscfg.dependency_info.DependencyInfoIterator(broken_dependency_handle),
        )

        self._children.append(result.installed_components)
        self._children.append(result.broken_dependencies)

        return result

    def get_software_feeds(self) -> nisyscfg.software_feed.SoftwareFeedIterator:
        """
        Retrieves a list of configured software feeds. A feed represents a
        location that the package manager uses to find and download available
        software.

        Note: This requires Secure Shell Server (sshd) to be enabled on the
        target.

        Raises an nisyscfg.errors.LibraryError exception in the event of an
        error.
        """
        software_feed_handle = nisyscfg.types.EnumSoftwareFeedHandle()
        error_code = self._library.GetSoftwareFeeds(self._session, ctypes.pointer(software_feed_handle))
        nisyscfg.errors.handle_error(self, error_code)
        if software_feed_handle:
            iter = nisyscfg.software_feed.SoftwareFeedIterator(software_feed_handle)
            self._children.append(iter)
            return iter

    @property
    def resource(self) -> nisyscfg.hardware_resource.HardwareResource:
        """System resource properties"""
        if not hasattr(self, '_resource'):
            resource_handle = self._get_property(16941086, nisyscfg.types.ResourceHandle)
            self._resource = nisyscfg.hardware_resource.HardwareResource(resource_handle)
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
