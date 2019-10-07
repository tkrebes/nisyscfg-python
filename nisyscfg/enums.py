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


class ResourceProperty(CtypesEnum):
    IsDevice = 16781312
    IsChassis = 16941056
    ConnectsToBusType = 16785408
    VendorId = 16789504
    VendorName = 16793600
    ProductId = 16797696
    ProductName = 16801792
    SerialNumber = 16805888
    FirmwareRevision = 16969728
    IsNIProduct = 16809984
    IsSimulated = 16814080
    ConnectsToLinkName = 16818176
    HasDriver = 16920576
    IsPresent = 16924672
    SlotNumber = 16822272
    SupportsInternalCalibration = 16842752
    InternalCalibrationLastTime = 16846848
    InternalCalibrationLastTemp = 16850944
    SupportsExternalCalibration = 16859136
    ExternalCalibrationLastTemp = 16867328
    CalibrationComments = 16961536
    InternalCalibrationLastLimited = 17420288
    ExternalCalibrationChecksum = 17432576
    CurrentTemp = 16965632
    PxiPciBusNumber = 16875520
    PxiPciDeviceNumber = 16879616
    PxiPciFunctionNumber = 16883712
    PxiPciLinkWidth = 16973824
    PxiPciMaxLinkWidth = 16977920
    UsbInterface = 16887808
    TcpHostName = 16928768
    TcpMacAddress = 16986112
    TcpIpAddress = 16957440
    TcpDeviceClass = 17022976
    GpibPrimaryAddress = 16994304
    GpibSecondaryAddress = 16998400
    SerialPortBinding = 17076224
    ProvidesBusType = 16932864
    ProvidesLinkName = 16936960
    NumberOfSlots = 16826368
    SupportsFirmwareUpdate = 17080320
    FirmwareFilePattern = 17084416
    RecommendedCalibrationInterval = 17207296
    SupportsCalibrationWrite = 17215488
    HardwareRevision = 17256448
    CpuModelName = 17313792
    CpuSteppingRevision = 17317888
    ModelNameNumber = 17436672
    ModuleProgramMode = 17440768
    ConnectsToNumSlots = 17072128
    SlotOffsetLeft = 17276928
    InternalCalibrationValuesInRange = 17489920
    FirmwareUpdateMode = 17354752
    ExternalCalibrationLastTime = 16863232
    RecommendedNextCalibrationTime = 16871424
    ExternalCalibrationLastLimited = 17428480
    CalibrationCurrentPassword = 17223680
    CalibrationNewPassword = 17227776
    SysCfgAccess = 219504640
    AdapterType = 219332608
    MacAddress = 219168768
    AdapterMode = 219160576
    TcpIpRequestMode = 219172864
    TcpIpv4Address = 219181056
    TcpIpv4Subnet = 219189248
    TcpIpv4Gateway = 219193344
    TcpIpv4DnsServer = 219197440
    TcpPreferredLinkSpeed = 219213824
    TcpCurrentLinkSpeed = 219222016
    TcpPacketDetection = 219258880
    TcpPollingInterval = 219262976
    IsPrimaryAdapter = 219308032
    EtherCatMasterId = 219250688
    EtherCatMasterRedundancy = 219500544
    WlanBssid = 219398144
    WlanCurrentLinkQuality = 219394048
    WlanCurrentSsid = 219377664
    WlanCurrentConnectionType = 219381760
    WlanCurrentSecurityType = 219385856
    WlanCurrentEapType = 219389952
    WlanCountryCode = 219406336
    WlanChannelNumber = 219410432
    WlanClientCertificate = 219422720
    WlanSecurityIdentity = 219414528
    WlanSecurityKey = 219418624
    SystemStartTime = 17108992
    CurrentTime = 219279360
    TimeZone = 219471872
    UserDirectedSafeModeSwitch = 219537408
    ConsoleOutSwitch = 219541504
    IpResetSwitch = 219545600
    NumberOfDiscoveredAccessPoints = 219365376
    NumberOfExperts = 16891904
    NumberOfServices = 17010688
    NumberOfAvailableFirmwareVersions = 17088512
    NumberOfCpus = 17137664
    NumberOfFans = 17174528
    NumberOfPowerSensors = 17448960
    NumberOfTemperatureSensors = 17186816
    NumberOfVoltageSensors = 17149952
    NumberOfUserLedIndicators = 17281024
    NumberOfUserSwitches = 17293312


class IndexedProperty(CtypesEnum):
    ServiceType = 17014784
    AvailableFirmwareVersion = 17092608
    WlanAvailableSsid = 219336704
    WlanAvailableBssid = 219443200
    WlanAvailableConnectionType = 219340800
    WlanAvailableSecurityType = 219344896
    WlanAvailableLinkQuality = 219353088
    WlanAvailableChannelNumber = 219357184
    WlanAvailableLinkSpeed = 219361280
    CpuTotalLoad = 17141760
    CpuInterruptLoad = 17145856
    CpuSpeed = 17309696
    FanName = 17178624
    FanReading = 17182720
    PowerName = 17453056
    PowerReading = 17457152
    PowerUpperCritical = 17461248
    TemperatureName = 17190912
    TemperatureReading = 16965632
    TemperatureLowerCritical = 17195008
    TemperatureUpperCritical = 17199104
    VoltageName = 17154048
    VoltageReading = 17158144
    VoltageNominal = 17162240
    VoltageLowerCritical = 17166336
    VoltageUpperCritical = 17170432
    UserLedName = 17285120
    UserSwitchName = 17297408
    UserSwitchState = 17301504
    UserLedState = 17289216
    ExpertName = 16900096
    ExpertResourceName = 16896000
    ExpertUserAlias = 16904192


class SystemProperty(CtypesEnum):
    DeviceClass = 16941057
    ProductId = 16941058
    FileSystem = 16941060
    FirmwareRevision = 16941061
    IsFactoryResetSupported = 16941067
    IsFirmwareUpdateSupported = 16941068
    IsLocked = 16941069
    IsLockingSupported = 16941070
    IsOnLocalSubnet = 16941072
    IsRestartSupported = 16941076
    MacAddress = 16941077
    ProductName = 16941078
    OperatingSystem = 16941079
    OperatingSystemVersion = 17100800
    OperatingSystemDescription = 17104896
    SerialNumber = 16941080
    SystemState = 16941082
    MemoryPhysTotal = 219480064
    MemoryPhysFree = 219484160
    MemoryLargestBlock = 219488256
    MemoryVirtTotal = 219492352
    MemoryVirtFree = 219496448
    PrimaryDiskTotal = 219291648
    PrimaryDiskFree = 219295744
    SystemResourceHandle = 16941086
    ImageDescription = 219516928
    ImageId = 219521024
    ImageTitle = 219525120
    ImageVersion = 219529216
    InstalledApiVersion = 16941087
    IsDst = 16941066
    IsRestartProtected = 16941073
    HaltOnError = 16941074
    RepositoryLocation = 16941084
    SystemComment = 16941081
    AutoRestartTimeout = 16941085
    DnsServer = 16941059
    Gateway = 16941062
    Hostname = 16941063
    IpAddress = 16941064
    IpAddressMode = 16941065
    SubnetMask = 16941083


class FilterProperty(CtypesEnum):
    IsDevice = 16781312
    IsChassis = 16941056
    ServiceType = 17014784
    ConnectsToBusType = 16785408
    ConnectsToLinkName = 16818176
    ProvidesBusType = 16932864
    VendorId = 16789504
    ProductId = 16797696
    SerialNumber = 16805888
    IsNIProduct = 16809984
    IsSimulated = 16814080
    SlotNumber = 16822272
    HasDriver = 16920576
    IsPresent = 16924672
    SupportsCalibration = 16908288
    SupportsFirmwareUpdate = 17080320
    ProvidesLinkName = 16936960
    ExpertName = 16900096
    ResourceName = 16896000
    UserAlias = 16904192


class PropertyType(CtypesEnum):
    Bool = 1
    Int = 2
    UnsignedInt = 3
    Double = 4
    String = 6
    Timestamp = 7

