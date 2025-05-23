"""Documentation for PXI HardwareResource properties."""

from typing import Mapping, Protocol, Union

import nisyscfg.enums
import nisyscfg.pxi.enums


class HardwareResource(Protocol):
    """PXI HardwareResource properties."""

    # Chassis attributes
    pxi_chassis_number: int
    """PXI chassis number."""
    chassis_led_blink_pattern: int
    """Chassis LED blink pattern."""

    # Clock attributes
    clk10_source: Union[nisyscfg.pxi.enums.Clock10Sources, int]
    """Source for external CLK10 Reference Clock outputs."""
    external_clock_output_source: Union[nisyscfg.pxi.enums.ExternalClockOutputSources, int]
    """Source for external clock output."""
    internal_oscillator: Union[nisyscfg.pxi.enums.InternalOscillators, int]
    """Internal oscillator selection."""
    high_density_trig_port_count: int
    """Number of high-density trigger ports."""

    # Fan control attributes
    fan_mode: Union[nisyscfg.pxi.enums.FanModes, int]
    """Fan mode."""
    fan_user_rpm: int
    """User-specified fan RPM."""
    supported_fan_modes: Union[nisyscfg.pxi.enums.FanModes, int]
    """Supported fan modes."""
    fan_manual_rpm_lower_bound: int
    """Lower bound for manual fan RPM."""
    fan_manual_rpm_upper_bound: int
    """Upper bound for manual fan RPM."""
    cooling_profile: Union[nisyscfg.pxi.enums.CoolingProfiles, int]
    """Cooling profile."""
    cooling_profile_source: Union[nisyscfg.pxi.enums.CoolingProfileSource, int]
    """Source of the cooling profile."""
    supported_cooling_profiles: Union[nisyscfg.pxi.enums.CoolingProfiles, int]
    """Supported cooling profiles."""
    enable_user_override_of_cooling_profile: bool
    """Allow user override of cooling profile."""

    # Power supply attributes
    power_supply_bay_count: int
    """Number of power supply bays."""
    power_supplies_redundant: int
    """Whether power supplies are redundant."""
    inhibit_mode: Union[nisyscfg.pxi.enums.InhibitModes, int]
    """Inhibit mode."""
    supported_inhibit_modes: Union[nisyscfg.pxi.enums.InhibitModes, int]
    """Supported inhibit modes."""

    # Calibration attributes
    cal_ext_action: Union[nisyscfg.pxi.enums.CalExtActions, int]
    """External calibration action."""
    cal_ext_dac_value: int
    """External calibration DAC value."""

    # Power supply index attributes
    power_supply_name: Mapping[int, str]
    """Name of each power supply."""
    power_supply_state: Mapping[int, Union[nisyscfg.pxi.enums.PowerSupplyStates, int]]
    """State of each power supply."""
    power_supply_power: Mapping[int, int]
    """Power rating (Watts) of each power supply."""
    power_supply_power_reading: Mapping[int, float]
    """Power reading (Watts) of each power supply."""
    power_supply_intake_temp: Mapping[int, float]
    """Intake temperature (°C) of each power supply."""
    power_supply_power_line_frequency: Mapping[int, int]
    """Power line frequency (Hz) of each power supply."""

    # High Density Trigger Port index Attributes
    trig_port_name: Mapping[int, str]
    """Name of each high density trigger port."""
    trig_port_state: Mapping[int, Union[nisyscfg.pxi.enums.PxiHighDensityTrigPortState, int]]
    """State of each high density trigger port."""
    trig_port_remove_device_alias: Mapping[int, str]
    """Remove device alias for each high density trigger port."""
