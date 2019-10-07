import ctypes
from nisyscfg.enums import PropertyType


class Property(object):
    def __init__(self, id, c_type, syscfg_type=None, readable=True, writeable=True):
        self._id = id
        self._c_type = c_type
        self._syscfg_type = syscfg_type
        self._readable = readable
        self._writeable = writeable

    @property
    def id(self):
        return self._id

    @property
    def c_type(self):
        return self._c_type

    @property
    def syscfg_type(self):
        return self._syscfg_type

    @property
    def indexed(self):
        return False

    def __get__(self, instance, owner):
        return instance.get_property(self)

    def __set__(self, instance, value):
        return instance.set_property(self, value)


class IndexedProperty(object):
    def __init__(self, id, count_property, c_type, syscfg_type=None, readable=True, writeable=True):
        self._id = id
        self._count_property = count_property
        self._c_type = c_type
        self._syscfg_type = syscfg_type
        self._readable = readable
        self._writeable = writeable

    @property
    def id(self):
        return self._id

    @property
    def c_type(self):
        return self._c_type

    @property
    def syscfg_type(self):
        return self._syscfg_type

    @property
    def indexed(self):
        return True

    @property
    def count_property(self):
        return self._count_property

    def __get__(self, instance, owner):
        return instance.get_property(self)


class PropertyBool(Property):
    def __init__(self, id, c_type=ctypes.c_uint, readable=True, writeable=True):
        super(PropertyBool, self).__init__(id, c_type, PropertyType.Bool, readable, writeable)


class PropertyInt(Property):
    def __init__(self, id, c_type=ctypes.c_int, readable=True, writeable=True):
        super(PropertyInt, self).__init__(id, c_type, PropertyType.Int, readable, writeable)


class PropertyUnsignedInt(Property):
    def __init__(self, id, c_type=ctypes.c_uint, readable=True, writeable=True):
        super(PropertyUnsignedInt, self).__init__(id, c_type, PropertyType.UnsignedInt, readable, writeable)


class PropertyDouble(Property):
    def __init__(self, id, c_type=ctypes.c_double, readable=True, writeable=True):
        super(PropertyDouble, self).__init__(id, c_type, PropertyType.Double, readable, writeable)


class PropertyString(Property):
    def __init__(self, id, c_type=ctypes.c_char_p, readable=True, writeable=True):
        super(PropertyString, self).__init__(id, c_type, PropertyType.String, readable, writeable)


class HardwareResourceAddon(object):
    def __init__(self, resource):
        self._resource = resource

    def get_property(self, property):
        return self._resource._get_property(property)

    def set_property(self, property, value):
        self._resource._set_property(property, value)


class HardwareFilterAddon(object):
    def __init__(self, filter):
        self._filter = filter

    def set_property(self, property, value):
        self._filter._set_property(property, value)
