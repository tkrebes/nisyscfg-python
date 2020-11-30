from __future__ import absolute_import

import locale
import six
import sys


if sys.platform.startswith("win"):
    # On Windows, nisyscfg uses the system code page for the decoding of C-strings
    def get_syscfg_locale():
        return locale.getlocale()[1] or locale.getdefaultlocale()[1] or "ascii"


else:
    # On other OSes, nisyscfg uses ISO-8859-1 (Latin1) for the decoding of C-strings
    def get_syscfg_locale():
        return "ISO-8859-1"


def c_string_encode(value):
    if isinstance(value, six.text_type):
        return value.encode(get_syscfg_locale())
    return value


def c_string_decode(value):
    if isinstance(value, six.binary_type):
        return value.decode(get_syscfg_locale())
    return value
