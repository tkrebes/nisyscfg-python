"""System session classes."""

import ctypes
import pathlib
import tempfile
import zipfile
from contextlib import ExitStack
from typing import Any, List, NamedTuple, Optional, Protocol, Type, Union

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
import nisyscfg.system_info
import nisyscfg.xnet.properties
from nisyscfg._lib import c_string_decode, c_string_encode


class InstallAllResult(NamedTuple):
    """Result of install_all operation."""

    installed_components: nisyscfg.component_info.ComponentInfoIterator
    """Iterator of installed components."""
    broken_dependencies: nisyscfg.dependency_info.DependencyInfoIterator
    """Iterator of broken dependencies."""


class SaveChangesResult(NamedTuple):
    """Result of save_changes operation."""

    restart_required: bool
    """Indicates if a restart is required."""
    details: str
    """Details of the save changes operation."""


class _HasClose(Protocol):
    """Protocol for objects that have a close method."""

    def close(self) -> None:
        """Close the object."""
        ...


@nisyscfg.properties.PropertyBag(nisyscfg.properties.System)
class Session(object):
    """System configuration session with a specific system."""

    def __init__(
        self,
        target: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        language: nisyscfg.enums.Locale = nisyscfg.enums.Locale.DEFAULT,
        force_property_refresh: bool = True,
        timeout: float = 300.0,
    ) -> None:
        """Initializes a NI System Configuration session to specific system.

        This function communicates to the device at the specified address. If the
        device is no longer online, but it has previously been discovered in
        Measurement & Automation Explorer (MAX), this function succeeds, allowing
        you to retrieve cached information about the device.

        Args:
            target (str, optional): Specifies the IP address (ex. "224.102.13.24" ), MAC address
                (ex. "00:80:12:34:56:AB" ), or DNS name (ex. "myhost" ) of the target on a
                local or Real-Time system. The target defaults to the local system. Values
                such as a None, an empty string, and the strings localhost or 127.0.0.1
                also mean the local system.

            username (str, optional): Specifies the username for the system you are initializing.
                Leave this parameter None if your target is running LabWindows/CVI 2009
                Real-Time Module or earlier or if you are connecting to the local
                system.

            password (str, optional): Specifies the password for the system you are initializing.
                Leave this parameter None if no password has been set or if you are
                connecting to the local system.

            language (nisyscfg.enums.Locale, optional): Specifies the language.

            force_property_refresh (bool, optional): Forces properties to be refreshed every time
                they are read by default. If FALSE, properties are queried once and cached in
                memory, which can optimize performance.

            timeout (float, optional): Specifies the time, in seconds, that the function waits
                before the operation times out. When the operation succeeds, the session handle that
                is returned is set to the default, which is defined as 300 (5 minutes).

        Raises:
            nisyscfg.errors.LibraryError: In the event of an error.
        """
        self._children: List[_HasClose] = []
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
            ctypes.pointer(self._session),
        )
        nisyscfg.errors.handle_error(self, error_code)
        self.target_name = target

    def __del__(self) -> None:
        """Destructor to ensure the session is closed when the object is deleted."""
        self.close()

    def __enter__(self) -> "Session":
        """Enter the runtime context related to this object."""
        return self

    def __exit__(
        self,
        type: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[object],
    ) -> None:
        """Exit the runtime context related to this object."""
        self.close()

    def _get_status_description(self, status: Union[int, nisyscfg.errors.Status]) -> str:
        """Returns a detailed description of the status code."""
        c_detailed_description = ctypes.POINTER(ctypes.c_char)()
        error_code = self._library.GetStatusDescription(
            self._session, status, ctypes.pointer(c_detailed_description)
        )
        if c_detailed_description:
            detailed_description = c_string_decode(
                ctypes.cast(c_detailed_description, ctypes.c_char_p).value
            )
            error_code_2 = self._library.FreeDetailedString(c_detailed_description)
        nisyscfg.errors.handle_error(self, error_code, is_error_handling=True)
        nisyscfg.errors.handle_error(self, error_code_2, is_error_handling=True)
        return detailed_description

    def close(self) -> None:
        """Closes references to previously allocated session, filters, resources, and enumerators.

        Raises:
            nisyscfg.errors.LibraryError: In the event of an error.
        """
        self._children.reverse()
        for child in self._children:
            child.close()
        if self._session:
            error_code = self._library.CloseHandle(self._session)
            nisyscfg.errors.handle_error(self, error_code)
            self._session = nisyscfg.types.SessionHandle()

    def get_system_experts(self, expert_names: str = "") -> nisyscfg.expert_info.ExpertInfoIterator:
        """Returns the experts available on the system.

        Args:
            expert_names (str, optional): This is a case-insensitive comma-separated string
                specifying which experts to query. If None or empty string, all
                supported experts are queried.

        Raises:
            nisyscfg.errors.LibraryError: In the event of an error.
        """
        expert_handle = nisyscfg.types.EnumExpertHandle()
        if isinstance(expert_names, list):
            expert_names = ",".join(expert_names)
        error_code = self._library.GetSystemExperts(
            self._session, c_string_encode(expert_names), ctypes.pointer(expert_handle)
        )
        nisyscfg.errors.handle_error(self, error_code)
        iter = nisyscfg.expert_info.ExpertInfoIterator(expert_handle)
        self._children.append(iter)
        return iter

    def find_hardware(
        self,
        filter: Optional[nisyscfg.filter.Filter] = None,
        mode: nisyscfg.enums.FilterMode = nisyscfg.enums.FilterMode.MATCH_VALUES_ALL,
        expert_names: str = "",
    ) -> nisyscfg.hardware_resource.HardwareResourceIterator:
        """Returns an iterator of hardware in a specified system.

        Args:
            filter (nisyscfg.filter.Filter, optional): Specifies a filter you can use to limit the
                results to hardware matching specific properties. The default is no filter.

            mode (nisyscfg.enums.FilterMode, optional): The enumerated list of filter modes.

            expert_names (str, optional): This is a case-insensitive comma-separated string
                specifying which experts to query. If None or empty-string, all
                supported experts are queried.

        Raises:
            nisyscfg.errors.LibraryError: In the event of an error.
        """
        filter_handle = None if filter is None else filter._handle
        resource_handle = nisyscfg.types.EnumResourceHandle()
        if isinstance(expert_names, list):
            expert_names = ",".join(expert_names)
        error_code = self._library.FindHardware(
            self._session,
            mode,
            filter_handle,
            c_string_encode(expert_names),
            ctypes.pointer(resource_handle),
        )
        nisyscfg.errors.handle_error(self, error_code)
        iter = nisyscfg.hardware_resource.HardwareResourceIterator(self._session, resource_handle)
        self._children.append(iter)
        return iter

    def find_systems(
        self,
        device_class: str = "",
        detect_online_systems: bool = True,
        cache_mode: nisyscfg.enums.IncludeCachedResults = nisyscfg.enums.IncludeCachedResults.NONE,
        find_output_mode: nisyscfg.enums.SystemNameFormat = nisyscfg.enums.SystemNameFormat.HOSTNAME_IP,
        timeout: float = 4.0,
        only_installable_systems: bool = False,
    ) -> nisyscfg.system_info.SystemInfoIterator:
        """Retrieves systems on the network.

        Args:
            device_class (str, optional): Specifies the class of device for which you are
                searching. Common values are "PXI" and "cRIO". To specify multiple
                classes, use a comma to separate the values.

            detect_online_systems (bool, optional): Detects systems that are online. This option
                checks for all local online systems by default. You must set this
                parameter to TRUE on Real-Time targets. On Windows operating systems,
                set this parameter to FALSE if you only want to return previously
                detected results.

            cache_mode (nisyscfg.enums.IncludeCachedResults, optional): Specifies whether to
                include cached results.

            find_output_mode (nisyscfg.enums.SystemNameFormat, optional): Specifies the preferred
                output format of hostname and IP addresses for systems on the network. The
                Initialize function accepts all of these formats.

                Note: In some cases this parameter may return a system that is not in
                the requested format. For example, if you request the default
                HOSTNAME_IP but an unconfigured system is detected, that system is
                returned as IP_MAC.

            timeout (float, optional): The time, in seconds, the function waits before it times out.
                The default is 4 s. In some cases, the operation may take longer to
                time out.

            only_installable_systems (bool, optional): Detects only the systems that support the
                ability to install software remotely. This includes all Real-Time
                systems.

        Returns:
            nisyscfg.system_info.SystemInfoIterator: An iterator of system names in the format
            requested from the input parameter.

        Raises:
            nisyscfg.errors.LibraryError: In the event of an error.
        """
        system_handle = nisyscfg.types.EnumSystemHandle()
        error_code = self._library.FindSystems(
            self._session,
            c_string_encode(device_class),
            nisyscfg.enums.Bool(detect_online_systems),
            cache_mode,
            find_output_mode,
            int(timeout * 1000),
            nisyscfg.enums.Bool(only_installable_systems),
            ctypes.pointer(system_handle),
        )
        nisyscfg.errors.handle_error(self, error_code)

        return nisyscfg.system_info.SystemInfoIterator(system_handle)

    def create_filter(self) -> nisyscfg.filter.Filter:
        """Creates a hardware filter that is used to query for specific resources in a system.

        After creating a filter, set one or more properties to limit the set of  detected resources.

        Raises:
            nisyscfg.errors.LibraryError: In the event of an error.
        """
        filter = nisyscfg.filter.Filter(self._session)
        self._children.append(filter)
        return filter

    def restart(
        self,
        sync_call: bool = True,
        install_mode: bool = False,
        flush_dns: bool = False,
        timeout: float = 90.0,
    ) -> str:
        """Reboots a system or network device.

        Args:
            sync_call (bool, optional): Waits until the reboot has finished before the function
                operation is completed, by default. Select FALSE to not wait until the
                reboot is finished before the function completes its operation.

            install_mode (bool, optional): Does not reboot the system into install mode by default.
                To reboot into install mode, select TRUE. The default is FALSE, reboot
                into normal mode.

            flush_dns (bool, optional): Does not clear the DNS cache by default. DNS clients
                temporarily store system hostnames. Flushing the DNS allows you to clear
                those names from memory. This parameter applies to the local Windows
                system.

            timeout (float, optional): The time, in seconds, that the function waits to establish a
                connection before it returns an error. The default is 90 s.

        Returns:
            str: The new IP address of the rebooted system. This IP address may
            differ from the previous IP address if the system acquires a different
            IP address from the DHCP server.

        Raises:
            nisyscfg.errors.LibraryError: In the event of an error.
        """
        new_ip_address = nisyscfg.types.simple_string()
        error_code = self._library.Restart(
            self._session,
            sync_call,
            install_mode,
            flush_dns,
            int(timeout * 1000),
            new_ip_address,
        )
        nisyscfg.errors.handle_error(self, error_code)
        return c_string_decode(new_ip_address.value)

    def get_filtered_base_system_images(
        self,
        repository_path: Optional[str] = None,
        device_class: Optional[str] = None,
        os: Optional[str] = None,
        product_id: int = 0,
    ) -> nisyscfg.component_info.ComponentInfoIterator:
        """Retrieves a collection of base system images available from a repository path.

        These include a base operating system and are intended to be used with format().

        Args:
            repository_path (str, optional): Specifies the location that contains installable
                components.

            device_class (str, optional): Specifies the type of device for which you are
                searching. Common values are PXI and cRIO. To specify multiple classes,
                use a comma to separate the values.

            os (str, optional): Specifies the operating system.

            product_id (int, optional): Specifies the bus-specific product identifier code. This
                is not the product's sellable model number.

        Returns:
            nisyscfg.component_info.ComponentInfoIterator: An iterator of base system images.

        Raises:
            nisyscfg.errors.LibraryError: In the event of an error.
        """
        software_component_handle = nisyscfg.types.EnumSoftwareComponentHandle()
        error_code = self._library.GetFilteredBaseSystemImages(
            c_string_encode(repository_path),
            c_string_encode(device_class),
            c_string_encode(os),
            ctypes.c_uint(product_id),
            ctypes.pointer(software_component_handle),
        )
        nisyscfg.errors.handle_error(self, error_code)
        if software_component_handle:
            iter = nisyscfg.component_info.ComponentInfoIterator(software_component_handle)
            self._children.append(iter)
            return iter
        return nisyscfg.component_info.ComponentInfoIterator()

    def format(
        self,
        auto_restart: bool = True,
        file_system: nisyscfg.enums.FileSystemMode = nisyscfg.enums.FileSystemMode.DEFAULT,
        network_settings: nisyscfg.enums.NetworkInterfaceSettings = nisyscfg.enums.NetworkInterfaceSettings.RESET_PRIMARY_RESET_OTHERS,  # noqa: E501
        system_image_id: Optional[str] = None,
        system_image_version: Optional[str] = None,
        timeout: float = 90.0,
    ) -> None:
        """Formats the system.

        Erases all data from the primary hard drive of a system and formats it
        with the base system image, network settings, and filesystem specified.
        The operation will fail if you choose not to restart the target
        automatically and the target's boot flow requires it to be in safe mode
        or restart after the operation. Refer to the the definition of safe
        mode to understand the differences between safe mode for different
        target boot flows. This function can only be used to format Real-Time
        systems.

        Args:
            auto_restart (bool, optional): Restarts the system before and/or after the operation as
                required by the target's boot flow. The operation will fail if you
                choose not to restart the target automatically and the target's boot
                flow requires it to be in safe mode or restart after the operation.

            file_system (nisyscfg.enums.FileSystemMode, optional): Formats the primary hard drive
                into a user-selected file system. Not all systems support all modes.

            network_settings (nisyscfg.enums.NetworkInterfaceSettings, optional): Resets the primary
                network adapter and disables secondary adapters by default.

            system_image_id (str, optional): The system image ID.

            system_image_version (str, optional): The system image version.

            timeout (float, optional): The time, in seconds, that the function waits for the format
                to time out. The default is 90 s. If restart after format is TRUE, the
                default increases by 90 s. If the system is not in safe mode, the
                default increases by another 90 s.

        Raises:
            nisyscfg.errors.LibraryError: In the event of an error.
        """
        error_code = self._library.FormatWithBaseSystemImage(
            self._session,
            nisyscfg.enums.Bool(auto_restart),
            file_system,
            network_settings,
            c_string_encode(system_image_id),
            c_string_encode(system_image_version),
            ctypes.c_uint(int(timeout * 1000)),
        )
        nisyscfg.errors.handle_error(self, error_code)

    def get_available_software_components(
        self,
        item_types: nisyscfg.enums.IncludeComponentTypes = nisyscfg.enums.IncludeComponentTypes.ALL_VISIBLE,
    ) -> nisyscfg.component_info.ComponentInfoIterator:
        """Retrieves software components on the local system that are available for installation.

        Args:
            item_types (nisyscfg.enums.IncludeComponentTypes, optional): Allows inclusion of hidden
                software installed on the target when
                :attr:`nisyscfg.enums.IncludeComponentTypes.ALL_VISIBLE_AND_HIDDEN` is selected.
                Hidden software is not listed by default.

        Returns:
            nisyscfg.component_info.ComponentInfoIterator: An iterator of software components
            available for installation on the system.

        Raises:
            nisyscfg.errors.LibraryError: In the event of an error.
        """
        software_component_handle = nisyscfg.types.EnumSoftwareComponentHandle()
        error_code = self._library.GetAvailableSoftwareComponents(
            self._session, item_types, ctypes.pointer(software_component_handle)
        )
        nisyscfg.errors.handle_error(self, error_code)
        if software_component_handle:
            iter = nisyscfg.component_info.ComponentInfoIterator(software_component_handle)
            self._children.append(iter)
            return iter
        return nisyscfg.component_info.ComponentInfoIterator()

    def get_installed_software_components(
        self,
        item_types: nisyscfg.enums.IncludeComponentTypes = nisyscfg.enums.IncludeComponentTypes.ALL_VISIBLE,
        cached: bool = False,
    ) -> nisyscfg.component_info.ComponentInfoIterator:
        """Retrieves software components installed on a system.

        Args:
            item_types (nisyscfg.enums.IncludeComponentTypes, optional): Allows inclusion of hidden
                software installed on the target when
                :attr:`nisyscfg.enums.IncludeComponentTypes.ALL_VISIBLE_AND_HIDDEN` is selected.
                Hidden software is not listed by default.

            cached (bool, optional) Returns information that has already been read from the
                specified real-time system if TRUE. The system is contacted again for
                the information by default.


        Returns:
            nisyscfg.component_info.ComponentInfoIterator: An iterator of software components
            installed on the system.

        Raises:
            nisyscfg.errors.LibraryError: In the event of an error.
        """
        software_component_handle = nisyscfg.types.EnumSoftwareComponentHandle()
        error_code = self._library.GetInstalledSoftwareComponents(
            self._session, item_types, cached, ctypes.pointer(software_component_handle)
        )
        nisyscfg.errors.handle_error(self, error_code)
        if software_component_handle:
            iter = nisyscfg.component_info.ComponentInfoIterator(software_component_handle)
            self._children.append(iter)
            return iter
        return nisyscfg.component_info.ComponentInfoIterator()

    def add_software_feed(self, name: str, uri: str, enabled: bool, trusted: bool) -> None:
        """Adds a software feed to the system.

        Note: This requires Secure Shell Server (sshd) to be enabled on the
        target.

        Args:
            name (str): Name of the feed for identification purposes.

            uri (str): Location of the feed, such as "file://..." or "http://...". NI
                feeds often start with "http://download.ni.com/".

            enabled (bool): Whether the feed is enabled.

            trusted (bool): Whether the feed is trusted. A trusted feed will not be
                cryptographically verified by the package manager to be a safe and
                secure source of packages. Feeds are not trusted by default. A system
                administrator may have reason to trust the feed regardless.

        Raises:
            nisyscfg.errors.LibraryError: In the event of an error.
        """
        error_code = self._library.AddSoftwareFeed(
            self._session,
            c_string_encode(name),
            c_string_encode(uri),
            nisyscfg.enums.Bool(enabled),
            nisyscfg.enums.Bool(trusted),
        )
        nisyscfg.errors.handle_error(self, error_code)

    def modify_software_feed(
        self, old_name: str, new_name: str, uri: str, enabled: bool, trusted: bool
    ) -> None:
        """Modifies an existing software feed by name.

        Note: This requires Secure Shell Server (sshd) to be enabled on the
        target.

        Args:
            old_name (str): Name of the feed to modify. This feed must exist on the system.

            new_name (str): New name of the feed. This feed must not exist on the
                system. If not specified, the feed name will remain unchanged.

            uri (str): New location of the feed, such as "file://..." or "http://...".
                NI feeds often start with "http://download.ni.com/".

            enabled (bool): New enabled state.

            trusted (bool): New trusted state. A trusted feed will not be
                cryptographically verified by the package manager to be a safe and
                secure source of packages. Feeds are not trusted by default. A system
                administrator may have reason to trust the feed regardless.

        Raises:
            nisyscfg.errors.LibraryError: In the event of an error.
        """
        error_code = self._library.ModifySoftwareFeed(
            self._session,
            c_string_encode(old_name),
            c_string_encode(new_name),
            c_string_encode(uri),
            nisyscfg.enums.Bool(enabled),
            nisyscfg.enums.Bool(trusted),
        )
        nisyscfg.errors.handle_error(self, error_code)

    def remove_software_feed(self, name: str) -> None:
        """Removes an existing software feed by name.

        Note: This requires Secure Shell Server (sshd) to be enabled on the
        target.

        Args:
            name (str): Name of the feed to remove. This feed must exist on the system.

        Raises:
            nisyscfg.errors.LibraryError: In the event of an error.
        """
        error_code = self._library.RemoveSoftwareFeed(self._session, c_string_encode(name))
        nisyscfg.errors.handle_error(self, error_code)

    def install_all(
        self, auto_restart: bool = True, deselect_conflicts: bool = True
    ) -> InstallAllResult:
        """Installs software on a Real-Time system.

        Args:
            auto_restart (bool, optional): Restarts the system into install mode by default before
                the operation is performed, and restarts back to a running state after
                the operation is complete. If you choose not to restart automatically,
                the operation will fail if the system is not already in install mode.

            deselect_conflicts (bool, optional): Indicates whether to deselect conflicting software
                components automatically. Select True to deselect the conflicting
                software components. If False, installation will fail if the system
                has conflicting software components.

        Returns:
            InstallAllResult: A named tuple containing the following fields:

            - installed_components: An iterator to get information about each
              component that was just installed.
            - broken_dependencies: An iterator to get a list of broken
              dependencies, which are specific software components that cannot
              operate without another software component installed.

        Raises:
            nisyscfg.errors.LibraryError: In the event of an error.
        """
        installed_component_handle = nisyscfg.types.EnumSoftwareFeedHandle()
        broken_dependency_handle = nisyscfg.types.EnumDependencyHandle()
        error_code = self._library.InstallAll(
            self._session,
            auto_restart,
            deselect_conflicts,
            ctypes.pointer(installed_component_handle),
            ctypes.pointer(broken_dependency_handle),
        )
        nisyscfg.errors.handle_error(self, error_code)

        result = InstallAllResult(
            installed_components=nisyscfg.component_info.ComponentInfoIterator(
                installed_component_handle
            ),
            broken_dependencies=nisyscfg.dependency_info.DependencyInfoIterator(
                broken_dependency_handle
            ),
        )

        self._children.append(result.installed_components)
        self._children.append(result.broken_dependencies)

        return result

    def uninstall_all(self, auto_restart: bool = True) -> None:
        """Uninstalls all software from a specified system.

        ARgs:
            auto_restart (bool, optional): Restarts the system before and/or after the operation as
                required by the target's boot flow. The operation will fail if you
                choose not to restart the target automatically and the target's boot
                flow requires it to be in safe mode or restart after the operation.

        Raises:
            nisyscfg.errors.LibraryError: In the event of an error.
        """
        error_code = self._library.UninstallAll(self._session, auto_restart)
        nisyscfg.errors.handle_error(self, error_code)

    def _install_uninstall(
        self,
        components_to_install: Optional[List[str]] = None,
        components_to_uninstall: Optional[List[str]] = None,
        auto_restart: bool = True,
        auto_select_dependencies: bool = True,
        auto_select_recommends: bool = True,
        item_types: nisyscfg.enums.IncludeComponentTypes = nisyscfg.enums.IncludeComponentTypes.ALL_VISIBLE,
    ) -> nisyscfg.dependency_info.DependencyInfoIterator:
        """Modifies the software components installed on a system.

        Allows you to install components, uninstall components, or both install
        and uninstall components simultaneously (as long as two components do
        not overlap each other).

        Args:
            components_to_install (List[str], optional): List of software components IDs or titles
                to install.

            components_to_uninstall (List[str], optional): List of software components IDs to
                remove.

            auto_restart (bool, optional): Restarts the system into install mode by default before
                the operation is performed, and restarts back to a running state after
                the operation is complete. If you choose not to restart automatically,
                the operation will fail if the system is not already in install mode.

            auto_select_dependencies (bool, optional): Specifies whether to automatically select
                software components that are required by the software you have
                specified to install.

            auto_select_recommends (bool, optional): Specifies whether to automatically select
                recommended packages.

            item_types (nisyscfg.enums.IncludeComponentTypes, optional): Allows inclusion of hidden
                software installed on the target when
                :attr:`nisyscfg.enums.IncludeComponentTypes.ALL_VISIBLE_AND_HIDDEN` is selected.
                Hidden software is not listed by default.

        Returns:
            nisyscfg.dependency_info.DependencyInfoIterator: An iterator to get a list of broken
            dependencies, which are specific software components that cannot operate without another
            software component installed.

        Raises:
            nisyscfg.errors.LibraryError: In the event of an error.
        """
        software_to_install = nisyscfg.component_info.EnumSoftwareComponent()

        if components_to_install:
            for component_name in components_to_install:
                component = self._get_latest_component(component_name, item_types)
                software_to_install.add_component(
                    component.id,
                    component.version,
                    nisyscfg.enums.VersionSelectionMode.EXACT,
                )

        if components_to_uninstall:
            c_components_to_uninstall = (ctypes.c_char_p * len(components_to_uninstall))(
                *map(c_string_encode, components_to_uninstall)
            )
        else:
            c_components_to_uninstall = (ctypes.c_char_p * 0)()

        broken_dependency_handle = nisyscfg.types.EnumDependencyHandle()

        error_code = self._library.InstallUninstallComponents2(
            self._session,
            auto_restart,
            auto_select_dependencies,
            auto_select_recommends,
            software_to_install._handle,
            len(c_components_to_uninstall),
            ctypes.cast(c_components_to_uninstall, ctypes.POINTER(ctypes.POINTER(ctypes.c_char))),
            ctypes.pointer(broken_dependency_handle),
        )
        nisyscfg.errors.handle_error(self, error_code)

        broken_dependencies = nisyscfg.dependency_info.DependencyInfoIterator(
            broken_dependency_handle
        )
        self._children.append(broken_dependencies)

        return broken_dependencies

    def install(
        self,
        components: Optional[List[str]] = None,
        auto_restart: bool = True,
        auto_select_dependencies: bool = True,
        auto_select_recommends: bool = True,
        item_types: nisyscfg.enums.IncludeComponentTypes = nisyscfg.enums.IncludeComponentTypes.ALL_VISIBLE,
    ) -> nisyscfg.dependency_info.DependencyInfoIterator:
        """Installs software components to the system.

        Args:
            components (List[str], optional): List of software components IDs or titles to install.

            auto_restart (bool, optional): Restarts the system into install mode by default before
                the operation is performed, and restarts back to a running state after
                the operation is complete. If you choose not to restart automatically,
                the operation will fail if the system is not already in install mode.

            auto_select_dependencies (bool, optional): Specifies whether to automatically select
                software components that are required by the software you have
                specified to install.

            auto_select_recommends (bool, optional): Specifies whether to automatically select
                recommended packages.

            item_types (nisyscfg.enums.IncludeComponentTypes, optional): Allows inclusion of hidden
                software installed on the target when
                :attr:`nisyscfg.enums.IncludeComponentTypes.ALL_VISIBLE_AND_HIDDEN` is selected.
                Hidden software is not listed by default.

        Returns:
            nisyscfg.dependency_info.DependencyInfoIterator: An iterator to get a list of broken
            dependencies, which are specific software components that cannot operate without another
            software component installed.

        Raises:
            nisyscfg.errors.LibraryError: In the event of an error.
        """
        return self._install_uninstall(
            components_to_install=components,
            auto_restart=auto_restart,
            auto_select_dependencies=auto_select_dependencies,
            auto_select_recommends=auto_select_recommends,
            item_types=item_types,
        )

    def uninstall(
        self,
        components: Optional[List[str]] = None,
        auto_restart: bool = True,
        auto_select_dependencies: bool = True,
        auto_select_recommends: bool = True,
        item_types: nisyscfg.enums.IncludeComponentTypes = nisyscfg.enums.IncludeComponentTypes.ALL_VISIBLE,
    ) -> nisyscfg.dependency_info.DependencyInfoIterator:
        """Uninstall software components from the system.

        Args:
            components (List[str], optional): List of software components IDs to remove.

            auto_restart (bool, optional): Restarts the system into install mode by default before
                the operation is performed, and restarts back to a running state after
                the operation is complete. If you choose not to restart automatically,
                the operation will fail if the system is not already in install mode.

            auto_select_dependencies (bool, optional): Specifies whether to automatically select
                software components that are required by the software you have
                specified to install.

            auto_select_recommends (bool, optional): Specifies whether to automatically select
                recommended packages.

            item_types (nisyscfg.enums.IncludeComponentTypes, optional): Allows inclusion of hidden
                software installed on the target when
                :attr:`nisyscfg.enums.IncludeComponentTypes.ALL_VISIBLE_AND_HIDDEN` is selected.
                Hidden software is not listed by default.

        Returns:
            nisyscfg.dependency_info.DependencyInfoIterator: An iterator to get a list of broken
            dependencies, which are specific software components that cannot operate without another
            software component installed.

        Raises:
            nisyscfg.errors.LibraryError: In the event of an error.
        """
        return self._install_uninstall(
            components_to_uninstall=components,
            auto_restart=auto_restart,
            auto_select_dependencies=auto_select_dependencies,
            auto_select_recommends=auto_select_recommends,
            item_types=item_types,
        )

    def _get_latest_component(
        self,
        component_name: str,
        item_types: nisyscfg.enums.IncludeComponentTypes = nisyscfg.enums.IncludeComponentTypes.ALL_VISIBLE,
    ) -> nisyscfg.component_info.ComponentInfo:
        """Retrieves the latest version of a software component."""
        components = [
            component
            for component in self.get_available_software_components(item_types)
            if (component.title == component_name) or (component.id == component_name)
        ]

        if not components:
            raise nisyscfg.errors.Error(
                'Component "{component_name}" not available for install on target "{self.target_name}".'.format(
                    component_name=component_name, self=self
                )
            )

        return max(components, key=lambda comp: comp.version.split("."))

    def get_software_feeds(self) -> nisyscfg.software_feed.SoftwareFeedIterator:
        """Retrieves configured software feeds.

        A feed represents a location that the package manager uses to find and download available
        software.

        Note: This requires Secure Shell Server (sshd) to be enabled on the
        target.

        Returns:
            nisyscfg.software_feed.SoftwareFeedIterator: An iterator to get a list of software feeds
            configured on the system.

        Raises:
            nisyscfg.errors.LibraryError: In the event of an error.
        """
        software_feed_handle = nisyscfg.types.EnumSoftwareFeedHandle()
        error_code = self._library.GetSoftwareFeeds(
            self._session, ctypes.pointer(software_feed_handle)
        )
        nisyscfg.errors.handle_error(self, error_code)
        if software_feed_handle:
            iter = nisyscfg.software_feed.SoftwareFeedIterator(software_feed_handle)
            self._children.append(iter)
            return iter
        return nisyscfg.software_feed.SoftwareFeedIterator()

    @property
    def resource(self) -> nisyscfg.hardware_resource.HardwareResource:
        """System resource properties."""
        if not hasattr(self, "_resource"):
            resource_handle = self._get_property(16941086, nisyscfg.types.ResourceHandle)
            self._resource = nisyscfg.hardware_resource.HardwareResource(resource_handle)
            self._children.append(self._resource)
        return self._resource

    def _get_property(self, id: int, c_type: Any) -> Any:
        """Retrieves a system property."""
        value: Any
        value_arg: Any

        if c_type == ctypes.c_char_p:
            value = nisyscfg.types.simple_string()
            value_arg = value
        elif issubclass(c_type, nisyscfg.enums._BaseEnum) or issubclass(
            c_type, nisyscfg.enums._BaseFlag
        ):
            value = ctypes.c_int()
            value_arg = ctypes.pointer(value)
        else:
            value = c_type(0)
            value_arg = ctypes.pointer(value)

        error_code = self._library.GetSystemProperty(self._session, id, value_arg)
        nisyscfg.errors.handle_error(self, error_code)

        if issubclass(c_type, nisyscfg.enums._BaseEnum) or issubclass(
            c_type, nisyscfg.enums._BaseFlag
        ):
            return c_type(value.value)

        if issubclass(c_type, ctypes.c_void_p):
            return value

        return c_string_decode(value.value)

    def _set_property(self, id: int, value: Any, c_type: Any, nisyscfg_type: Any) -> None:
        if c_type == ctypes.c_char_p:
            value = c_string_encode(value)
        elif issubclass(c_type, nisyscfg.enums._BaseEnum) or issubclass(
            c_type, nisyscfg.enums._BaseFlag
        ):
            value = ctypes.c_int(value)
        else:
            value = c_type(value)

        error_code = self._library.SetSystemProperty(self._session, id, value)
        nisyscfg.errors.handle_error(self, error_code)

    def save_changes(self) -> SaveChangesResult:
        """Saves changes made to systems.

        Returns:
            nisyscfg.system.SaveChangesResult: A tuple containing the following fields:

            - restart_required - Specifies whether the changes require a reboot.
              If TRUE, call restart().

            - details - A string containing results of any errors that may have
              occurred during execution.

        Raises:
            nisyscfg.errors.LibraryError: In the event of an error.
        """
        restart_required = ctypes.c_int()
        c_details = ctypes.POINTER(ctypes.c_char)()
        error_code = self._library.SaveSystemChanges(
            self._session, restart_required, ctypes.pointer(c_details)
        )
        if c_details:
            details = c_string_decode(ctypes.cast(c_details, ctypes.c_char_p).value)
            error_code_2 = self._library.FreeDetailedString(c_details)
        nisyscfg.errors.handle_error(self, error_code)
        nisyscfg.errors.handle_error(self, error_code_2)
        return SaveChangesResult(restart_required=restart_required.value != 0, details=details)

    @property
    def property_accessor(self) -> nisyscfg.properties.PropertyAccessor:
        """The property accessor."""
        return self._property_accessor

    def set_system_image(
        self,
        source: Union[str, pathlib.Path],
        auto_restart: bool = True,
        encryption_passphrase: Optional[str] = None,
        exclude_paths: Optional[List[str]] = None,
        original_system_only: bool = False,
        network_settings: nisyscfg.enums.NetworkInterfaceSettings = nisyscfg.enums.NetworkInterfaceSettings.PRESERVE_PRIMARY_PRESERVE_OTHERS,
    ) -> None:
        """Applies an image to a system.

        The system image is a copy of the contents and software on the primary
        hard drive of a specified target system. Applying the image to the
        system restores it to the state captured when the image was created.
        This image can exist as a folder or a zipped archive.

        Args:
            source (Union[str, pathlib.Path]): The path to the system image file or folder.

            auto_restart (bool, optional): Restarts the system into install mode by default before
                the operation is performed, and restarts back to a running state after
                the operation is complete. If you choose not to restart automatically,
                and the system is not in install mode, the resulting image may not be
                valid.

            encryption_passphrase (str, optional): A passphrase used to encrypt a portion of the
                image that contains sensitive information.

            exclude_paths (List[str], optional): Specifies the list of files and folders to exclude
                from the target image. Files on the blacklist will not be copied from the
                image to the target and they will not be removed from the target.

            original_system_only (bool, optional): Verifies that the target system has the same MAC
                address as the system from which the image was originally created.
                Selecting True will allow you to restore an image from the exact same
                target from which the image was created only. This option is False by
                default. When the option is False, this operation can also apply the
                system image to other targets of the same device class.

            network_settings (nisyscfg.enums.NetworkInterfaceSettings, optional): Resets the primary
                network adapter and disables secondary adapters by default.

        Raises:
            FileNotFoundError: If the source file or folder does not exist.
            nisyscfg.errors.InvalidSystemImageError: If the source is not a valid zip file.
            nisyscfg.errors.LibraryError: In the event of an error.
        """
        source = pathlib.Path(source)
        if not source.exists():
            raise FileNotFoundError(f"The source {source} does not exist.")
        if exclude_paths is not None:
            raise NotImplementedError("Excluding paths is not implemented yet.")

        with ExitStack() as stack:
            if source.is_dir():
                source_folder = str(source)
            else:
                source_folder = str(stack.enter_context(tempfile.TemporaryDirectory()))
                try:
                    zip_ref = stack.enter_context(zipfile.ZipFile(source, "r"))
                except zipfile.BadZipFile:
                    raise nisyscfg.errors.InvalidSystemImageError(
                        f"{source} is not a valid zip file."
                    )
                zip_ref.extractall(source_folder)

            error_code = self._library.SetSystemImageFromFolder2(
                self._session,
                nisyscfg.enums.Bool(auto_restart),
                c_string_encode(source_folder),
                c_string_encode(encryption_passphrase),
                0,  # len(exclude_paths)
                exclude_paths,
                nisyscfg.enums.Bool(original_system_only),
                network_settings,
            )
            nisyscfg.errors.handle_error(self, error_code)

    device_class: str
    """Device class of the system."""
    product_id: int
    """Product ID of the system."""
    file_system: Union[nisyscfg.enums.FileSystemMode, int]
    """File system mode of the system."""
    firmware_revision: str
    """Firmware revision of the system."""
    is_factory_reset_supported: Union[nisyscfg.enums.Bool, int]
    """Whether factory reset is supported."""
    is_firmware_update_supported: Union[nisyscfg.enums.Bool, int]
    """Whether firmware update is supported."""
    is_locked: Union[nisyscfg.enums.Bool, int]
    """Whether the system is locked."""
    is_locking_supported: Union[nisyscfg.enums.Bool, int]
    """Whether locking is supported."""
    is_on_local_subnet: Union[nisyscfg.enums.Bool, int]
    """Whether the system is on the local subnet."""
    is_restart_supported: Union[nisyscfg.enums.Bool, int]
    """Whether restart is supported."""
    mac_address: str
    """MAC address of the system."""
    product_name: str
    """Product name of the system."""
    operating_system: str
    """Operating system of the system."""
    operating_system_version: str
    """Operating system version."""
    operating_system_description: str
    """Description of the operating system."""
    serial_number: str
    """Serial number of the system."""
    system_state: str
    """State of the system."""
    memory_phys_total: float
    """Total physical memory (bytes)."""
    memory_phys_free: float
    """Free physical memory (bytes)."""
    memory_largest_block: float
    """Largest block of free memory (bytes)."""
    memory_virt_total: float
    """Total virtual memory (bytes)."""
    memory_virt_free: float
    """Free virtual memory (bytes)."""
    primary_disk_total: float
    """Total primary disk space (bytes)."""
    primary_disk_free: float
    """Free primary disk space (bytes)."""
    image_description: str
    """Description of the system image."""
    image_id: str
    """ID of the system image."""
    image_title: str
    """Title of the system image."""
    image_version: str
    """Version of the system image."""
    installed_api_version: str
    """Installed API version."""
    is_dst: Union[nisyscfg.enums.Bool, int]
    """Whether daylight saving time is in effect."""
    is_restart_protected: Union[nisyscfg.enums.Bool, int]
    """Whether restart protection is enabled."""
    halt_on_error: Union[nisyscfg.enums.Bool, int]
    """Whether to halt on error."""
    repository_location: str
    """Repository location for software components."""
    system_comment: str
    """System comment."""
    auto_restart_timeout: int
    """Auto-restart timeout (ms)."""
    dns_server: str
    """DNS server address."""
    gateway: str
    """Gateway address."""
    hostname: str
    """Hostname of the system."""
    ip_address: str
    """IP address of the system."""
    ip_address_mode: Union[nisyscfg.enums.IpAddressMode, int]
    """IP address mode."""
    subnet_mask: str
    """Subnet mask of the system."""
