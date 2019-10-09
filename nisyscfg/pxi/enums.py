from nisyscfg.enums import BaseEnum


class Clock10Sources(BaseEnum):
    UNKNOWN = -1  #: Not applicable, or not software-readable
    INTERNAL = 0  #: Internal Oscillator
    BUILT_IN_CONNECTOR = 1  #: Supplied by the dedicated 10 MHz REF IN connector (e.g. SMA or SMB)
    TIMING_MODULE = 2  #: System Timing Module
    TRIG_10MHZ_PORT0 = 3  #: TRIG / 10 MHz Port 0 / REF IN


class ExternalClockOutputSources(BaseEnum):
    UNKNOWN = -1  #: Not applicable, or not software-readable
    PXI_CLK10 = 0  #: PXI_CLK10 from the chassis backplane
    INTERNAL_OSCILLATOR = 1  #: Internal Oscillator


class InternalOscillators(BaseEnum):
    UNSUPPORTED = -1  #: Not software-readable
    VCXO = 0  #: Voltage-controlled Oscillator
    OCXO = 1  #: Oven-controlled Oscillator


class FanModes(BaseEnum):
    AUTO = 1  #: Default operating mode
    SAFE_MANUAL = 2  #: Allows caller to manipulate the fan speed within safe boundaries by setting FanUserRpm
    HIGH = 4  #: Fans run at the maximum speed for the current cooling profile


class CoolingProfiles(BaseEnum):
    WATTS_38 = 1  #: Default operating mode
    WATTS_58 = 2  #: More aggressive cooling profile for cooling modules requiring 58W or less of cooling
    WATTS_82 = 4  #: More aggressive cooling profile for cooling modules requiring 82W or less of cooling


class PowerSupplyStates(BaseEnum):
    OFF = 0
    ON = 1
    FAULTED = 2
    FAULT_OUTPUT_VOLTAGE_OVERVOLTAGE_12V = 16
    FAULT_OUTPUT_VOLTAGE_UNDERVOLTAGE_12V = 17
    FAULT_OUTPUT_VOLTAGE_OVERVOLTAGE_5V_AUX = 18
    FAULT_OUTPUT_VOLTAGE_UNDERVOLTAGE_5V_AUX = 19
    FAULT_OUTPUT_CURRENT_OVERCURRENT_12V = 20
    FAULT_OUTPUT_CURRENT_OVERCURRENT_5V_AUX = 21
    FAULT_INPUT_VOLTAGE_OVERVOLTAGE = 22
    FAULT_INPUT_VOLTAGE_UNDERVOLTAGE = 23
    FAULT_LOWER_AMBIENT_TEMPERATURE = 24
    FAULT_UPPER_AMBIENT_TEMPERATURE = 25
    FAULT_LOWER_INTERNAL_TEMPERATURE = 26
    FAULT_UPPER_INTERNAL_TEMPERATURE = 27
    FAULT_FAN = 28
    ALERT_OUTPUT_VOLTAGE_OVERVOLTAGE_12V = 48
    ALERT_OUTPUT_VOLTAGE_UNDERVOLTAGE_12V = 49
    ALERT_OUTPUT_VOLTAGE_OVERVOLTAGE_5V_AUX = 50
    ALERT_OUTPUT_VOLTAGE_UNDERVOLTAGE_5V_AUX = 51
    ALERT_OUTPUT_CURRENT_OVERCURRENT_12V = 52
    ALERT_OUTPUT_CURRENT_OVERCURRENT_5V_AUX = 53
    ALERT_OUTPUT_CURRENT_SHARING = 54
    ALERT_INPUT_VOLTAGE_OVERVOLTAGE = 55
    ALERT_INPUT_VOLTAGE_UNDERVOLTAGE = 56
    ALERT_LOWER_AMBIENT_TEMPERATURE = 57
    ALERT_UPPER_AMBIENT_TEMPERATURE = 58
    ALERT_LOWER_INTERNAL_TEMPERATURE = 59
    ALERT_UPPER_INTERNAL_TEMPERATURE = 60
    ALERT_FAN = 61


class InhibitModes(BaseEnum):
    DEFAULT = 1  #: Chassis power controlled by the power button and OS
    MANUAL = 2  #: Chassis power controlled by the Remote Inhibit signal


class CalExtActions(BaseEnum):
    CANCEL = 0
    OCXO_START = 1
    COMMIT = 2
