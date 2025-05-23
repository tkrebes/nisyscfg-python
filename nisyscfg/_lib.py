import locale
import sys
from typing import Any

if sys.platform.startswith("win"):
    # On Windows, nisyscfg uses the system code page for the decoding of C-strings
    def get_syscfg_locale() -> str:
        """Get the system locale for NI System Configuration uses to decode C-strings."""
        return locale.getlocale()[1] or locale.getdefaultlocale()[1] or "ascii"

else:
    # On other OSes, nisyscfg uses ISO-8859-1 (Latin1) for the decoding of C-strings
    def get_syscfg_locale() -> str:
        """Get the system locale for NI System Configuration uses to decode C-strings."""
        return "ISO-8859-1"


def c_string_encode(value: Any) -> Any:
    """Encode a string to bytes with the locale used by NI System Configuration."""
    if isinstance(value, str):
        return value.encode(get_syscfg_locale())
    return value


def c_string_decode(value: Any) -> Any:
    """Decode bytes to string with the locale used by NI System Configuration."""
    if isinstance(value, bytes):
        return value.decode(get_syscfg_locale())
    return value


# Legacy functions
def ascii_encode(value: Any) -> Any:
    """Encode a string to bytes with the ascii locale."""
    if isinstance(value, str):
        return value.encode("ascii")
    return value


def ascii_decode(value: Any) -> Any:
    """Decode bytes to string with the ascii locale."""
    if isinstance(value, bytes):
        try:
            value_return = value.decode("ascii")
        except UnicodeDecodeError:
            value_return = value.decode("ascii", errors="backslashreplace")
        return value_return
    return value
