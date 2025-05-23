import ctypes
import platform
import sys
import threading
from typing import Optional, Union

from nisyscfg import _library, errors

if sys.platform.startswith("linux"):
    from ctypes import CDLL, RTLD_GLOBAL

    class WinDLL(CDLL):
        """Dummy class to satisfy mypy on Linux."""

        ...

else:
    from ctypes import CDLL, RTLD_GLOBAL, WinDLL


class _CTypesLibrary(object):
    def __init__(self, cdll: CDLL, windll: Optional[WinDLL] = None):
        self._cdll = cdll
        self._windll = windll or cdll

    @property
    def cdll(self) -> CDLL:
        return self._cdll

    @property
    def windll(self) -> Union[WinDLL, CDLL]:
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


def _get_library_name() -> str:
    try:
        return _library_info[platform.system()][platform.architecture()[0]]["name"]
    except KeyError:
        raise errors.UnsupportedPlatformError


def _get_library_type() -> str:
    try:
        return _library_info[platform.system()][platform.architecture()[0]]["type"]
    except KeyError:
        raise errors.UnsupportedPlatformError


def get() -> _library.Library:
    """Get the singleton instance of the library."""
    global _instance
    global _instance_lock

    with _instance_lock:
        if _instance is None:
            try:
                library_type = _get_library_type()
                if library_type == "dual":
                    ctypes_library = _CTypesLibrary(
                        CDLL(_get_library_name(), RTLD_GLOBAL),
                        WinDLL(_get_library_name()),
                    )
                else:
                    assert library_type == "cdll"
                    # ctypes.CDLL to make it easier to unit test both current and legacy APIs
                    ctypes_library = _CTypesLibrary(ctypes.CDLL(_get_library_name(), RTLD_GLOBAL))
            except OSError:
                raise errors.LibraryNotInstalledError()
            _instance = _library.Library(ctypes_library)
    return _instance
