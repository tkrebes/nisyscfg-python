import ctypes
import nisyscfg.errors
import nisyscfg.properties
import nisyscfg.xnet.properties

from nisyscfg._lib import c_string_encode


@nisyscfg.properties.PropertyBag(nisyscfg.properties.Filter)
@nisyscfg.properties.PropertyBag(nisyscfg.xnet.properties.Filter, expert="xnet")
class Filter(object):
    def __init__(self, session):
        self._handle = nisyscfg.types.FilterHandle()
        self._library = nisyscfg._library_singleton.get()
        self._property_accessor = nisyscfg.properties.PropertyAccessor(
            setter=self._set_property_with_type
        )
        error_code = self._library.CreateFilter(session, ctypes.pointer(self._handle))
        nisyscfg.errors.handle_error(self, error_code)

    def __del__(self):
        self.close()

    def close(self):
        if self._handle:
            error_code = self._library.CloseHandle(self._handle)
            nisyscfg.errors.handle_error(self, error_code)
            self._handle = None

    def _set_property_with_type(self, id, value, c_type, nisyscfg_type):
        if c_type == ctypes.c_char_p:
            value = c_string_encode(value)
        elif issubclass(c_type, nisyscfg.enums.BaseEnum):
            value = ctypes.c_int(value)
        else:
            value = c_type(value)

        error_code = self._library.SetFilterPropertyWithType(self._handle, id, nisyscfg_type, value)
        nisyscfg.errors.handle_error(self, error_code)
