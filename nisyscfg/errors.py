# This file is code generated

import platform
import warnings

from nisyscfg.enums import BaseEnum


def _is_success(code):
    return code == 0


def _is_error(code):
    return code < 0


def _is_warning(code):
    return code > 0


class Error(Exception):
    def __init__(self, message):
        super(Error, self).__init__(message)


class LibraryError(Error):
    def __init__(self, code, description):
        assert _is_error(code), "Should not raise Error if code is not fatal."
        self.code = code
        self.description = description
        if self.description:
            message = str(self.code) + ": " + self.description
        else:
            message = str(self.code) + ":"
        super(LibraryError, self).__init__(message)


class LibraryWarning(Warning):
    def __init__(self, code, description):
        assert _is_warning(code), "Should not create Warning if code is not positive."
        self.code = code
        self.description = description
        if self.description:
            message = "Warning {0} occurred.\n{1}".format(str(code), description)
        else:
            message = "Warning {0} occurred.".format(str(code))
        super(LibraryWarning, self).__init__(message)


class UnsupportedPlatformError(Error):
    def __init__(self):
        super(UnsupportedPlatformError, self).__init__(
            "Platform is unsupported: " + platform.architecture()[0] + " " + platform.system()
        )


class LibraryNotInstalledError(Error):
    def __init__(self):
        super(LibraryNotInstalledError, self).__init__(
            "The NI System Configuration runtime could not be loaded. Make sure"
            " it is installed and its bitness matches that of your Python"
            " interpreter. Please visit http://www.ni.com/downloads/drivers/ to"
            " download and install it."
        )


def handle_error(session, code, ignore_warnings=False, is_error_handling=False):
    if _is_success(code) or (_is_warning(code) and ignore_warnings):
        return

    try:
        status = Status(code)
        # Only lookup descriptions for nisyscfg status codes
        if is_error_handling:
            # The caller is in the midst of error handling and an error occurred.
            # Don't try to get the description or we'll start recursing until the stack overflows.
            description = ""
        else:
            description = session._get_status_description(code)
    except Exception:
        status = code
        description = ""

    if _is_error(code):
        raise LibraryError(status, description)

    assert _is_warning(code)
    warnings.warn(LibraryWarning(status, description))


warnings.filterwarnings("always", category=LibraryWarning)


class Status(BaseEnum):
    OK = 0
    END_OF_ENUM = 1
    SELF_TEST_BASIC_ONLY = 263024
    FOUND_CACHED_OFFLINE_SYSTEM = 263168
    RESTART_LOCALHOST_INITIATED = 263169
    CHANGED_PROPERTY_NOT_SAVED = 263170
    NOT_IMPLEMENTED = -2147467263
    NULL_POINTER = -2147467261
    FAIL = -2147467259
    UNEXPECTED = -2147418113
    OUT_OF_MEMORY = -2147024882
    INVALID_ARG = -2147024809
    OPERATION_TIMED_OUT = -2147220448
    FILE_NOT_FOUND = -2147220322
    INVALID_MAC_FORMAT = -2147220278
    PROP_MISMATCH = -2147220624
    PROP_DOES_NOT_EXIST = -2147220623
    URI_ILLEGAL_SYNTAX = -2147220622
    URI_TARGET_DOES_NOT_EXIST = -2147220621
    URI_EXPERT_DOES_NOT_EXIST = -2147220620
    ITEM_DOES_NOT_EXIST = -2147220619
    INVALID_MODE = -2147220618
    SYS_CONFIG_API_NOT_INSTALLED = -2147220616
    NAME_SYNTAX_ILLEGAL = -2147220614
    NAME_COLLISION = -2147220613
    NO_PROP_VALIDATED = -2147220612
    URI_UNAUTHORIZED = -2147220611
    RENAME_RESOURCE_DEPENDENCIES = -2147220610
    VALUE_INVALID = -2147220609
    VALUES_INCONSISTENT = -2147220608
    CANCELED = -2147220607
    RESPONSE_SYNTAX = -2147220606
    RESOURCE_IS_NOT_PRESENT = -2147220605
    RESOURCE_IS_SIMULATED = -2147220604
    NOT_IN_FIRMWARE_UPDATE_STATE = -2147220603
    FIRMWARE_IMAGE_DEVICE_MISMATCH = -2147220602
    FIRMWARE_IMAGE_CORRUPT = -2147220601
    INVALID_FIRMWARE_VERSION = -2147220600
    OLDER_FIRMWARE_VERSION = -2147220599
    INVALID_LOGIN_CREDENTIALS = -2147220598
    FIRMWARE_UPDATE_ATTEMPT_FAILED = -2147220597
    ENCRYPTION_FAILED = -2147220596
    SOME_PROPS_NOT_VALIDATED = -2147220595
    INVALID_CALIBRATION_CREDENTIALS = -2147220594
    CANNOT_DELETE_PRESENT_RESOURCE = -2147220593
    URI_TARGET_TRANSMIT_ERROR = -2147220592
    DECRYPTION_FAILED = -2147220591
    FIRMWARE_EXPERT_VERSION_MISMATCH = -2147220590
    AMBIGUOUS_IMPORT_ACTION = -2147220589
    REQUIRED_ITEM_FAILED_IMPORT = -2147220588
    ITEM_IN_USE = -2147220587
    ITEM_TYPE_NOT_SUPPORTED = -2147220586
    PERMISSION_DENIED = -2147220560
    SYSTEM_NOT_FOUND = -2147220559
    TRANSFORM_FAILED = -2147220558
    NOT_INSTALLED = -2147220557
    LAUNCH_FAILURE = -2147220556
    INTERNAL_TIMEOUT = -2147220555
    MISSING_TRANSFORM = -2147220554
    INCORRECT_EXTENSION = -2147220553
    FILE_READ_ONLY = -2147220552
    REPORT_OVERWRITE = -2147220551
    DIRECTORY_ERROR = -2147220550
    CANNOT_OPEN_FILE = -2147220480
    INSUFFICIENT_PERMISSIONS = -2147220479
    NCE_COPIER_FAILED = -2147220478
    FILE_OPERATION_FAILED = -2147220477
    NAME_COLLISION_ERROR = -2147220476
    UNEXPECTED_ERROR = -2147220475
    NCE_NO_STREAM_ERROR = -2147220474
    NCE_COMPRESSION_ERROR = -2147220473
    NCE_STREAM_READ_ERROR = -2147220472
    NCE_STREAM_WRITE_ERROR = -2147220471
    NCE_STREAM_SEEK_ERROR = -2147220470
    NCE_REPO_NOT_READY = -2147220469
    NCE_REPO_INVALID = -2147220468
    NCE_REPO_INCOMPAT = -2147220467
    NCE_NO_IMPORT_STORAGE = -2147220466
    NCE_NO_EXPORT_STORAGE = -2147220465
    NCE_NO_OBJ_COPIER = -2147220464
    COPY_IN_PROGRESS = -2147220463
    FILE_NOT_RECOGNIZED = -2147220462
    SYSTEM_NOT_SUPPORTED = -2147220461
    SYSTEM_NOT_REACHABLE = -2147220460
    PRODUCT_SOFTWARE_NOT_INSTALLED = -2147220459
    PRODUCT_SOFTWARE_TOO_OLD = -2147220458
    PRODUCT_SOFTWARE_TOO_NEW = -2147220457
    DATA_TOO_OLD = -2147220456
    DATA_TOO_NEW = -2147220455
    NO_ITEMS_TO_COPY = -2147220454
    ORPHAN_ITEMS = -2147220453
    DIRTY_ITEMS = -2147220452
    FILE_OVERWRITE = -2147220451
    ITEM_OVERWRITE = -2147220450
    MISSING_DEPENDENCY = -2147220449
    OPERATION_CANCELED = -2147220447
    WARNING_CONFLICTS = -2147220446
    ERROR_CONFLICTS = -2147220445
    ITEMS_REQUIRE_USER_INPUT = -2147220444
    PRODUCT_EXPERT_NOT_READY = -2147220443
    ORPHAN_FILES = -2147220442
    IS_CONST = -2147220441
    UNSUPPORTED_PRODUCT_MODE = -2147220440
    INSTALL_OPTION_NOT_SUPPORTED = -2147220381
    FIRMWARE_TOO_OLD = -2147220380
    SOFTWARE_TOO_OLD = -2147220379
    REQUIRES_SSH = -2147220378
    OPKG_RESPONSE_SYNTAX = -2147220377
    WRONG_SOFTWARE_SET_TYPE = -2147220376
    REQUIRES_OPKG = -2147220375
    HD_FORMAT_ENCRYPT_NOT_SUPPORTED = -2147220374
    HD_FORMAT_NO_RECOVERY_KEY_DEVICE = -2147220373
    RESTART_LOCALHOST_AMBIGUOUS = -2147220372
    IMAGE_INVALID_CORRUPT = -2147220371
    SAFE_OR_INSTALL_MODE_REQUIRED = -2147220370
    ENCRYPT_PHRASE_MISMATCH = -2147220369
    INVALID_IP = -2147220368
    INVALID_GATEWAY = -2147220367
    INVALID_DNS = -2147220366
    INVALID_SUBNET = -2147220365
    CMD_NOT_SUPPORTED = -2147220364
    CONFIG_FAILED = -2147220363
    LOCKED = -2147220362
    BAD_PASSWORD = -2147220361
    NOT_CONFIGURABLE = -2147220360
    UNLOCK_FAILED = -2147220359
    LOCK_FAILED = -2147220358
    INSTALL_FAILED = -2147220357
    INSTALLATION_CORRUPT = -2147220356
    EMPTY_FILE = -2147220355
    UNCONFIGURED_IP = -2147220354
    INSTALLATION_GENERIC_FAILURE = -2147220352
    DOWNLOAD_ALREADY_STARTED = -2147220350
    ABORTED = -2147220349
    DISK_FULL = -2147220338
    HD_FORMAT_FAILED = -2147220337
    HD_FORMAT_NOT_SAFE_MODE = -2147220336
    HD_FORMAT_REBOOT_FAILED = -2147220335
    CONNECTION_REFUSED = -2147220334
    GET_REMOTE_FILES_FAILED = -2147220331
    PUT_REMOTE_FILES_FAILED = -2147220330
    INVALID_IMAGE = -2147220329
    IMAGE_DEVICE_CODE_MISMATCH = -2147220328
    SYSTEM_MISMATCH = -2147220327
    HD_FORMAT_WRONG_FS = -2147220326
    CUSTOM_INSTALL_NOT_SUPPORTED = -2147220325
    FTP_FAILED = -2147220324
    TIMEOUT = -2147220323
    DIR_NOT_FOUND = -2147220321
    PATH_NOT_FOUND = -2147220320
    NO_SOFTWARE_AVAILABLE = -2147220319
    OVERWRITE_ERROR = -2147220318
    HD_FORMAT_CANNOT_KEEP_CFG = -2147220317
    FILE_OR_PATH_TOO_LONG = -2147220316
    DDP_INTERNAL_TIMEOUT = -2147220315
    IO_PERMISSION_DENIED = -2147220314
    PATH_ALREADY_EXISTS = -2147220313
    EXECUTION_FAILURE = -2147220312
    DOWNLOAD_ERROR = -2147220311
    NET_SEND_FAILED = -2147220309
    CONTACT_HOST_DISCONNECTED = -2147220308
    NET_SVC_DOWN = -2147220307
    NOT_CONFIRMED = -2147220306
    HOST_NOT_RESOLVED = -2147220305
    REBOOT_TIMEOUT = -2147220304
    NO_CONFIRMATION_FP1600 = -2147220303
    DUPLICATE_STARTUP = -2147220300
    REMOTE_INVALID_ARGUMENT = -2147220299
    NOT_UNINSTALLABLE = -2147220298
    DUPLICATES_NOT_ALLOWED = -2147220297
    NOT_INSTALLABLE = -2147220296
    WRONG_DEVICE = -2147220295
    WRONG_OS = -2147220294
    OS_VERSION_TOO_OLD = -2147220293
    IO_ERROR = -2147220292
    CORRUPT_CONFIG = -2147220291
    BUFFER_OVERFLOW = -2147220290
    UNSUPPORTED_CDF_VERSION = -2147220289
    INVALID_STACK = -2147220288
    INCOMPLETE_STACK = -2147220287
    STACK_ITEM_MISSING = -2147220286
    TOP_LEVEL_HIDDEN_COMPONENT_ERROR = -2147220285
    INVALID_ADDON = -2147220284
    NO_RT_IMAGES_FOLDER = -2147220283
    NO_RT_IMAGES_REGISTRY = -2147220282
    NO_RTS2_CDF = -2147220281
    UNSUPPORTED_OS = -2147220280
    EXACT_VERSION_REQUIRED = -2147220279
    INVALID_STARTUP = -2147220277
