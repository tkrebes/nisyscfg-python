import ctypes
import platform
import threading

from nisyscfg import _library
from nisyscfg import errors


class CTypesLibrary(object):
    def __init__(self, cdll, windll=None):
        self._cdll = cdll
        self._windll = windll
        if self._windll is None:
            self._windll = self._cdll

    @property
    def cdll(self):
        return self._cdll

    @property
    def windll(self):
        return self._windll


_instance = None
_instance_lock = threading.Lock()
_library_info = {
    "Linux": {"64bit": {"name": "libnisyscfg.so", "type": "cdll"}},
    "Windows": {
        "32bit": {"name": "nisyscfg.dll", "type": "dual"},
        "64bit": {"name": "nisyscfg.dll", "type": "cdll"},
    },
}


def _get_library_name():
    try:
        return _library_info[platform.system()][platform.architecture()[0]]["name"]
    except KeyError:
        raise errors.UnsupportedPlatformError


def _get_library_type():
    try:
        return _library_info[platform.system()][platform.architecture()[0]]["type"]
    except KeyError:
        raise errors.UnsupportedPlatformError


def get():
    global _instance
    global _instance_lock

    with _instance_lock:
        if _instance is None:
            try:
                library_type = _get_library_type()
                if library_type == "dual":
                    ctypes_library = CTypesLibrary(
                        ctypes.CDLL(_get_library_name()),
                        ctypes.WinDLL(_get_library_name()),
                    )
                else:
                    assert library_type == "cdll"
                    ctypes_library = CTypesLibrary(ctypes.CDLL(_get_library_name()))
            except OSError:
                raise errors.LibraryNotInstalledError()
            _instance = _library.Library(ctypes_library)
    return _instance
