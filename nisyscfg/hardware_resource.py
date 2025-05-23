"""Hardware resource classes."""

import collections.abc
import ctypes
from functools import reduce
from typing import Any, List, Mapping, NamedTuple, Optional

import nisyscfg
import nisyscfg.enums
import nisyscfg.errors
import nisyscfg.properties
import nisyscfg.pxi.hardware_resource
import nisyscfg.pxi.properties
import nisyscfg.timestamp
import nisyscfg.types
import nisyscfg.xnet.hardware_resource
import nisyscfg.xnet.properties
from nisyscfg._lib import c_string_decode, c_string_encode


class _NoDefault(object):
    pass


class SaveChangesResult(NamedTuple):
    """Result of saving changes to a hardware resource."""

    restart_required: bool
    """Specifies whether the changes require a reboot."""
    details: str
    """A string containing results of any errors that may have occurred during execution."""


class UpgradeFirmwareResult(NamedTuple):
    """Result of upgrading firmware on a hardware resource."""

    status: "nisyscfg.enums.FirmwareStatus"
    """The status of the firmware update."""
    details: str
    """Results of any errors that may have occurred when this function completed."""


class FirmwareStatusResult(NamedTuple):
    """Status of a firmware upgrade in progress."""

    percent_complete: int
    """The status, in percent, of the current step in the firmware upgrade."""
    status: "nisyscfg.enums.FirmwareStatus"
    """The status of the firmware update."""
    details: str
    """Results of any errors that may have occurred when this function completed."""


class DeleteResult(NamedTuple):
    """Result of deleting a hardware resource."""

    dependent_items_deleted: bool
    """Returns whether resources other than the specified one were deleted."""
    details: str
    """A string containing results of any errors that may have occurred during execution."""


@nisyscfg.properties.PropertyBag(nisyscfg.properties.Resource, nisyscfg.properties.IndexedResource)
@nisyscfg.properties.PropertyBag(
    nisyscfg.pxi.properties.Resource,
    nisyscfg.pxi.properties.IndexedResource,
    expert="pxi",
)
@nisyscfg.properties.PropertyBag(nisyscfg.xnet.properties.Resource, expert="xnet")
class HardwareResource(object):
    """Represents a hardware resource in NI System Configuration."""

    def __init__(self, handle: nisyscfg.types.Handle) -> None:
        """Initializes a HardwareResource.

        Args:
            handle: The handle to the hardware resource.
        """
        self._handle: Optional[nisyscfg.types.Handle] = handle
        self._library = nisyscfg._library_singleton.get()
        self._property_accessor = nisyscfg.properties.PropertyAccessor(
            setter=self._set_property,
            getter=self._get_property,
            indexed_getter=self._get_indexed_property,
        )

    def __del__(self) -> None:
        """Destructor to ensure resources are released."""
        self.close()

    def __repr__(self) -> str:
        """Returns a string representation of the hardware resource."""
        return "HardwareResource(name={})".format(self.name)

    @property
    def name(self) -> str:
        """Returns a name that identifies a resource.

        Returns:
            str: The name or alias of the resource.
        """
        name = self.expert_user_alias[0]
        # If the resource doesn't have an alias, use the resource name instead
        if not name:
            name = self.expert_resource_name[0]
        return name

    def close(self) -> None:
        """Closes reference to previously allocated resource.

        Raises:
            nisyscfg.errors.LibraryError: If an error occurs during close.
        """
        if self._handle:
            error_code = self._library.CloseHandle(self._handle)
            nisyscfg.errors.handle_error(None, error_code)
            self._handle = None

    def _get_property(self, id: int, c_type: Any) -> Any:
        value: Any = nisyscfg.types.simple_string()
        value_arg: Any = value
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

        error_code = self._library.GetResourceProperty(self._handle, id, value_arg)
        nisyscfg.errors.handle_error(None, error_code)

        if issubclass(c_type, nisyscfg.enums._BaseEnum) or issubclass(
            c_type, nisyscfg.enums._BaseFlag
        ):
            return c_type(value.value)

        if c_type == nisyscfg.types.TimestampUTC:
            return nisyscfg.timestamp._convert_ctype_to_datetime(value)

        return c_string_decode(value.value)

    def _get_indexed_property(self, id: int, index: int, c_type: Any) -> Any:
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
            value = c_type()
            value_arg = ctypes.pointer(value)

        error_code = self._library.GetResourceIndexedProperty(self._handle, id, index, value_arg)
        nisyscfg.errors.handle_error(None, error_code)

        if issubclass(c_type, nisyscfg.enums._BaseEnum) or issubclass(
            c_type, nisyscfg.enums._BaseFlag
        ):
            return c_type(value.value)

        if c_type == nisyscfg.types.TimestampUTC:
            return nisyscfg.timestamp._convert_ctype_to_datetime(value)

        return c_string_decode(value.value)

    def get_property(self, name: str, default: Any = _NoDefault()) -> Any:
        """Returns value of hardware resource property.

        Return the value for hardware resource property specified by the name,
        else default. If default is not given and the property does not exist,
        this function raises an nisyscfg.errors.LibraryError exception.
        """
        try:
            return reduce(getattr, name.split("."), self)
        except nisyscfg.errors.LibraryError as err:
            if err.code != nisyscfg.errors.Status.PROP_DOES_NOT_EXIST or isinstance(
                default, _NoDefault
            ):
                raise
            return default

    def _set_property(self, id: int, value: Any, c_type: Any, nisyscfg_type: Any) -> None:
        if c_type == ctypes.c_char_p:
            value = c_string_encode(value)
        elif issubclass(c_type, nisyscfg.enums._BaseEnum) or issubclass(
            c_type, nisyscfg.enums._BaseFlag
        ):
            value = ctypes.c_int(value)
        elif c_type == nisyscfg.types.TimestampUTC:
            value = nisyscfg.timestamp._convert_datetime_to_ctype(value)
        else:
            value = c_type(value)

        error_code = self._library.SetResourceProperty(self._handle, id, value)
        nisyscfg.errors.handle_error(None, error_code)

    def rename(
        self, new_name: str, overwrite_conflict: bool = False, update_dependencies: bool = False
    ) -> Optional["HardwareResource"]:
        """Changes the display name of a resource.

        Args:
            new_name (str): The user-specified new name for the resource.
            overwrite_conflict (bool): Allows resource name changes to occur if there are
                any naming conflicts. If this value is True, the resource name change
                occurs even if another resource with the same name already exists. If
                this value is False (default), this function raises if another resource
                with the same name already exists. If this value is True and you choose
                a name that is already assigned to an existing resource, this function
                also changes the name of the existing resource.
            update_dependencies (bool): Updates dependencies (for example: a task or
                channel) if the resource being renamed has them. Dependencies will be
                updated to refer to the new name by default. Select FALSE if you do not
                want to update these dependencies.
                Note: If overwrite_conflict is True and an existing resource was also
                renamed due to a conflict, the dependencies for that resource will not
                be updated. This option only affects the dependencies for the resource
                you are currently renaming.

        Returns:
            Optional[HardwareResource]: Resource whose name was overwritten. This will be None
            if no other resource was overwritten.

        Raises:
            nisyscfg.errors.LibraryError: In the event of an error.
        """
        name_already_existed = ctypes.c_int()
        overwritten_resource_handle = nisyscfg.types.ResourceHandle()
        error_code = self._library.RenameResource(
            self._handle,
            c_string_encode(new_name),
            overwrite_conflict,
            update_dependencies,
            ctypes.pointer(name_already_existed),
            ctypes.pointer(overwritten_resource_handle),
        )
        nisyscfg.errors.handle_error(None, error_code)

        # TODO(tkrebes): Ensure lifetime of HardwareResource does not exceed the
        # session.
        overwritten_resource = (
            HardwareResource(overwritten_resource_handle)
            if overwritten_resource_handle.value
            else None
        )

        # Do not return the bool 'name_already_existed' since it is equivalent
        # to 'overwritten_syscfg_resource == None'.
        return overwritten_resource

    def reset(self, mode: int = 0) -> None:
        """Executes a reset on a specified resource.

        Args:
            mode (int): Reserved. This must be 0.

        Raises:
            nisyscfg.errors.LibraryError: In the event of an error.
        """  # noqa: D212, W505 - Multi-line docstring summary should start at the first line (auto-generated noqa), doc line too long (109 > 100 characters) (auto-generated noqa)
        error_code = self._library.ResetHardware(self._handle, mode)
        nisyscfg.errors.handle_error(None, error_code)

    def save_changes(self) -> SaveChangesResult:
        """Writes and saves property changes on a device.

        Returns:
            nisyscfg.hardware_resource.SaveChangesResult: A named tuple containing the
            restart_required flag and details string.

        Raises:
            nisyscfg.errors.LibraryError: In the event of an error.
        """
        restart_required = ctypes.c_int()
        c_details = ctypes.POINTER(ctypes.c_char)()
        error_code = self._library.SaveResourceChanges(
            self._handle, restart_required, ctypes.pointer(c_details)
        )
        if c_details:
            details = c_string_decode(ctypes.cast(c_details, ctypes.c_char_p).value)
            error_code_2 = self._library.FreeDetailedString(c_details)
        nisyscfg.errors.handle_error(None, error_code)
        nisyscfg.errors.handle_error(None, error_code_2)

        return SaveChangesResult(restart_required=restart_required.value != 0, details=details)

    def self_calibrate(self) -> str:
        """Performs a self-calibration on a device.

        Self-calibration adjusts the calibration constants with respect to an
        onboard reference stored on the device. The new calibration constants
        are defined with respect to the calibration constants created during an
        external calibration to ensure that the measurements are traceable to
        these external standards. The new calibration constants do not affect
        the constants created during an external calibration because they are
        stored in a different area of the device memory. You can perform a self-
        calibration at any time to adjust the device for use in environments
        other than those in which the device was externally calibrated.

        Returns:
             A string containing results of any errors that may have occurred during execution.

        Raises:
            nisyscfg.errors.LibraryError: In the event of an error.
        """
        c_details = ctypes.POINTER(ctypes.c_char)()
        error_code = self._library.SelfCalibrateHardware(self._handle, ctypes.pointer(c_details))
        if c_details:
            details = c_string_decode(ctypes.cast(c_details, ctypes.c_char_p).value)
            error_code_2 = self._library.FreeDetailedString(c_details)
        nisyscfg.errors.handle_error(None, error_code)
        nisyscfg.errors.handle_error(None, error_code_2)

        return details

    def self_test(self, mode: int = 0) -> str:
        """Verifies that system devices are able to perform basic I/O functions.

        No other tasks should run on the system while executing the self test
        because the driver may need exclusive access to some device resources.
        You do not need to disconnect devices from external equipment because
        the state of I/O lines are maintained throughout the test.

        Args:
            mode (int): Reserved. This must be 0.

        Returns:
            A string containing results of any errors that may have occurred during execution.

        Raises:
            nisyscfg.errors.LibraryError: In the event of an error.
        """
        c_details = ctypes.POINTER(ctypes.c_char)()
        error_code = self._library.SelfTestHardware(self._handle, mode, ctypes.pointer(c_details))
        if c_details:
            details = c_string_decode(ctypes.cast(c_details, ctypes.c_char_p).value)
            error_code_2 = self._library.FreeDetailedString(c_details)
        nisyscfg.errors.handle_error(None, error_code)
        nisyscfg.errors.handle_error(None, error_code_2)

        return details

    def upgrade_firmware(
        self,
        version: Optional[str] = None,
        filepath: Optional[str] = None,
        auto_stop_task: bool = True,
        force: bool = False,
        sync_call: bool = True,
    ) -> UpgradeFirmwareResult:
        """Updates the firmware on the target.

        Args:
            version (str): Specifies the firmware version you want to apply to the
                target. Use '0' to install the latest available firmware.

            filepath (str): Specifies the firmware file you want to upload to the target.
                Note: Parameters version and filepath are mutually exclusive and you
                must specify one and only one.

            auto_stop_task (bool,optional): Specifies to automatically end all tasks running on the
                target, even if they are incomplete and switch to firmware update mode.
                The default is True.

            force (bool,optional): Specifies to overwrite the destination firmware image even if
                the version is the same as or older than the version of the destination
                firmware image. If False, the function checks the version of the
                firmware returned by the expert and, if the returned version is newer
                than the version you are upgrading, this function returns an error. If
                the firmware version is the same and this parameter is set to False, the
                function does not upgrade the firmware and returns success. If True,
                this function automatically upgrades the firmware, regardless of the
                version of the destination firmware image. The default is False.

            sync_call (bool,optional): Specifies whether to wait for the upgrade operation to
                finish before returning. If False, the upgrade operation may continue
                running even after this function returns. To check the status, query
                the firmware_status property. The default is True.

        Returns:
            UpgradeFirmwareResult: A named tuple containing the status and details of the
            firmware update.

        Raises:
            nisyscfg.errors.LibraryError: In the event of an error.
        """
        if version and filepath:
            raise ValueError("version and filepath are mutually exclusive parameters")

        firmware_status = ctypes.c_int()
        c_details = ctypes.POINTER(ctypes.c_char)()
        if version:
            error_code = self._library.UpgradeFirmwareVersion(
                self._handle,
                c_string_encode(version),
                auto_stop_task,
                force,
                sync_call,
                ctypes.pointer(firmware_status),
                ctypes.pointer(c_details),
            )
        elif filepath:
            error_code = self._library.UpgradeFirmwareFromFile(
                self._handle,
                c_string_encode(filepath),
                auto_stop_task,
                force,
                sync_call,
                ctypes.pointer(firmware_status),
                ctypes.pointer(c_details),
            )
        else:
            raise ValueError(
                "upgrade_firmware() requires either version or filepath to be specified"
            )

        if c_details:
            details = c_string_decode(ctypes.cast(c_details, ctypes.c_char_p).value)
            error_code_2 = self._library.FreeDetailedString(c_details)
        nisyscfg.errors.handle_error(None, error_code)
        nisyscfg.errors.handle_error(None, error_code_2)

        return UpgradeFirmwareResult(
            status=nisyscfg.enums.FirmwareStatus(firmware_status.value), details=details
        )

    @property
    def firmware_status(self) -> FirmwareStatusResult:
        """Returns the status of the firmware upgrade in progress.

        Returns:
            FirmwareStatusResult: A named tuple containing percent complete,
            status, and details.

        Raises:
            nisyscfg.errors.LibraryError: In the event of an error.
        """
        percent_complete = ctypes.c_int()
        firmware_status = ctypes.c_int()
        c_details = ctypes.POINTER(ctypes.c_char)()
        error_code = self._library.CheckFirmwareStatus(
            self._handle, percent_complete, firmware_status, ctypes.pointer(c_details)
        )
        if c_details:
            details = c_string_decode(ctypes.cast(c_details, ctypes.c_char_p).value)
            error_code_2 = self._library.FreeDetailedString(c_details)
        nisyscfg.errors.handle_error(None, error_code)
        nisyscfg.errors.handle_error(None, error_code_2)

        return FirmwareStatusResult(
            percent_complete=percent_complete.value,
            status=nisyscfg.enums.FirmwareStatus(firmware_status.value),
            details=details,
        )

    def delete(
        self,
        mode: nisyscfg.enums.DeleteValidationMode = nisyscfg.enums.DeleteValidationMode.DELETE_IF_NO_DEPENDENCIES_EXIST,
    ) -> DeleteResult:
        """Permanently removes a hardware resource and its configuration data from the system.

        Note: Not all devices can be deleted; consult your product documentation.

        Args:
            mode (nisyscfg.enums.DeleteValidationMode): Specifies the conditions under which to
                delete the specified resource.

        Returns:
            DeleteResult: A named tuple containing the dependent_items_deleted flag and details
            string.

        Raises:
            nisyscfg.errors.LibraryError: In the event of an error.
        """
        dependent_items_deleted = ctypes.c_int()
        c_details = ctypes.POINTER(ctypes.c_char)()
        error_code = self._library.DeleteResource(
            self._handle, mode, dependent_items_deleted, ctypes.pointer(c_details)
        )
        if c_details:
            details = c_string_decode(ctypes.cast(c_details, ctypes.c_char_p).value)
            error_code_2 = self._library.FreeDetailedString(c_details)
        nisyscfg.errors.handle_error(None, error_code)
        nisyscfg.errors.handle_error(None, error_code_2)

        return DeleteResult(
            dependent_items_deleted=dependent_items_deleted.value != 0, details=details
        )

    @property
    def property_accessor(self) -> nisyscfg.properties.PropertyAccessor:
        """The property accessor."""
        return self._property_accessor

    is_device: bool
    """Specifies whether the resource is a device."""
    is_chassis: bool
    """Specifies whether the resource is a chassis."""
    connects_to_bus_type: nisyscfg.enums.BusType
    """The bus type to which the resource connects."""
    vendor_id: int
    """The vendor ID for the resource."""
    vendor_name: str
    """The vendor name for the resource."""
    product_id: int
    """The product ID for the resource."""
    product_name: str
    """The product name for the resource."""
    serial_number: str
    """The serial number for the resource."""
    firmware_revision: str
    """The firmware revision for the resource."""
    is_ni_product: bool
    """Specifies whether the resource is an NI product."""
    is_simulated: bool
    """Specifies whether the resource is simulated."""
    connects_to_link_name: str
    """The link name to which the resource connects."""
    has_driver: nisyscfg.enums.HasDriverType
    """Indicates whether the resource has a driver."""
    is_present: nisyscfg.enums.IsPresentType
    """Indicates whether the resource is present."""
    slot_number: int
    """The slot number for the resource."""
    supports_internal_calibration: bool
    """Specifies whether the device supports internal calibration."""
    internal_calibration_last_time: float
    """The last time internal calibration was performed."""
    internal_calibration_last_temp: float
    """The temperature at the last internal calibration."""
    supports_external_calibration: bool
    """Specifies whether the device supports external calibration."""
    external_calibration_last_temp: float
    """The temperature at the last external calibration."""
    calibration_comments: str
    """Comments related to calibration."""
    internal_calibration_last_limited: bool
    """Indicates if the last internal calibration was limited."""
    external_calibration_checksum: str
    """Checksum of the last external calibration."""
    current_temp: float
    """The current temperature of the resource."""
    pxi_pci_bus_number: int
    """PXI/PCI bus number."""
    pxi_pci_device_number: int
    """PXI/PCI device number."""
    pxi_pci_function_number: int
    """PXI/PCI function number."""
    pxi_pci_link_width: int
    """PXI/PCI link width."""
    pxi_pci_max_link_width: int
    """PXI/PCI maximum link width."""
    usb_interface: int
    """USB interface number."""
    tcp_host_name: str
    """TCP host name."""
    tcp_mac_address: str
    """TCP MAC address."""
    tcp_ip_address: str
    """TCP IP address."""
    tcp_device_class: str
    """TCP device class."""
    gpib_primary_address: int
    """GPIB primary address."""
    gpib_secondary_address: int
    """GPIB secondary address."""
    serial_port_binding: str
    """Serial port binding."""
    provides_bus_type: nisyscfg.enums.BusType
    """The bus type provided by the resource."""
    provides_link_name: str
    """The link name provided by the resource."""
    number_of_slots: int
    """The number of slots for the resource."""
    supports_firmware_update: bool
    """Specifies whether the resource supports firmware update."""
    firmware_file_pattern: str
    """Firmware file pattern."""
    recommended_calibration_interval: int
    """Recommended calibration interval."""
    supports_calibration_write: bool
    """Specifies whether calibration write is supported."""
    hardware_revision: str
    """Hardware revision."""
    cpu_model_name: str
    """CPU model name."""
    cpu_stepping_revision: int
    """CPU stepping revision."""
    model_name_number: int
    """Model name number."""
    module_program_mode: nisyscfg.enums.ModuleProgramMode
    """Module program mode."""
    connects_to_num_slots: int
    """Number of slots the resource connects to."""
    slot_offset_left: int
    """Slot offset left."""
    internal_calibration_values_in_range: bool
    """Indicates if internal calibration values are in range."""
    firmware_update_mode: nisyscfg.enums.FirmwareUpdateMode
    """Firmware update mode."""
    external_calibration_last_time: float
    """The last time external calibration was performed."""
    recommended_next_calibration_time: float
    """Recommended next calibration time."""
    external_calibration_last_limited: bool
    """Indicates if the last external calibration was limited."""
    calibration_current_password: str
    """Current calibration password."""
    calibration_new_password: str
    """New calibration password."""
    system_configuration_web_access: nisyscfg.enums.AccessType
    """System configuration web access type."""
    adapter_type: nisyscfg.enums.AdapterType
    """Adapter type."""
    mac_address: str
    """MAC address."""
    adapter_mode: nisyscfg.enums.AdapterMode
    """Adapter mode."""
    tcp_ip_request_mode: nisyscfg.enums.IpAddressMode
    """TCP IP request mode."""
    tcp_ip_v4_address: str
    """TCP IPv4 address."""
    tcp_ip_v4_subnet: str
    """TCP IPv4 subnet."""
    tcp_ip_v4_gateway: str
    """TCP IPv4 gateway."""
    tcp_ip_v4_dns_server: str
    """TCP IPv4 DNS server."""
    tcp_preferred_link_speed: nisyscfg.enums.LinkSpeed
    """Preferred TCP link speed."""
    tcp_current_link_speed: nisyscfg.enums.LinkSpeed
    """Current TCP link speed."""
    tcp_packet_detection: nisyscfg.enums.PacketDetection
    """TCP packet detection."""
    tcp_polling_interval: int
    """TCP polling interval."""
    is_primary_adapter: bool
    """Indicates if this is the primary adapter."""
    ether_cat_master_id: int
    """EtherCAT master ID."""
    ether_cat_master_redundancy: bool
    """EtherCAT master redundancy."""
    wlan_bssid: str
    """WLAN BSSID."""
    wlan_current_link_quality: int
    """Current WLAN link quality."""
    wlan_current_ssid: str
    """Current WLAN SSID."""
    wlan_current_connection_type: nisyscfg.enums.ConnectionType
    """Current WLAN connection type."""
    wlan_current_security_type: nisyscfg.enums.SecurityType
    """Current WLAN security type."""
    wlan_current_eap_type: nisyscfg.enums.EapType
    """Current WLAN EAP type."""
    wlan_country_code: int
    """WLAN country code."""
    wlan_channel_number: int
    """WLAN channel number."""
    wlan_client_certificate: str
    """WLAN client certificate."""
    wlan_security_identity: str
    """WLAN security identity."""
    wlan_security_key: str
    """WLAN security key."""
    system_start_time: float
    """System start time."""
    current_time: float
    """Current system time."""
    time_zone: str
    """System time zone."""
    user_directed_safe_mode_switch: bool
    """User directed safe mode switch."""
    console_out_switch: bool
    """Console out switch."""
    ip_reset_switch: bool
    """IP reset switch."""
    number_of_discovered_access_points: int
    """Number of discovered access points."""
    number_of_experts: int
    """Number of experts."""
    number_of_services: int
    """Number of services."""
    number_of_available_firmware_versions: int
    """Number of available firmware versions."""
    number_of_cpus: int
    """Number of CPUs."""
    number_of_fans: int
    """Number of fans."""
    number_of_power_sensors: int
    """Number of power sensors."""
    number_of_temperature_sensors: int
    """Number of temperature sensors."""
    number_of_voltage_sensors: int
    """Number of voltage sensors."""
    number_of_user_led_indicators: int
    """Number of user LED indicators."""
    number_of_user_switches: int
    """Number of user switches."""

    service_type: Mapping[int, nisyscfg.enums.ServiceType]
    """Service type for each service."""
    available_firmware_version: Mapping[int, str]
    """Available firmware version for each component."""
    wlan_available_ssid: Mapping[int, str]
    """Available WLAN SSID for each access point."""
    wlan_available_bssid: Mapping[int, str]
    """Available WLAN BSSID for each access point."""
    wlan_available_connection_type: Mapping[int, nisyscfg.enums.ConnectionType]
    """Available WLAN connection type for each access point."""
    wlan_available_security_type: Mapping[int, nisyscfg.enums.SecurityType]
    """Available WLAN security type for each access point."""
    wlan_available_link_quality: Mapping[int, int]
    """Available WLAN link quality for each access point."""
    wlan_available_channel_number: Mapping[int, int]
    """Available WLAN channel number for each access point."""
    wlan_available_link_speed: Mapping[int, nisyscfg.enums.LinkSpeed]
    """Available WLAN link speed for each access point."""
    cpu_total_load: Mapping[int, int]
    """Total CPU load for each CPU."""
    cpu_interrupt_load: Mapping[int, int]
    """CPU interrupt load for each CPU."""
    cpu_speed: Mapping[int, int]
    """CPU speed for each CPU."""
    fan_name: Mapping[int, str]
    """Name of each fan."""
    fan_reading: Mapping[int, int]
    """Reading of each fan."""
    power_name: Mapping[int, str]
    """Name of each power sensor."""
    power_reading: Mapping[int, float]
    """Reading of each power sensor."""
    power_upper_critical: Mapping[int, float]
    """Upper critical value for each power sensor."""
    temperature_name: Mapping[int, str]
    """Name of each temperature sensor."""
    temperature_reading: Mapping[int, float]
    """Reading of each temperature sensor."""
    temperature_lower_critical: Mapping[int, float]
    """Lower critical value for each temperature sensor."""
    temperature_upper_critical: Mapping[int, float]
    """Upper critical value for each temperature sensor."""
    voltage_name: Mapping[int, str]
    """Name of each voltage sensor."""
    voltage_reading: Mapping[int, float]
    """Reading of each voltage sensor."""
    voltage_nominal: Mapping[int, float]
    """Nominal voltage for each voltage sensor."""
    voltage_lower_critical: Mapping[int, float]
    """Lower critical voltage for each voltage sensor."""
    voltage_upper_critical: Mapping[int, float]
    """Upper critical voltage for each voltage sensor."""
    user_led_name: Mapping[int, str]
    """Name of each user LED indicator."""
    user_switch_name: Mapping[int, str]
    """Name of each user switch."""
    user_switch_state: Mapping[int, nisyscfg.enums.SwitchState]
    """State of each user switch."""
    user_led_state: Mapping[int, nisyscfg.enums.LedState]
    """State of each user LED indicator."""
    expert_name: Mapping[int, str]
    """Name of each expert."""
    expert_resource_name: Mapping[int, str]
    """Resource name for each expert."""
    expert_user_alias: Mapping[int, str]
    """User alias for each expert."""

    pxi: nisyscfg.pxi.hardware_resource.HardwareResource
    """The PXI properties."""

    xnet: nisyscfg.xnet.hardware_resource.HardwareResource
    """The XNET properties."""


class HardwareResourceIterator(collections.abc.Iterator):
    """Iterator for hardware resources in a NI System Configuration session.

    Iterates over hardware resources found in a session, providing access to each resource.
    """

    def __init__(self, session: nisyscfg.types.Handle, handle: nisyscfg.types.Handle) -> None:
        """Initializes the iterator.

        Args:
            session: The session handle.
            handle: The enumeration handle for hardware resources.
        """
        self._children: List[HardwareResource] = []
        self._session = session
        self._handle = handle
        self._library = nisyscfg._library_singleton.get()

    def __del__(self) -> None:
        """Destructor to ensure resources are released."""
        self.close()

    def __iter__(self) -> "HardwareResourceIterator":
        """Returns the iterator object itself."""
        return self

    def __next__(self) -> HardwareResource:
        """Returns the next hardware resource in the iteration.

        Returns:
            HardwareResource: The next hardware resource.

        Raises:
            StopIteration: If there are no more resources.
        """
        if not self._handle:
            raise StopIteration()
        resource_handle = nisyscfg.types.ResourceHandle()
        error_code = self._library.NextResource(
            self._session, self._handle, ctypes.pointer(resource_handle)
        )
        if error_code == nisyscfg.errors.Status.END_OF_ENUM:
            raise StopIteration()
        nisyscfg.errors.handle_error(None, error_code)
        resource = HardwareResource(resource_handle)
        self._children.append(resource)
        return resource

    def close(self) -> None:
        """Closes the iterator and releases associated resources."""
        self._children.reverse()
        for child in self._children:
            child.close()
        if self._handle:
            error_code = self._library.CloseHandle(self._handle)
            nisyscfg.errors.handle_error(None, error_code)
            self._handle = nisyscfg.types.Handle()
