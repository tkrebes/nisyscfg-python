# This file is code generated

from enum import IntEnum


class CtypesEnum(IntEnum):
    @classmethod
    def from_param(cls, obj):
        return int(obj)


class IncludeCachedResults(CtypesEnum):
    NONE = 0
    OnlyIfOnline = 1
    All = 3


class SystemNameFormat(CtypesEnum):
    Hostname = 16
    HostnameIp = 18
    HostnameMac = 19
    Ip = 32
    IpHostname = 33
    IpMac = 35
    Mac = 48
    MacHostname = 49
    MacIp = 50


class FileSystemMode(CtypesEnum):
    Default = 0
    Fat = 1
    Reliance = 2
    UBIFS = 16384
    Ext4 = 32768


class NetworkInterfaceSettings(CtypesEnum):
    ResetPrimaryResetOthers = 0
    PreservePrimaryResetOthers = 1
    PreservePrimaryPreserveOthers = 2
    PreservePrimaryApplyOthers = 3
    ApplyPrimaryResetOthers = 4
    ApplyPrimaryPreserveOthers = 5
    ApplyPrimaryApplyOthers = 6


class ComponentType(CtypesEnum):
    Standard = 0
    Hidden = 1
    System = 2
    Unknown = 3
    Startup = 4
    Image = 5
    Essential = 6


class IncludeComponentTypes(CtypesEnum):
    AllVisible = 0
    AllVisibleAndHidden = 1
    OnlyStandard = 2
    OnlyStartup = 3


class VersionSelectionMode(CtypesEnum):
    Highest = 0
    Exact = 1


class ImportMode(CtypesEnum):
    MergeItems = 0
    DeleteConfigFirst = 1048576
    PreserveConflictItems = 2097152


class ReportType(CtypesEnum):
    Xml = 0
    Html = 1
    TechnicalSupportZip = 2


class BusType(CtypesEnum):
    BuiltIn = 0
    PciPxi = 1
    Usb = 2
    Gpib = 3
    Vxi = 4
    Serial = 5
    TcpIp = 6
    CompactRio = 7
    Scxi = 8
    CompactDaq = 9
    SwitchBlock = 10
    Scc = 11
    FireWire = 12
    Accessory = 13
    Can = 14
    SwitchBlockDevice = 15


class HasDriverType(CtypesEnum):
    Unknown = - 1
    NotInstalled = 0
    Installed = 1


class IsPresentType(CtypesEnum):
    Initializing = - 2
    Unknown = - 1
    NotPresent = 0
    Present = 1


class IpAddressMode(CtypesEnum):
    Static = 1
    DhcpOrLinkLocal = 2
    LinkLocalOnly = 4
    DhcpOnly = 8


class Bool(CtypesEnum):
    FALSE = 0
    TRUE = 1


class Locale(CtypesEnum):
    Default = 0
    ChineseSimplified = 2052
    English = 1033
    French = 1036
    German = 1031
    Japanese = 1041
    Korean = 1042


class FilterMode(CtypesEnum):
    MatchValuesAll = 1
    MatchValuesAny = 2
    MatchValuesNone = 3
    AllPropertiesExist = 4


class ServiceType(CtypesEnum):
    MDnsNiTcp = 0
    MDnsNiRealtime = 1
    MDnsNiSysapi = 2
    MDnsNiHttp = 3
    LocalSystem = 4
    LocalNetInterface = 5
    LocalTimeKeeper = 6
    LocalTimeSource = 7
    MDnsLxi = 8
    LocalFpga = 9


class AdapterType(CtypesEnum):
    Ethernet = 1
    Wlan = 2


class AdapterMode(CtypesEnum):
    Disabled = 1
    TcpIpEthernet = 2
    Deterministic = 4
    EtherCat = 8
    TcpIpWlan = 32
    TcpIpAccessPoint = 64


class LinkSpeed(CtypesEnum):
    NONE = 0
    Auto = 1
    _10mbHalf = 2
    _10mbFull = 4
    _100mbHalf = 8
    _100mbFull = 16
    GigabitHalf = 32
    GigabitFull = 64
    Wlan80211a = 131072
    Wlan80211b = 262144
    Wlan80211g = 524288
    Wlan80211n = 1048576
    Wlan80211n5GHz = 2097152


class PacketDetection(CtypesEnum):
    NONE = 0
    LineInterrupt = 1
    Polling = 2
    SignaledInterrupt = 4


class ConnectionType(CtypesEnum):
    NONE = 0
    Infrastructure = 1
    AdHoc = 2


class SecurityType(CtypesEnum):
    NONE = 0
    NotSupported = 1
    Open = 2
    Wep = 4
    WpaPsk = 8
    WpaEap = 16
    Wpa2Psk = 32
    Wpa2Eap = 64


class EapType(CtypesEnum):
    NONE = 0
    EapTls = 1
    EapTtls = 2
    EapFast = 4
    Leap = 8
    Peap = 16


class FirmwareStatus(CtypesEnum):
    ReadyPendingAutoRestart = - 4
    VerifyingNewImage = - 3
    WritingFlashingNewImage = - 2
    UpdateModeWaitingForImage = - 1
    CorruptCannotRun = 0
    NoneInstalled = 1
    InstalledNormalOperation = 2
    ReadyPendingUserRestart = 3
    ReadyPendingUserAction = 4
    UpdateAttemptFailed = 5


class DeleteValidationMode(CtypesEnum):
    ValidateButDoNotDelete = - 1
    DeleteIfNoDependenciesExist = 0
    DeleteItemAndAnyDependencies = 1
    DeleteItemButKeepDependencies = 2


class AccessType(CtypesEnum):
    LocalOnly = 0
    LocalAndRemote = 1


class LedState(CtypesEnum):
    Off = 0
    SolidGreen = 1
    SolidYellow = 2
    BlinkingGreen = 4
    BlinkingYellow = 8


class SwitchState(CtypesEnum):
    Disabled = 0
    Enabled = 1


class FirmwareUpdateMode(CtypesEnum):
    NONE = 0
    Manual = 1
    DriverManaged = 2


class ModuleProgramMode(CtypesEnum):
    NONE = 0
    RealtimeCpu = 1
    RealtimeScan = 2
    LabVIEWFpga = 4


class PropertyType(CtypesEnum):
    Bool = 1
    Int = 2
    UnsignedInt = 3
    Double = 4
    String = 6
    Timestamp = 7

