from hightime import datetime
from hightime import timedelta
import nisyscfg
import nisyscfg._library_singleton
import nisyscfg.errors
import nisyscfg.types

import ctypes


# International Atomic Time epoch
tai_epoch = datetime(year=1970, month=1, day=1)


def _convert_ctype_to_datatime(timestamp: nisyscfg.types.TimestampUTC) -> datetime:
    library = nisyscfg._library_singleton.get()
    seconds_since_tai_epoch = ctypes.c_uint64()
    fractional_seconds = ctypes.c_double()

    error_code = library.ValuesFromTimestamp(
        timestamp,
        ctypes.pointer(seconds_since_tai_epoch),
        ctypes.pointer(fractional_seconds),
    )
    nisyscfg.errors.handle_error(None, error_code, is_error_handling=True)

    return (
        tai_epoch
        + timedelta(seconds=seconds_since_tai_epoch.value)
        + timedelta(seconds=fractional_seconds.value)
    )


def _convert_datatime_to_ctype(timestamp: datetime) -> nisyscfg.types.TimestampUTC:
    library = nisyscfg._library_singleton.get()

    time_since_tai_epoch = timestamp - tai_epoch
    seconds_since_tai_epoch = time_since_tai_epoch.days * 86400 + time_since_tai_epoch.seconds
    fractional_seconds = (
        (time_since_tai_epoch.microseconds / 10 ** 6)
        + (time_since_tai_epoch.femtoseconds / 10 ** 15)
        + (time_since_tai_epoch.yoctoseconds / 10 ** 24)
    )
    timestamp = nisyscfg.types.TimestampUTC()

    error_code = library.TimestampFromValues(
        seconds_since_tai_epoch,
        fractional_seconds,
        ctypes.pointer(timestamp),
    )
    nisyscfg.errors.handle_error(None, error_code, is_error_handling=True)

    return timestamp
