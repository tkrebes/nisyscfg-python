import sys
import threading


class Addons(object):
    def __init__(self):
        self._func_lock = threading.Lock()
        self._addons = None

    def __getattr__(self, name):
        with self._func_lock:
            if self._addons is None:
                import pkg_resources

                self._addons = {}
                for entry_point in pkg_resources.iter_entry_points('nisyscfg_addons'):
                    self._addons[entry_point.name] = entry_point.load()
        if name in self._addons:
            return self._addons[name]
        raise AttributeError(name)


sys.modules[__name__] = Addons()
