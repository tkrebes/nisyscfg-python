from nisyscfg.properties import (
    BitmaskProperty,
    IntProperty,
    UnsignedIntProperty,
    IndexedStringProperty,
    IndexedUnsignedIntProperty,
    IndexedDoubleProperty,
)
from nisyscfg.pxi.enums import (
    Clock10Sources,
    ExternalClockOutputSources,
    InternalOscillators,
    FanModes,
    CoolingProfiles,
    PowerSupplyStates,
    InhibitModes,
    CalExtActions,
)


class Resource(object):
    # Chassis attributes
    PXI_CHASSIS_NUMBER = UnsignedIntProperty(184565760)

    # Clock attributes
    CLK10_SOURCE = IntProperty(184635392, Clock10Sources)
    # Sets the source for external CLK10 Reference Clock outputs on the
    # chassis. The default is PXI_CLK10 from the backplane, which itself may
    # be sourced from various inputs. To achieve minimal phase offset of the
    # PXI_CLK10 reference clock between multiple chassis, set this attribute
    # to NISysCfgPxiExternalClockOutputSourceInternalOscillator, then split
    # the signal from the 10 MHz REF OUT connector using matched-length
    # cabling to the 10 Mhz REF IN connector on each chassis requiring minimal
    # phase offset. For best results, use the same model of chassis. */
    EXTERNAL_CLOCK_OUTPUT_SOURCE = IntProperty(184639488, ExternalClockOutputSources)
    INTERNAL_OSCILLATOR = IntProperty(184643584, InternalOscillators)

    # Fan control attributes
    FAN_MODE = UnsignedIntProperty(185597952, FanModes)
    FAN_USER_RPM = UnsignedIntProperty(185602048)
    SUPPORTED_FAN_MODES = BitmaskProperty(185606144, FanModes)
    FAN_MANUAL_RPM_LOWER_BOUND = UnsignedIntProperty(185634816)
    FAN_MANUAL_RPM_UPPER_BOUND = UnsignedIntProperty(185638912)
    COOLING_PROFILE = UnsignedIntProperty(185610240, CoolingProfiles)
    SUPPORTED_COOLING_PROFILES = BitmaskProperty(185614336, CoolingProfiles)

    # Power supply attributes
    POWER_SUPPLY_BAY_COUNT = IntProperty(186777600)
    POWER_SUPPLIES_REDUNDANT = UnsignedIntProperty(186798080)
    INHIBIT_MODE = UnsignedIntProperty(186806272, InhibitModes)
    SUPPORTED_INHIBIT_MODES = BitmaskProperty(186810368, InhibitModes)

    # Calibration attributes
    CAL_EXT_ACTION = UnsignedIntProperty(186908672, CalExtActions)
    CAL_EXT_DAC_VALUE = UnsignedIntProperty(186925056)


class IndexedResource(object):
    # Power supply index attributes
    POWER_SUPPLY_NAME = IndexedStringProperty(186781696, Resource.POWER_SUPPLY_BAY_COUNT)
    POWER_SUPPLY_STATE = IndexedUnsignedIntProperty(186789888, Resource.POWER_SUPPLY_BAY_COUNT, PowerSupplyStates)
    POWER_SUPPLY_POWER = IndexedUnsignedIntProperty(186793984, Resource.POWER_SUPPLY_BAY_COUNT)  #: (Watts)
    POWER_SUPPLY_POWER_READING = IndexedDoubleProperty(186822656, Resource.POWER_SUPPLY_BAY_COUNT)  #: (Watts)
    POWER_SUPPLY_INTAKE_TEMP = IndexedDoubleProperty(186802176, Resource.POWER_SUPPLY_BAY_COUNT)  #: (degrees Celsius)
    POWER_SUPPLY_POWER_LINE_FREQUENCY = IndexedUnsignedIntProperty(186785792, Resource.POWER_SUPPLY_BAY_COUNT)  #: (Hertz)
