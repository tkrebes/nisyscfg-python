# This file is code generated
# fmt: off

import ctypes
import threading

from nisyscfg.enums import *  # noqa: F403
from nisyscfg.errors import *  # noqa: F403
from nisyscfg.types import *  # noqa: F403


class Library(object):
    def __init__(self, ctypes_library):
        self._func_lock = threading.Lock()
        self._library = ctypes_library
        self._InitializeSession_cfunc = None
        self._CloseHandle_cfunc = None
        self._GetSystemExperts_cfunc = None
        self._SetRemoteTimeout_cfunc = None
        self._FindHardware_cfunc = None
        self._FindSystems_cfunc = None
        self._SelfTestHardware_cfunc = None
        self._SelfCalibrateHardware_cfunc = None
        self._ResetHardware_cfunc = None
        self._RenameResource_cfunc = None
        self._DeleteResource_cfunc = None
        self._GetResourceProperty_cfunc = None
        self._SetResourceProperty_cfunc = None
        self._SetResourcePropertyWithType_cfunc = None
        self._SetResourcePropertyV_cfunc = None
        self._SetResourcePropertyWithTypeV_cfunc = None
        self._GetResourceIndexedProperty_cfunc = None
        self._SaveResourceChanges_cfunc = None
        self._GetSystemProperty_cfunc = None
        self._SetSystemProperty_cfunc = None
        self._SetSystemPropertyV_cfunc = None
        self._SaveSystemChanges_cfunc = None
        self._CreateFilter_cfunc = None
        self._SetFilterProperty_cfunc = None
        self._SetFilterPropertyWithType_cfunc = None
        self._SetFilterPropertyV_cfunc = None
        self._SetFilterPropertyWithTypeV_cfunc = None
        self._UpgradeFirmwareFromFile_cfunc = None
        self._UpgradeFirmwareVersion_cfunc = None
        self._EraseFirmware_cfunc = None
        self._CheckFirmwareStatus_cfunc = None
        self._Format_cfunc = None
        self._FormatWithBaseSystemImage_cfunc = None
        self._Restart_cfunc = None
        self._GetAvailableSoftwareComponents_cfunc = None
        self._GetAvailableSoftwareSets_cfunc = None
        self._GetFilteredSoftwareComponents_cfunc = None
        self._GetFilteredSoftwareSets_cfunc = None
        self._GetFilteredBaseSystemImages_cfunc = None
        self._GetInstalledSoftwareComponents_cfunc = None
        self._GetInstalledSoftwareSet_cfunc = None
        self._GetSystemImageAsFolder_cfunc = None
        self._GetSystemImageAsFolder2_cfunc = None
        self._CreateSystemImageAsFolder_cfunc = None
        self._SetSystemImageFromFolder_cfunc = None
        self._SetSystemImageFromFolder2_cfunc = None
        self._InstallAll_cfunc = None
        self._InstallUninstallComponents_cfunc = None
        self._InstallUninstallComponents2_cfunc = None
        self._InstallSoftwareSet_cfunc = None
        self._InstallStartup_cfunc = None
        self._UninstallAll_cfunc = None
        self._GetSoftwareFeeds_cfunc = None
        self._AddSoftwareFeed_cfunc = None
        self._ModifySoftwareFeed_cfunc = None
        self._RemoveSoftwareFeed_cfunc = None
        self._ChangeAdministratorPassword_cfunc = None
        self._ExportConfiguration_cfunc = None
        self._ImportConfiguration_cfunc = None
        self._GenerateMAXReport_cfunc = None
        self._CreateComponentsEnum_cfunc = None
        self._AddComponentToEnum_cfunc = None
        self._FreeDetailedString_cfunc = None
        self._NextResource_cfunc = None
        self._NextSystemInfo_cfunc = None
        self._NextExpertInfo_cfunc = None
        self._NextComponentInfo_cfunc = None
        self._NextSoftwareSet_cfunc = None
        self._GetSoftwareSetInfo_cfunc = None
        self._NextDependencyInfo_cfunc = None
        self._NextSoftwareFeed_cfunc = None
        self._ResetEnumeratorGetCount_cfunc = None
        self._GetStatusDescription_cfunc = None
        self._TimestampFromValues_cfunc = None
        self._ValuesFromTimestamp_cfunc = None

    def InitializeSession(self, targetName, username, password, language, forcePropertyRefresh, connectTimeoutMsec, expertEnumHandle, sessionHandle):  # noqa: N802,N803
        with self._func_lock:
            if self._InitializeSession_cfunc is None:
                self._InitializeSession_cfunc = self._library.windll.NISysCfgInitializeSession
                self._InitializeSession_cfunc.argtypes = [ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), Locale, Bool, ctypes.c_uint, EnumExpertHandle, SessionHandle]  # noqa: F405
                self._InitializeSession_cfunc.restype = Status  # noqa: F405
        return self._InitializeSession_cfunc(targetName, username, password, language, forcePropertyRefresh, connectTimeoutMsec, expertEnumHandle, sessionHandle)

    def CloseHandle(self, syscfgHandle):  # noqa: N802,N803
        with self._func_lock:
            if self._CloseHandle_cfunc is None:
                self._CloseHandle_cfunc = self._library.windll.NISysCfgCloseHandle
                self._CloseHandle_cfunc.argtypes = [ctypes.c_void_p]  # noqa: F405
                self._CloseHandle_cfunc.restype = Status  # noqa: F405
        return self._CloseHandle_cfunc(syscfgHandle)

    def GetSystemExperts(self, sessionHandle, expertNames, expertEnumHandle):  # noqa: N802,N803
        with self._func_lock:
            if self._GetSystemExperts_cfunc is None:
                self._GetSystemExperts_cfunc = self._library.windll.NISysCfgGetSystemExperts
                self._GetSystemExperts_cfunc.argtypes = [SessionHandle, ctypes.POINTER(ctypes.c_char), EnumExpertHandle]  # noqa: F405
                self._GetSystemExperts_cfunc.restype = Status  # noqa: F405
        return self._GetSystemExperts_cfunc(sessionHandle, expertNames, expertEnumHandle)

    def SetRemoteTimeout(self, sessionHandle, remoteTimeoutMsec):  # noqa: N802,N803
        with self._func_lock:
            if self._SetRemoteTimeout_cfunc is None:
                self._SetRemoteTimeout_cfunc = self._library.windll.NISysCfgSetRemoteTimeout
                self._SetRemoteTimeout_cfunc.argtypes = [SessionHandle, ctypes.c_uint]  # noqa: F405
                self._SetRemoteTimeout_cfunc.restype = Status  # noqa: F405
        return self._SetRemoteTimeout_cfunc(sessionHandle, remoteTimeoutMsec)

    def FindHardware(self, sessionHandle, filterMode, filterHandle, expertNames, resourceEnumHandle):  # noqa: N802,N803
        with self._func_lock:
            if self._FindHardware_cfunc is None:
                self._FindHardware_cfunc = self._library.windll.NISysCfgFindHardware
                self._FindHardware_cfunc.argtypes = [SessionHandle, FilterMode, FilterHandle, ctypes.POINTER(ctypes.c_char), EnumResourceHandle]  # noqa: F405
                self._FindHardware_cfunc.restype = Status  # noqa: F405
        return self._FindHardware_cfunc(sessionHandle, filterMode, filterHandle, expertNames, resourceEnumHandle)

    def FindSystems(self, sessionHandle, deviceClass, detectOnlineSystems, cacheMode, findOutputMode, timeoutMsec, onlyInstallableSystems, systemEnumHandle):  # noqa: N802,N803
        with self._func_lock:
            if self._FindSystems_cfunc is None:
                self._FindSystems_cfunc = self._library.windll.NISysCfgFindSystems
                self._FindSystems_cfunc.argtypes = [SessionHandle, ctypes.POINTER(ctypes.c_char), Bool, IncludeCachedResults, SystemNameFormat, ctypes.c_uint, Bool, EnumSystemHandle]  # noqa: F405
                self._FindSystems_cfunc.restype = Status  # noqa: F405
        return self._FindSystems_cfunc(sessionHandle, deviceClass, detectOnlineSystems, cacheMode, findOutputMode, timeoutMsec, onlyInstallableSystems, systemEnumHandle)

    def SelfTestHardware(self, resourceHandle, mode, detailedResult):  # noqa: N802,N803
        with self._func_lock:
            if self._SelfTestHardware_cfunc is None:
                self._SelfTestHardware_cfunc = self._library.windll.NISysCfgSelfTestHardware
                self._SelfTestHardware_cfunc.argtypes = [ResourceHandle, ctypes.c_uint, ctypes.POINTER(ctypes.POINTER(ctypes.c_char))]  # noqa: F405
                self._SelfTestHardware_cfunc.restype = Status  # noqa: F405
        return self._SelfTestHardware_cfunc(resourceHandle, mode, detailedResult)

    def SelfCalibrateHardware(self, resourceHandle, detailedResult):  # noqa: N802,N803
        with self._func_lock:
            if self._SelfCalibrateHardware_cfunc is None:
                self._SelfCalibrateHardware_cfunc = self._library.windll.NISysCfgSelfCalibrateHardware
                self._SelfCalibrateHardware_cfunc.argtypes = [ResourceHandle, ctypes.POINTER(ctypes.POINTER(ctypes.c_char))]  # noqa: F405
                self._SelfCalibrateHardware_cfunc.restype = Status  # noqa: F405
        return self._SelfCalibrateHardware_cfunc(resourceHandle, detailedResult)

    def ResetHardware(self, resourceHandle, mode):  # noqa: N802,N803
        with self._func_lock:
            if self._ResetHardware_cfunc is None:
                self._ResetHardware_cfunc = self._library.windll.NISysCfgResetHardware
                self._ResetHardware_cfunc.argtypes = [ResourceHandle, ctypes.c_uint]  # noqa: F405
                self._ResetHardware_cfunc.restype = Status  # noqa: F405
        return self._ResetHardware_cfunc(resourceHandle, mode)

    def RenameResource(self, resourceHandle, newName, overwriteConflict, updateDependencies, nameAlreadyExisted, overwrittenResourceHandle):  # noqa: N802,N803
        with self._func_lock:
            if self._RenameResource_cfunc is None:
                self._RenameResource_cfunc = self._library.windll.NISysCfgRenameResource
                self._RenameResource_cfunc.argtypes = [ResourceHandle, ctypes.POINTER(ctypes.c_char), Bool, Bool, ctypes.POINTER(ctypes.c_int), ResourceHandle]  # noqa: F405
                self._RenameResource_cfunc.restype = Status  # noqa: F405
        return self._RenameResource_cfunc(resourceHandle, newName, overwriteConflict, updateDependencies, nameAlreadyExisted, overwrittenResourceHandle)

    def DeleteResource(self, resourceHandle, mode, dependentItemsDeleted, detailedResult):  # noqa: N802,N803
        with self._func_lock:
            if self._DeleteResource_cfunc is None:
                self._DeleteResource_cfunc = self._library.windll.NISysCfgDeleteResource
                self._DeleteResource_cfunc.argtypes = [ResourceHandle, DeleteValidationMode, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.POINTER(ctypes.c_char))]  # noqa: F405
                self._DeleteResource_cfunc.restype = Status  # noqa: F405
        return self._DeleteResource_cfunc(resourceHandle, mode, dependentItemsDeleted, detailedResult)

    def GetResourceProperty(self, resourceHandle, propertyID, value):  # noqa: N802,N803
        with self._func_lock:
            if self._GetResourceProperty_cfunc is None:
                self._GetResourceProperty_cfunc = self._library.windll.NISysCfgGetResourceProperty
                self._GetResourceProperty_cfunc.argtypes = [ResourceHandle, ctypes.c_uint, ctypes.c_void_p]  # noqa: F405
                self._GetResourceProperty_cfunc.restype = Status  # noqa: F405
        return self._GetResourceProperty_cfunc(resourceHandle, propertyID, value)

    def SetResourceProperty(self, resourceHandle, propertyID, args):  # noqa: N802,N803
        with self._func_lock:
            if self._SetResourceProperty_cfunc is None:
                self._SetResourceProperty_cfunc = self._library.cdll.NISysCfgSetResourceProperty
                self._SetResourceProperty_cfunc.restype = Status  # noqa: F405
        return self._SetResourceProperty_cfunc(resourceHandle, propertyID, args)

    def SetResourcePropertyWithType(self, resourceHandle, propertyID, propertyType, args):  # noqa: N802,N803
        with self._func_lock:
            if self._SetResourcePropertyWithType_cfunc is None:
                self._SetResourcePropertyWithType_cfunc = self._library.cdll.NISysCfgSetResourcePropertyWithType
                self._SetResourcePropertyWithType_cfunc.restype = Status  # noqa: F405
        return self._SetResourcePropertyWithType_cfunc(resourceHandle, propertyID, propertyType, args)

    def SetResourcePropertyV(self, resourceHandle, propertyID, args):  # noqa: N802,N803
        with self._func_lock:
            if self._SetResourcePropertyV_cfunc is None:
                self._SetResourcePropertyV_cfunc = self._library.windll.NISysCfgSetResourcePropertyV
                self._SetResourcePropertyV_cfunc.restype = Status  # noqa: F405
        return self._SetResourcePropertyV_cfunc(resourceHandle, propertyID, args)

    def SetResourcePropertyWithTypeV(self, resourceHandle, propertyID, propertyType, args):  # noqa: N802,N803
        with self._func_lock:
            if self._SetResourcePropertyWithTypeV_cfunc is None:
                self._SetResourcePropertyWithTypeV_cfunc = self._library.windll.NISysCfgSetResourcePropertyWithTypeV
                self._SetResourcePropertyWithTypeV_cfunc.restype = Status  # noqa: F405
        return self._SetResourcePropertyWithTypeV_cfunc(resourceHandle, propertyID, propertyType, args)

    def GetResourceIndexedProperty(self, resourceHandle, propertyID, index, value):  # noqa: N802,N803
        with self._func_lock:
            if self._GetResourceIndexedProperty_cfunc is None:
                self._GetResourceIndexedProperty_cfunc = self._library.windll.NISysCfgGetResourceIndexedProperty
                self._GetResourceIndexedProperty_cfunc.argtypes = [ResourceHandle, ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p]  # noqa: F405
                self._GetResourceIndexedProperty_cfunc.restype = Status  # noqa: F405
        return self._GetResourceIndexedProperty_cfunc(resourceHandle, propertyID, index, value)

    def SaveResourceChanges(self, resourceHandle, changesRequireRestart, detailedResult):  # noqa: N802,N803
        with self._func_lock:
            if self._SaveResourceChanges_cfunc is None:
                self._SaveResourceChanges_cfunc = self._library.windll.NISysCfgSaveResourceChanges
                self._SaveResourceChanges_cfunc.argtypes = [ResourceHandle, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.POINTER(ctypes.c_char))]  # noqa: F405
                self._SaveResourceChanges_cfunc.restype = Status  # noqa: F405
        return self._SaveResourceChanges_cfunc(resourceHandle, changesRequireRestart, detailedResult)

    def GetSystemProperty(self, sessionHandle, propertyID, value):  # noqa: N802,N803
        with self._func_lock:
            if self._GetSystemProperty_cfunc is None:
                self._GetSystemProperty_cfunc = self._library.windll.NISysCfgGetSystemProperty
                self._GetSystemProperty_cfunc.argtypes = [SessionHandle, ctypes.c_uint, ctypes.c_void_p]  # noqa: F405
                self._GetSystemProperty_cfunc.restype = Status  # noqa: F405
        return self._GetSystemProperty_cfunc(sessionHandle, propertyID, value)

    def SetSystemProperty(self, sessionHandle, propertyID, args):  # noqa: N802,N803
        with self._func_lock:
            if self._SetSystemProperty_cfunc is None:
                self._SetSystemProperty_cfunc = self._library.cdll.NISysCfgSetSystemProperty
                self._SetSystemProperty_cfunc.restype = Status  # noqa: F405
        return self._SetSystemProperty_cfunc(sessionHandle, propertyID, args)

    def SetSystemPropertyV(self, sessionHandle, propertyID, args):  # noqa: N802,N803
        with self._func_lock:
            if self._SetSystemPropertyV_cfunc is None:
                self._SetSystemPropertyV_cfunc = self._library.windll.NISysCfgSetSystemPropertyV
                self._SetSystemPropertyV_cfunc.restype = Status  # noqa: F405
        return self._SetSystemPropertyV_cfunc(sessionHandle, propertyID, args)

    def SaveSystemChanges(self, sessionHandle, changesRequireRestart, detailedResult):  # noqa: N802,N803
        with self._func_lock:
            if self._SaveSystemChanges_cfunc is None:
                self._SaveSystemChanges_cfunc = self._library.windll.NISysCfgSaveSystemChanges
                self._SaveSystemChanges_cfunc.argtypes = [SessionHandle, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.POINTER(ctypes.c_char))]  # noqa: F405
                self._SaveSystemChanges_cfunc.restype = Status  # noqa: F405
        return self._SaveSystemChanges_cfunc(sessionHandle, changesRequireRestart, detailedResult)

    def CreateFilter(self, sessionHandle, filterHandle):  # noqa: N802,N803
        with self._func_lock:
            if self._CreateFilter_cfunc is None:
                self._CreateFilter_cfunc = self._library.windll.NISysCfgCreateFilter
                self._CreateFilter_cfunc.argtypes = [SessionHandle, FilterHandle]  # noqa: F405
                self._CreateFilter_cfunc.restype = Status  # noqa: F405
        return self._CreateFilter_cfunc(sessionHandle, filterHandle)

    def SetFilterProperty(self, filterHandle, propertyID, args):  # noqa: N802,N803
        with self._func_lock:
            if self._SetFilterProperty_cfunc is None:
                self._SetFilterProperty_cfunc = self._library.cdll.NISysCfgSetFilterProperty
                self._SetFilterProperty_cfunc.restype = Status  # noqa: F405
        return self._SetFilterProperty_cfunc(filterHandle, propertyID, args)

    def SetFilterPropertyWithType(self, filterHandle, propertyID, propertyType, args):  # noqa: N802,N803
        with self._func_lock:
            if self._SetFilterPropertyWithType_cfunc is None:
                self._SetFilterPropertyWithType_cfunc = self._library.cdll.NISysCfgSetFilterPropertyWithType
                self._SetFilterPropertyWithType_cfunc.restype = Status  # noqa: F405
        return self._SetFilterPropertyWithType_cfunc(filterHandle, propertyID, propertyType, args)

    def SetFilterPropertyV(self, filterHandle, propertyID, args):  # noqa: N802,N803
        with self._func_lock:
            if self._SetFilterPropertyV_cfunc is None:
                self._SetFilterPropertyV_cfunc = self._library.windll.NISysCfgSetFilterPropertyV
                self._SetFilterPropertyV_cfunc.restype = Status  # noqa: F405
        return self._SetFilterPropertyV_cfunc(filterHandle, propertyID, args)

    def SetFilterPropertyWithTypeV(self, filterHandle, propertyID, propertyType, args):  # noqa: N802,N803
        with self._func_lock:
            if self._SetFilterPropertyWithTypeV_cfunc is None:
                self._SetFilterPropertyWithTypeV_cfunc = self._library.windll.NISysCfgSetFilterPropertyWithTypeV
                self._SetFilterPropertyWithTypeV_cfunc.restype = Status  # noqa: F405
        return self._SetFilterPropertyWithTypeV_cfunc(filterHandle, propertyID, propertyType, args)

    def UpgradeFirmwareFromFile(self, resourceHandle, firmwareFile, autoStopTasks, alwaysOverwrite, waitForOperationToFinish, firmwareStatus, detailedResult):  # noqa: N802,N803
        with self._func_lock:
            if self._UpgradeFirmwareFromFile_cfunc is None:
                self._UpgradeFirmwareFromFile_cfunc = self._library.windll.NISysCfgUpgradeFirmwareFromFile
                self._UpgradeFirmwareFromFile_cfunc.argtypes = [ResourceHandle, ctypes.POINTER(ctypes.c_char), Bool, Bool, Bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.POINTER(ctypes.c_char))]  # noqa: F405
                self._UpgradeFirmwareFromFile_cfunc.restype = Status  # noqa: F405
        return self._UpgradeFirmwareFromFile_cfunc(resourceHandle, firmwareFile, autoStopTasks, alwaysOverwrite, waitForOperationToFinish, firmwareStatus, detailedResult)

    def UpgradeFirmwareVersion(self, resourceHandle, firmwareVersion, autoStopTasks, alwaysOverwrite, waitForOperationToFinish, firmwareStatus, detailedResult):  # noqa: N802,N803
        with self._func_lock:
            if self._UpgradeFirmwareVersion_cfunc is None:
                self._UpgradeFirmwareVersion_cfunc = self._library.windll.NISysCfgUpgradeFirmwareVersion
                self._UpgradeFirmwareVersion_cfunc.argtypes = [ResourceHandle, ctypes.POINTER(ctypes.c_char), Bool, Bool, Bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.POINTER(ctypes.c_char))]  # noqa: F405
                self._UpgradeFirmwareVersion_cfunc.restype = Status  # noqa: F405
        return self._UpgradeFirmwareVersion_cfunc(resourceHandle, firmwareVersion, autoStopTasks, alwaysOverwrite, waitForOperationToFinish, firmwareStatus, detailedResult)

    def EraseFirmware(self, resourceHandle, autoStopTasks, firmwareStatus, detailedResult):  # noqa: N802,N803
        with self._func_lock:
            if self._EraseFirmware_cfunc is None:
                self._EraseFirmware_cfunc = self._library.windll.NISysCfgEraseFirmware
                self._EraseFirmware_cfunc.argtypes = [ResourceHandle, Bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.POINTER(ctypes.c_char))]  # noqa: F405
                self._EraseFirmware_cfunc.restype = Status  # noqa: F405
        return self._EraseFirmware_cfunc(resourceHandle, autoStopTasks, firmwareStatus, detailedResult)

    def CheckFirmwareStatus(self, resourceHandle, percentComplete, firmwareStatus, detailedResult):  # noqa: N802,N803
        with self._func_lock:
            if self._CheckFirmwareStatus_cfunc is None:
                self._CheckFirmwareStatus_cfunc = self._library.windll.NISysCfgCheckFirmwareStatus
                self._CheckFirmwareStatus_cfunc.argtypes = [ResourceHandle, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.POINTER(ctypes.c_char))]  # noqa: F405
                self._CheckFirmwareStatus_cfunc.restype = Status  # noqa: F405
        return self._CheckFirmwareStatus_cfunc(resourceHandle, percentComplete, firmwareStatus, detailedResult)

    def Format(self, sessionHandle, forceSafeMode, restartAfterFormat, fileSystem, networkSettings, timeoutMsec):  # noqa: N802,N803
        with self._func_lock:
            if self._Format_cfunc is None:
                self._Format_cfunc = self._library.windll.NISysCfgFormat
                self._Format_cfunc.argtypes = [SessionHandle, Bool, Bool, FileSystemMode, NetworkInterfaceSettings, ctypes.c_uint]  # noqa: F405
                self._Format_cfunc.restype = Status  # noqa: F405
        return self._Format_cfunc(sessionHandle, forceSafeMode, restartAfterFormat, fileSystem, networkSettings, timeoutMsec)

    def FormatWithBaseSystemImage(self, sessionHandle, autoRestart, fileSystem, networkSettings, systemImageID, systemImageVersion, timeoutMsec):  # noqa: N802,N803
        with self._func_lock:
            if self._FormatWithBaseSystemImage_cfunc is None:
                self._FormatWithBaseSystemImage_cfunc = self._library.windll.NISysCfgFormatWithBaseSystemImage
                self._FormatWithBaseSystemImage_cfunc.argtypes = [SessionHandle, Bool, FileSystemMode, NetworkInterfaceSettings, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.c_uint]  # noqa: F405
                self._FormatWithBaseSystemImage_cfunc.restype = Status  # noqa: F405
        return self._FormatWithBaseSystemImage_cfunc(sessionHandle, autoRestart, fileSystem, networkSettings, systemImageID, systemImageVersion, timeoutMsec)

    def Restart(self, sessionHandle, waitForRestartToFinish, installMode, flushDNS, timeoutMsec, newIpAddress):  # noqa: N802,N803
        with self._func_lock:
            if self._Restart_cfunc is None:
                self._Restart_cfunc = self._library.windll.NISysCfgRestart
                self._Restart_cfunc.argtypes = [SessionHandle, Bool, Bool, Bool, ctypes.c_uint, ctypes.POINTER(ctypes.c_char)]  # noqa: F405
                self._Restart_cfunc.restype = Status  # noqa: F405
        return self._Restart_cfunc(sessionHandle, waitForRestartToFinish, installMode, flushDNS, timeoutMsec, newIpAddress)

    def GetAvailableSoftwareComponents(self, sessionHandle, itemTypes, componentEnumHandle):  # noqa: N802,N803
        with self._func_lock:
            if self._GetAvailableSoftwareComponents_cfunc is None:
                self._GetAvailableSoftwareComponents_cfunc = self._library.windll.NISysCfgGetAvailableSoftwareComponents
                self._GetAvailableSoftwareComponents_cfunc.argtypes = [SessionHandle, IncludeComponentTypes, EnumSoftwareComponentHandle]  # noqa: F405
                self._GetAvailableSoftwareComponents_cfunc.restype = Status  # noqa: F405
        return self._GetAvailableSoftwareComponents_cfunc(sessionHandle, itemTypes, componentEnumHandle)

    def GetAvailableSoftwareSets(self, sessionHandle, setEnumHandle):  # noqa: N802,N803
        with self._func_lock:
            if self._GetAvailableSoftwareSets_cfunc is None:
                self._GetAvailableSoftwareSets_cfunc = self._library.windll.NISysCfgGetAvailableSoftwareSets
                self._GetAvailableSoftwareSets_cfunc.argtypes = [SessionHandle, EnumSoftwareSetHandle]  # noqa: F405
                self._GetAvailableSoftwareSets_cfunc.restype = Status  # noqa: F405
        return self._GetAvailableSoftwareSets_cfunc(sessionHandle, setEnumHandle)

    def GetFilteredSoftwareComponents(self, repositoryPath, deviceClass, operatingSystem, productID, itemTypes, componentEnumHandle):  # noqa: N802,N803
        with self._func_lock:
            if self._GetFilteredSoftwareComponents_cfunc is None:
                self._GetFilteredSoftwareComponents_cfunc = self._library.windll.NISysCfgGetFilteredSoftwareComponents
                self._GetFilteredSoftwareComponents_cfunc.argtypes = [ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.c_uint, IncludeComponentTypes, EnumSoftwareComponentHandle]  # noqa: F405
                self._GetFilteredSoftwareComponents_cfunc.restype = Status  # noqa: F405
        return self._GetFilteredSoftwareComponents_cfunc(repositoryPath, deviceClass, operatingSystem, productID, itemTypes, componentEnumHandle)

    def GetFilteredSoftwareSets(self, repositoryPath, deviceClass, operatingSystem, productID, setEnumHandle):  # noqa: N802,N803
        with self._func_lock:
            if self._GetFilteredSoftwareSets_cfunc is None:
                self._GetFilteredSoftwareSets_cfunc = self._library.windll.NISysCfgGetFilteredSoftwareSets
                self._GetFilteredSoftwareSets_cfunc.argtypes = [ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.c_uint, EnumSoftwareSetHandle]  # noqa: F405
                self._GetFilteredSoftwareSets_cfunc.restype = Status  # noqa: F405
        return self._GetFilteredSoftwareSets_cfunc(repositoryPath, deviceClass, operatingSystem, productID, setEnumHandle)

    def GetFilteredBaseSystemImages(self, repositoryPath, deviceClass, operatingSystem, productID, systemImageEnumHandle):  # noqa: N802,N803
        with self._func_lock:
            if self._GetFilteredBaseSystemImages_cfunc is None:
                self._GetFilteredBaseSystemImages_cfunc = self._library.windll.NISysCfgGetFilteredBaseSystemImages
                self._GetFilteredBaseSystemImages_cfunc.argtypes = [ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.c_uint, EnumSoftwareComponentHandle]  # noqa: F405
                self._GetFilteredBaseSystemImages_cfunc.restype = Status  # noqa: F405
        return self._GetFilteredBaseSystemImages_cfunc(repositoryPath, deviceClass, operatingSystem, productID, systemImageEnumHandle)

    def GetInstalledSoftwareComponents(self, sessionHandle, itemTypes, cached, componentEnumHandle):  # noqa: N802,N803
        with self._func_lock:
            if self._GetInstalledSoftwareComponents_cfunc is None:
                self._GetInstalledSoftwareComponents_cfunc = self._library.windll.NISysCfgGetInstalledSoftwareComponents
                self._GetInstalledSoftwareComponents_cfunc.argtypes = [SessionHandle, IncludeComponentTypes, Bool, EnumSoftwareComponentHandle]  # noqa: F405
                self._GetInstalledSoftwareComponents_cfunc.restype = Status  # noqa: F405
        return self._GetInstalledSoftwareComponents_cfunc(sessionHandle, itemTypes, cached, componentEnumHandle)

    def GetInstalledSoftwareSet(self, sessionHandle, cached, setHandle):  # noqa: N802,N803
        with self._func_lock:
            if self._GetInstalledSoftwareSet_cfunc is None:
                self._GetInstalledSoftwareSet_cfunc = self._library.windll.NISysCfgGetInstalledSoftwareSet
                self._GetInstalledSoftwareSet_cfunc.argtypes = [SessionHandle, Bool, SoftwareSetHandle]  # noqa: F405
                self._GetInstalledSoftwareSet_cfunc.restype = Status  # noqa: F405
        return self._GetInstalledSoftwareSet_cfunc(sessionHandle, cached, setHandle)

    def GetSystemImageAsFolder(self, sessionHandle, destinationFolder, encryptionPassphrase, overwriteIfExists, installedSoftwareOnly, autoRestart):  # noqa: N802,N803
        with self._func_lock:
            if self._GetSystemImageAsFolder_cfunc is None:
                self._GetSystemImageAsFolder_cfunc = self._library.windll.NISysCfgGetSystemImageAsFolder
                self._GetSystemImageAsFolder_cfunc.argtypes = [SessionHandle, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), Bool, Bool, Bool]  # noqa: F405
                self._GetSystemImageAsFolder_cfunc.restype = Status  # noqa: F405
        return self._GetSystemImageAsFolder_cfunc(sessionHandle, destinationFolder, encryptionPassphrase, overwriteIfExists, installedSoftwareOnly, autoRestart)

    def GetSystemImageAsFolder2(self, sessionHandle, autoRestart, destinationFolder, encryptionPassphrase, numBlacklistEntries, blacklistFilesDirectories, overwriteIfExists, installedSoftwareOnly):  # noqa: N802,N803
        with self._func_lock:
            if self._GetSystemImageAsFolder2_cfunc is None:
                self._GetSystemImageAsFolder2_cfunc = self._library.windll.NISysCfgGetSystemImageAsFolder2
                self._GetSystemImageAsFolder2_cfunc.argtypes = [SessionHandle, Bool, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.c_uint, ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), Bool, Bool]  # noqa: F405
                self._GetSystemImageAsFolder2_cfunc.restype = Status  # noqa: F405
        return self._GetSystemImageAsFolder2_cfunc(sessionHandle, autoRestart, destinationFolder, encryptionPassphrase, numBlacklistEntries, blacklistFilesDirectories, overwriteIfExists, installedSoftwareOnly)

    def CreateSystemImageAsFolder(self, sessionHandle, imageTitle, imageID, imageVersion, imageDescription, autoRestart, destinationFolder, encryptionPassphrase, numBlacklistEntries, blacklistFilesDirectories, overwriteIfExists):  # noqa: N802,N803
        with self._func_lock:
            if self._CreateSystemImageAsFolder_cfunc is None:
                self._CreateSystemImageAsFolder_cfunc = self._library.windll.NISysCfgCreateSystemImageAsFolder
                self._CreateSystemImageAsFolder_cfunc.argtypes = [SessionHandle, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), Bool, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.c_uint, ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), Bool]  # noqa: F405
                self._CreateSystemImageAsFolder_cfunc.restype = Status  # noqa: F405
        return self._CreateSystemImageAsFolder_cfunc(sessionHandle, imageTitle, imageID, imageVersion, imageDescription, autoRestart, destinationFolder, encryptionPassphrase, numBlacklistEntries, blacklistFilesDirectories, overwriteIfExists)

    def SetSystemImageFromFolder(self, sessionHandle, sourceFolder, encryptionPassphrase, autoRestart, originalSystemOnly):  # noqa: N802,N803
        with self._func_lock:
            if self._SetSystemImageFromFolder_cfunc is None:
                self._SetSystemImageFromFolder_cfunc = self._library.windll.NISysCfgSetSystemImageFromFolder
                self._SetSystemImageFromFolder_cfunc.argtypes = [SessionHandle, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), Bool, Bool]  # noqa: F405
                self._SetSystemImageFromFolder_cfunc.restype = Status  # noqa: F405
        return self._SetSystemImageFromFolder_cfunc(sessionHandle, sourceFolder, encryptionPassphrase, autoRestart, originalSystemOnly)

    def SetSystemImageFromFolder2(self, sessionHandle, autoRestart, sourceFolder, encryptionPassphrase, numBlacklistEntries, blacklistFilesDirectories, originalSystemOnly, networkSettings):  # noqa: N802,N803
        with self._func_lock:
            if self._SetSystemImageFromFolder2_cfunc is None:
                self._SetSystemImageFromFolder2_cfunc = self._library.windll.NISysCfgSetSystemImageFromFolder2
                self._SetSystemImageFromFolder2_cfunc.argtypes = [SessionHandle, Bool, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.c_uint, ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), Bool, NetworkInterfaceSettings]  # noqa: F405
                self._SetSystemImageFromFolder2_cfunc.restype = Status  # noqa: F405
        return self._SetSystemImageFromFolder2_cfunc(sessionHandle, autoRestart, sourceFolder, encryptionPassphrase, numBlacklistEntries, blacklistFilesDirectories, originalSystemOnly, networkSettings)

    def InstallAll(self, sessionHandle, autoRestart, deselectConflicts, installedComponentEnumHandle, brokenDependencyEnumHandle):  # noqa: N802,N803
        with self._func_lock:
            if self._InstallAll_cfunc is None:
                self._InstallAll_cfunc = self._library.windll.NISysCfgInstallAll
                self._InstallAll_cfunc.argtypes = [SessionHandle, Bool, Bool, EnumSoftwareComponentHandle, EnumDependencyHandle]  # noqa: F405
                self._InstallAll_cfunc.restype = Status  # noqa: F405
        return self._InstallAll_cfunc(sessionHandle, autoRestart, deselectConflicts, installedComponentEnumHandle, brokenDependencyEnumHandle)

    def InstallUninstallComponents(self, sessionHandle, autoRestart, autoSelectDependencies, componentToInstallEnumHandle, numComponentsToUninstall, componentIDsToUninstall, brokenDependencyEnumHandle):  # noqa: N802,N803
        with self._func_lock:
            if self._InstallUninstallComponents_cfunc is None:
                self._InstallUninstallComponents_cfunc = self._library.windll.NISysCfgInstallUninstallComponents
                self._InstallUninstallComponents_cfunc.argtypes = [SessionHandle, Bool, Bool, EnumSoftwareComponentHandle, ctypes.c_uint, ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), EnumDependencyHandle]  # noqa: F405
                self._InstallUninstallComponents_cfunc.restype = Status  # noqa: F405
        return self._InstallUninstallComponents_cfunc(sessionHandle, autoRestart, autoSelectDependencies, componentToInstallEnumHandle, numComponentsToUninstall, componentIDsToUninstall, brokenDependencyEnumHandle)

    def InstallUninstallComponents2(self, sessionHandle, autoRestart, autoSelectDependencies, autoSelectRecommends, componentToInstallEnumHandle, numComponentsToUninstall, componentIDsToUninstall, brokenDependencyEnumHandle):  # noqa: N802,N803
        with self._func_lock:
            if self._InstallUninstallComponents2_cfunc is None:
                self._InstallUninstallComponents2_cfunc = self._library.windll.NISysCfgInstallUninstallComponents2
                self._InstallUninstallComponents2_cfunc.argtypes = [SessionHandle, Bool, Bool, Bool, EnumSoftwareComponentHandle, ctypes.c_uint, ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), EnumDependencyHandle]  # noqa: F405
                self._InstallUninstallComponents2_cfunc.restype = Status  # noqa: F405
        return self._InstallUninstallComponents2_cfunc(sessionHandle, autoRestart, autoSelectDependencies, autoSelectRecommends, componentToInstallEnumHandle, numComponentsToUninstall, componentIDsToUninstall, brokenDependencyEnumHandle)

    def InstallSoftwareSet(self, sessionHandle, autoRestart, softwareSetID, version, addonEnumHandle, brokenDependencyEnumHandle):  # noqa: N802,N803
        with self._func_lock:
            if self._InstallSoftwareSet_cfunc is None:
                self._InstallSoftwareSet_cfunc = self._library.windll.NISysCfgInstallSoftwareSet
                self._InstallSoftwareSet_cfunc.argtypes = [SessionHandle, Bool, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), EnumSoftwareComponentHandle, EnumDependencyHandle]  # noqa: F405
                self._InstallSoftwareSet_cfunc.restype = Status  # noqa: F405
        return self._InstallSoftwareSet_cfunc(sessionHandle, autoRestart, softwareSetID, version, addonEnumHandle, brokenDependencyEnumHandle)

    def InstallStartup(self, sessionHandle, autoRestart, startupEnumHandle, uninstallConflicts, installedComponentEnumHandle, uninstalledComponentEnumHandle, brokenDependencyEnumHandle):  # noqa: N802,N803
        with self._func_lock:
            if self._InstallStartup_cfunc is None:
                self._InstallStartup_cfunc = self._library.windll.NISysCfgInstallStartup
                self._InstallStartup_cfunc.argtypes = [SessionHandle, Bool, EnumSoftwareComponentHandle, Bool, EnumSoftwareComponentHandle, EnumSoftwareComponentHandle, EnumDependencyHandle]  # noqa: F405
                self._InstallStartup_cfunc.restype = Status  # noqa: F405
        return self._InstallStartup_cfunc(sessionHandle, autoRestart, startupEnumHandle, uninstallConflicts, installedComponentEnumHandle, uninstalledComponentEnumHandle, brokenDependencyEnumHandle)

    def UninstallAll(self, sessionHandle, autoRestart):  # noqa: N802,N803
        with self._func_lock:
            if self._UninstallAll_cfunc is None:
                self._UninstallAll_cfunc = self._library.windll.NISysCfgUninstallAll
                self._UninstallAll_cfunc.argtypes = [SessionHandle, Bool]  # noqa: F405
                self._UninstallAll_cfunc.restype = Status  # noqa: F405
        return self._UninstallAll_cfunc(sessionHandle, autoRestart)

    def GetSoftwareFeeds(self, sessionHandle, feedEnumHandle):  # noqa: N802,N803
        with self._func_lock:
            if self._GetSoftwareFeeds_cfunc is None:
                self._GetSoftwareFeeds_cfunc = self._library.windll.NISysCfgGetSoftwareFeeds
                self._GetSoftwareFeeds_cfunc.argtypes = [SessionHandle, EnumSoftwareFeedHandle]  # noqa: F405
                self._GetSoftwareFeeds_cfunc.restype = Status  # noqa: F405
        return self._GetSoftwareFeeds_cfunc(sessionHandle, feedEnumHandle)

    def AddSoftwareFeed(self, sessionHandle, feedName, uri, enabled, trusted):  # noqa: N802,N803
        with self._func_lock:
            if self._AddSoftwareFeed_cfunc is None:
                self._AddSoftwareFeed_cfunc = self._library.windll.NISysCfgAddSoftwareFeed
                self._AddSoftwareFeed_cfunc.argtypes = [SessionHandle, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), Bool, Bool]  # noqa: F405
                self._AddSoftwareFeed_cfunc.restype = Status  # noqa: F405
        return self._AddSoftwareFeed_cfunc(sessionHandle, feedName, uri, enabled, trusted)

    def ModifySoftwareFeed(self, sessionHandle, feedName, newFeedName, uri, enabled, trusted):  # noqa: N802,N803
        with self._func_lock:
            if self._ModifySoftwareFeed_cfunc is None:
                self._ModifySoftwareFeed_cfunc = self._library.windll.NISysCfgModifySoftwareFeed
                self._ModifySoftwareFeed_cfunc.argtypes = [SessionHandle, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), Bool, Bool]  # noqa: F405
                self._ModifySoftwareFeed_cfunc.restype = Status  # noqa: F405
        return self._ModifySoftwareFeed_cfunc(sessionHandle, feedName, newFeedName, uri, enabled, trusted)

    def RemoveSoftwareFeed(self, sessionHandle, feedName):  # noqa: N802,N803
        with self._func_lock:
            if self._RemoveSoftwareFeed_cfunc is None:
                self._RemoveSoftwareFeed_cfunc = self._library.windll.NISysCfgRemoveSoftwareFeed
                self._RemoveSoftwareFeed_cfunc.argtypes = [SessionHandle, ctypes.POINTER(ctypes.c_char)]  # noqa: F405
                self._RemoveSoftwareFeed_cfunc.restype = Status  # noqa: F405
        return self._RemoveSoftwareFeed_cfunc(sessionHandle, feedName)

    def ChangeAdministratorPassword(self, sessionHandle, newPassword):  # noqa: N802,N803
        with self._func_lock:
            if self._ChangeAdministratorPassword_cfunc is None:
                self._ChangeAdministratorPassword_cfunc = self._library.windll.NISysCfgChangeAdministratorPassword
                self._ChangeAdministratorPassword_cfunc.argtypes = [SessionHandle, ctypes.POINTER(ctypes.c_char)]  # noqa: F405
                self._ChangeAdministratorPassword_cfunc.restype = Status  # noqa: F405
        return self._ChangeAdministratorPassword_cfunc(sessionHandle, newPassword)

    def ExportConfiguration(self, sessionHandle, destinationFile, expertNames, overwriteIfExists):  # noqa: N802,N803
        with self._func_lock:
            if self._ExportConfiguration_cfunc is None:
                self._ExportConfiguration_cfunc = self._library.windll.NISysCfgExportConfiguration
                self._ExportConfiguration_cfunc.argtypes = [SessionHandle, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), Bool]  # noqa: F405
                self._ExportConfiguration_cfunc.restype = Status  # noqa: F405
        return self._ExportConfiguration_cfunc(sessionHandle, destinationFile, expertNames, overwriteIfExists)

    def ImportConfiguration(self, sessionHandle, sourceFile, expertNames, importMode, detailedResult):  # noqa: N802,N803
        with self._func_lock:
            if self._ImportConfiguration_cfunc is None:
                self._ImportConfiguration_cfunc = self._library.windll.NISysCfgImportConfiguration
                self._ImportConfiguration_cfunc.argtypes = [SessionHandle, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ImportMode, ctypes.POINTER(ctypes.POINTER(ctypes.c_char))]  # noqa: F405
                self._ImportConfiguration_cfunc.restype = Status  # noqa: F405
        return self._ImportConfiguration_cfunc(sessionHandle, sourceFile, expertNames, importMode, detailedResult)

    def GenerateMAXReport(self, sessionHandle, outputFilename, reportType, overwriteIfExists):  # noqa: N802,N803
        with self._func_lock:
            if self._GenerateMAXReport_cfunc is None:
                self._GenerateMAXReport_cfunc = self._library.windll.NISysCfgGenerateMAXReport
                self._GenerateMAXReport_cfunc.argtypes = [SessionHandle, ctypes.POINTER(ctypes.c_char), ReportType, Bool]  # noqa: F405
                self._GenerateMAXReport_cfunc.restype = Status  # noqa: F405
        return self._GenerateMAXReport_cfunc(sessionHandle, outputFilename, reportType, overwriteIfExists)

    def CreateComponentsEnum(self, componentEnumHandle):  # noqa: N802,N803
        with self._func_lock:
            if self._CreateComponentsEnum_cfunc is None:
                self._CreateComponentsEnum_cfunc = self._library.windll.NISysCfgCreateComponentsEnum
                self._CreateComponentsEnum_cfunc.argtypes = [EnumSoftwareComponentHandle]  # noqa: F405
                self._CreateComponentsEnum_cfunc.restype = Status  # noqa: F405
        return self._CreateComponentsEnum_cfunc(componentEnumHandle)

    def AddComponentToEnum(self, componentEnumHandle, ID, version, mode):  # noqa: N802,N803
        with self._func_lock:
            if self._AddComponentToEnum_cfunc is None:
                self._AddComponentToEnum_cfunc = self._library.windll.NISysCfgAddComponentToEnum
                self._AddComponentToEnum_cfunc.argtypes = [EnumSoftwareComponentHandle, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), VersionSelectionMode]  # noqa: F405
                self._AddComponentToEnum_cfunc.restype = Status  # noqa: F405
        return self._AddComponentToEnum_cfunc(componentEnumHandle, ID, version, mode)

    def FreeDetailedString(self, str):  # noqa: N802,N803
        with self._func_lock:
            if self._FreeDetailedString_cfunc is None:
                self._FreeDetailedString_cfunc = self._library.windll.NISysCfgFreeDetailedString
                self._FreeDetailedString_cfunc.argtypes = [ctypes.POINTER(ctypes.c_char)]  # noqa: F405
                self._FreeDetailedString_cfunc.restype = Status  # noqa: F405
        return self._FreeDetailedString_cfunc(str)

    def NextResource(self, sessionHandle, resourceEnumHandle, resourceHandle):  # noqa: N802,N803
        with self._func_lock:
            if self._NextResource_cfunc is None:
                self._NextResource_cfunc = self._library.windll.NISysCfgNextResource
                self._NextResource_cfunc.argtypes = [SessionHandle, EnumResourceHandle, ResourceHandle]  # noqa: F405
                self._NextResource_cfunc.restype = Status  # noqa: F405
        return self._NextResource_cfunc(sessionHandle, resourceEnumHandle, resourceHandle)

    def NextSystemInfo(self, systemEnumHandle, system):  # noqa: N802,N803
        with self._func_lock:
            if self._NextSystemInfo_cfunc is None:
                self._NextSystemInfo_cfunc = self._library.windll.NISysCfgNextSystemInfo
                self._NextSystemInfo_cfunc.argtypes = [EnumSystemHandle, ctypes.POINTER(ctypes.c_char)]  # noqa: F405
                self._NextSystemInfo_cfunc.restype = Status  # noqa: F405
        return self._NextSystemInfo_cfunc(systemEnumHandle, system)

    def NextExpertInfo(self, expertEnumHandle, expertName, displayName, version):  # noqa: N802,N803
        with self._func_lock:
            if self._NextExpertInfo_cfunc is None:
                self._NextExpertInfo_cfunc = self._library.windll.NISysCfgNextExpertInfo
                self._NextExpertInfo_cfunc.argtypes = [EnumExpertHandle, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char)]  # noqa: F405
                self._NextExpertInfo_cfunc.restype = Status  # noqa: F405
        return self._NextExpertInfo_cfunc(expertEnumHandle, expertName, displayName, version)

    def NextComponentInfo(self, componentEnumHandle, ID, version, title, itemType, detailedDescription):  # noqa: N802,N803
        with self._func_lock:
            if self._NextComponentInfo_cfunc is None:
                self._NextComponentInfo_cfunc = self._library.windll.NISysCfgNextComponentInfo
                self._NextComponentInfo_cfunc.argtypes = [EnumSoftwareComponentHandle, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.POINTER(ctypes.c_char))]  # noqa: F405
                self._NextComponentInfo_cfunc.restype = Status  # noqa: F405
        return self._NextComponentInfo_cfunc(componentEnumHandle, ID, version, title, itemType, detailedDescription)

    def NextSoftwareSet(self, setEnumHandle, setHandle):  # noqa: N802,N803
        with self._func_lock:
            if self._NextSoftwareSet_cfunc is None:
                self._NextSoftwareSet_cfunc = self._library.windll.NISysCfgNextSoftwareSet
                self._NextSoftwareSet_cfunc.argtypes = [EnumSoftwareSetHandle, SoftwareSetHandle]  # noqa: F405
                self._NextSoftwareSet_cfunc.restype = Status  # noqa: F405
        return self._NextSoftwareSet_cfunc(setEnumHandle, setHandle)

    def GetSoftwareSetInfo(self, setHandle, itemTypes, includeAddOnDeps, ID, version, title, setType, detailedDescription, addOnEnumHandle, itemEnumHandle):  # noqa: N802,N803
        with self._func_lock:
            if self._GetSoftwareSetInfo_cfunc is None:
                self._GetSoftwareSetInfo_cfunc = self._library.windll.NISysCfgGetSoftwareSetInfo
                self._GetSoftwareSetInfo_cfunc.argtypes = [SoftwareSetHandle, IncludeComponentTypes, Bool, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), EnumSoftwareComponentHandle, EnumSoftwareComponentHandle]  # noqa: F405
                self._GetSoftwareSetInfo_cfunc.restype = Status  # noqa: F405
        return self._GetSoftwareSetInfo_cfunc(setHandle, itemTypes, includeAddOnDeps, ID, version, title, setType, detailedDescription, addOnEnumHandle, itemEnumHandle)

    def NextDependencyInfo(self, dependencyEnumHandle, dependerID, dependerVersion, dependerTitle, dependerDetailedDescription, dependeeID, dependeeVersion, dependeeTitle, dependeeDetailedDescription):  # noqa: N802,N803
        with self._func_lock:
            if self._NextDependencyInfo_cfunc is None:
                self._NextDependencyInfo_cfunc = self._library.windll.NISysCfgNextDependencyInfo
                self._NextDependencyInfo_cfunc.argtypes = [EnumDependencyHandle, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.POINTER(ctypes.c_char))]  # noqa: F405
                self._NextDependencyInfo_cfunc.restype = Status  # noqa: F405
        return self._NextDependencyInfo_cfunc(dependencyEnumHandle, dependerID, dependerVersion, dependerTitle, dependerDetailedDescription, dependeeID, dependeeVersion, dependeeTitle, dependeeDetailedDescription)

    def NextSoftwareFeed(self, feedEnumHandle, feedName, uri, enabled, trusted):  # noqa: N802,N803
        with self._func_lock:
            if self._NextSoftwareFeed_cfunc is None:
                self._NextSoftwareFeed_cfunc = self._library.windll.NISysCfgNextSoftwareFeed
                self._NextSoftwareFeed_cfunc.argtypes = [EnumSoftwareFeedHandle, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]  # noqa: F405
                self._NextSoftwareFeed_cfunc.restype = Status  # noqa: F405
        return self._NextSoftwareFeed_cfunc(feedEnumHandle, feedName, uri, enabled, trusted)

    def ResetEnumeratorGetCount(self, enumHandle, count):  # noqa: N802,N803
        with self._func_lock:
            if self._ResetEnumeratorGetCount_cfunc is None:
                self._ResetEnumeratorGetCount_cfunc = self._library.windll.NISysCfgResetEnumeratorGetCount
                self._ResetEnumeratorGetCount_cfunc.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint)]  # noqa: F405
                self._ResetEnumeratorGetCount_cfunc.restype = Status  # noqa: F405
        return self._ResetEnumeratorGetCount_cfunc(enumHandle, count)

    def GetStatusDescription(self, sessionHandle, status, detailedDescription):  # noqa: N802,N803
        with self._func_lock:
            if self._GetStatusDescription_cfunc is None:
                self._GetStatusDescription_cfunc = self._library.windll.NISysCfgGetStatusDescription
                self._GetStatusDescription_cfunc.argtypes = [SessionHandle, Status, ctypes.POINTER(ctypes.POINTER(ctypes.c_char))]  # noqa: F405
                self._GetStatusDescription_cfunc.restype = Status  # noqa: F405
        return self._GetStatusDescription_cfunc(sessionHandle, status, detailedDescription)

    def TimestampFromValues(self, secondsSinceEpoch1970, fractionalSeconds, timestamp):  # noqa: N802,N803
        with self._func_lock:
            if self._TimestampFromValues_cfunc is None:
                self._TimestampFromValues_cfunc = self._library.windll.NISysCfgTimestampFromValues
                self._TimestampFromValues_cfunc.argtypes = [UInt64, ctypes.c_double, ctypes.POINTER(TimestampUTC)]  # noqa: F405
                self._TimestampFromValues_cfunc.restype = Status  # noqa: F405
        return self._TimestampFromValues_cfunc(secondsSinceEpoch1970, fractionalSeconds, timestamp)

    def ValuesFromTimestamp(self, timestamp, secondsSinceEpoch1970, fractionalSeconds):  # noqa: N802,N803
        with self._func_lock:
            if self._ValuesFromTimestamp_cfunc is None:
                self._ValuesFromTimestamp_cfunc = self._library.windll.NISysCfgValuesFromTimestamp
                self._ValuesFromTimestamp_cfunc.argtypes = [TimestampUTC, ctypes.POINTER(UInt64), ctypes.POINTER(ctypes.c_double)]  # noqa: F405
                self._ValuesFromTimestamp_cfunc.restype = Status  # noqa: F405
        return self._ValuesFromTimestamp_cfunc(timestamp, secondsSinceEpoch1970, fractionalSeconds)
