# This file is code generated

import platform
import warnings

from nisyscfg.enums import CtypesEnum


def _is_success(code):
    return (code == 0)


def _is_error(code):
    return (code < 0)


def _is_warning(code):
    return (code > 0)


class Error(Exception):
    def __init__(self, message):
        super(Error, self).__init__(message)


class LibraryError(Error):
    def __init__(self, code, description):
        assert (_is_error(code)), "Should not raise Error if code is not fatal."
        self.code = code
        self.description = description
        if self.description:
            message = str(self.code) + ": " + self.description
        else:
            message = str(self.code) + ":"
        super(LibraryError, self).__init__(message)


class LibraryWarning(Warning):
    def __init__(self, code, description):
        assert (_is_warning(code)), "Should not create Warning if code is not positive."
        if self.description:
            message = 'Warning {0} occurred.\n{1}'.format(str(code), description)
        else:
            message = 'Warning {0} occurred.'.format(str(code))
        super(LibraryWarning, self).__init__(message)


class UnsupportedPlatformError(Error):
    def __init__(self):
        super(UnsupportedPlatformError, self).__init__('Platform is unsupported: ' + platform.architecture()[0] + ' ' + platform.system())


class LibraryNotInstalledError(Error):
    def __init__(self):
        super(LibraryNotInstalledError, self).__init__('The NI System Configuration runtime could not be loaded. Make sure it is installed and its bitness matches that of your Python interpreter. Please visit http://www.ni.com/downloads/drivers/ to download and install it.')


def handle_error(session, code, ignore_warnings=False, is_error_handling=False):
    if _is_success(code) or (_is_warning(code) and ignore_warnings):
        return

    try:
        status = Status(code)
        # Only lookup descriptions for nisyscfg status codes
        if is_error_handling:
            # The caller is in the midst of error handling and an error occurred.
            # Don't try to get the description or we'll start recursing until the stack overflows.
            description = ''
        else:
            description = session._get_status_description(code)
    except Exception:
        status = code
        description = ''

    if _is_error(code):
        raise LibraryError(status, description)

    assert _is_warning(code)
    warnings.warn(LibraryWarning(status, description))


warnings.filterwarnings("always", category=LibraryWarning)


class Status(CtypesEnum):
    OK = 0
    EndOfEnum = 1
    SelfTestBasicOnly = 263024
    FoundCachedOfflineSystem = 263168
    RestartLocalhostInitiated = 263169
    ChangedPropertyNotSaved = 263170
    NotImplemented = -2147467263
    NullPointer = -2147467261
    Fail = -2147467259
    Unexpected = -2147418113
    OutOfMemory = -2147024882
    InvalidArg = -2147024809
    OperationTimedOut = -2147220448
    FileNotFound = -2147220322
    InvalidMACFormat = -2147220278
    PropMismatch = -2147220624
    PropDoesNotExist = -2147220623
    UriIllegalSyntax = -2147220622
    UriTargetDoesNotExist = -2147220621
    UriExpertDoesNotExist = -2147220620
    ItemDoesNotExist = -2147220619
    InvalidMode = -2147220618
    SysConfigAPINotInstalled = -2147220616
    NameSyntaxIllegal = -2147220614
    NameCollision = -2147220613
    NoPropValidated = -2147220612
    UriUnauthorized = -2147220611
    RenameResourceDependencies = -2147220610
    ValueInvalid = -2147220609
    ValuesInconsistent = -2147220608
    Canceled = -2147220607
    ResponseSyntax = -2147220606
    ResourceIsNotPresent = -2147220605
    ResourceIsSimulated = -2147220604
    NotInFirmwareUpdateState = -2147220603
    FirmwareImageDeviceMismatch = -2147220602
    FirmwareImageCorrupt = -2147220601
    InvalidFirmwareVersion = -2147220600
    OlderFirmwareVersion = -2147220599
    InvalidLoginCredentials = -2147220598
    FirmwareUpdateAttemptFailed = -2147220597
    EncryptionFailed = -2147220596
    SomePropsNotValidated = -2147220595
    InvalidCalibrationCredentials = -2147220594
    CannotDeletePresentResource = -2147220593
    UriTargetTransmitError = -2147220592
    DecryptionFailed = -2147220591
    FirmwareExpertVersionMismatch = -2147220590
    AmbiguousImportAction = -2147220589
    RequiredItemFailedImport = -2147220588
    ItemInUse = -2147220587
    ItemTypeNotSupported = -2147220586
    PermissionDenied = -2147220560
    SystemNotFound = -2147220559
    TransformFailed = -2147220558
    NotInstalled = -2147220557
    LaunchFailure = -2147220556
    InternalTimeout = -2147220555
    MissingTransform = -2147220554
    IncorrectExtension = -2147220553
    FileReadOnly = -2147220552
    ReportOverwrite = -2147220551
    DirectoryError = -2147220550
    CannotOpenFile = -2147220480
    InsufficientPermissions = -2147220479
    NCECopierFailed = -2147220478
    FileOperationFailed = -2147220477
    NameCollisionError = -2147220476
    UnexpectedError = -2147220475
    NCENoStreamError = -2147220474
    NCECompressionError = -2147220473
    NCEStreamReadError = -2147220472
    NCEStreamWriteError = -2147220471
    NCEStreamSeekError = -2147220470
    NCERepoNotReady = -2147220469
    NCERepoInvalid = -2147220468
    NCERepoIncompat = -2147220467
    NCENoImportStorage = -2147220466
    NCENoExportStorage = -2147220465
    NCENoObjCopier = -2147220464
    CopyInProgress = -2147220463
    FileNotRecognized = -2147220462
    SystemNotSupported = -2147220461
    SystemNotReachable = -2147220460
    ProductSoftwareNotInstalled = -2147220459
    ProductSoftwareTooOld = -2147220458
    ProductSoftwareTooNew = -2147220457
    DataTooOld = -2147220456
    DataTooNew = -2147220455
    NoItemsToCopy = -2147220454
    OrphanItems = -2147220453
    DirtyItems = -2147220452
    FileOverwrite = -2147220451
    ItemOverwrite = -2147220450
    MissingDependency = -2147220449
    OperationCanceled = -2147220447
    WarningConflicts = -2147220446
    ErrorConflicts = -2147220445
    ItemsRequireUserInput = -2147220444
    ProductExpertNotReady = -2147220443
    OrphanFiles = -2147220442
    IsConst = -2147220441
    UnsupportedProductMode = -2147220440
    InstallOptionNotSupported = -2147220381
    FirmwareTooOld = -2147220380
    SoftwareTooOld = -2147220379
    RequiresSSH = -2147220378
    OpkgResponseSyntax = -2147220377
    WrongSoftwareSetType = -2147220376
    RequiresOpkg = -2147220375
    HDFormatEncryptNotSupported = -2147220374
    HDFormatNoRecoveryKeyDevice = -2147220373
    RestartLocalhostAmbiguous = -2147220372
    ImageInvalidCorrupt = -2147220371
    SafeOrInstallModeRequired = -2147220370
    EncryptPhraseMismatch = -2147220369
    InvalidIP = -2147220368
    InvalidGateway = -2147220367
    InvalidDNS = -2147220366
    InvalidSubnet = -2147220365
    CmdNotSupported = -2147220364
    ConfigFailed = -2147220363
    Locked = -2147220362
    BadPassword = -2147220361
    NotConfigurable = -2147220360
    UnlockFailed = -2147220359
    LockFailed = -2147220358
    InstallFailed = -2147220357
    InstallationCorrupt = -2147220356
    EmptyFile = -2147220355
    UnconfiguredIP = -2147220354
    InstallationGenericFailure = -2147220352
    DownloadAlreadyStarted = -2147220350
    Aborted = -2147220349
    DiskFull = -2147220338
    HDFormatFailed = -2147220337
    HDFormatNotSafeMode = -2147220336
    HDFormatRebootFailed = -2147220335
    ConnectionRefused = -2147220334
    GetRemoteFilesFailed = -2147220331
    PutRemoteFilesFailed = -2147220330
    InvalidImage = -2147220329
    ImageDeviceCodeMismatch = -2147220328
    SystemMismatch = -2147220327
    HDFormatWrongFS = -2147220326
    CustomInstallNotSupported = -2147220325
    FTPFailed = -2147220324
    Timeout = -2147220323
    DirNotFound = -2147220321
    PathNotFound = -2147220320
    NoSoftwareAvailable = -2147220319
    OverwriteError = -2147220318
    HDFormatCannotKeepCfg = -2147220317
    FileOrPathTooLong = -2147220316
    DDPInternalTimeout = -2147220315
    IOPermissionDenied = -2147220314
    PathAlreadyExists = -2147220313
    ExecutionFailure = -2147220312
    DownloadError = -2147220311
    NetSendFailed = -2147220309
    ContactHostDisconnected = -2147220308
    NetSvcDown = -2147220307
    NotConfirmed = -2147220306
    HostNotResolved = -2147220305
    RebootTimeout = -2147220304
    NoConfirmationFP1600 = -2147220303
    DuplicateStartup = -2147220300
    RemoteInvalidArgument = -2147220299
    NotUninstallable = -2147220298
    DuplicatesNotAllowed = -2147220297
    NotInstallable = -2147220296
    WrongDevice = -2147220295
    WrongOS = -2147220294
    OSVersionTooOld = -2147220293
    IOError = -2147220292
    CorruptConfig = -2147220291
    BufferOverflow = -2147220290
    UnsupportedCDFVersion = -2147220289
    InvalidStack = -2147220288
    IncompleteStack = -2147220287
    StackItemMissing = -2147220286
    TopLevelHiddenComponentError = -2147220285
    InvalidAddon = -2147220284
    NoRTImagesFolder = -2147220283
    NoRTImagesRegistry = -2147220282
    NoRTS2CDF = -2147220281
    UnsupportedOS = -2147220280
    ExactVersionRequired = -2147220279
    InvalidStartup = -2147220277

