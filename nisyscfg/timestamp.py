"""Timestamp conversion utilities."""

import ctypes

from hightime import datetime, timedelta

import nisyscfg
import nisyscfg._library_singleton
import nisyscfg.errors
import nisyscfg.types

# International Atomic Time epoch
# TAI epoch is 1970-01-01


tai_epoch = datetime(year=1970, month=1, day=1)


def is_blank_timestamp(timestamp: nisyscfg.types.TimestampUTC) -> bool:
    """Check if a timestamp is blank (all fields are zero).

    Args:
        timestamp (nisyscfg.types.TimestampUTC): The timestamp to check.

    Returns:
        bool: True if all fields in the timestamp are zero, False otherwise.
    """
    return all(num == 0 for num in timestamp)


def _convert_ctype_to_datetime(timestamp: nisyscfg.types.TimestampUTC) -> datetime:
    """Convert a nisyscfg.types.TimestampUTC to a Python datetime object.

    If the timestamp is blank (all zeros), returns 1 Jan 1904.
    Otherwise, converts the timestamp to a datetime object.

    Args:
        timestamp (nisyscfg.types.TimestampUTC): The timestamp to convert.

    Returns:
        datetime: The corresponding Python datetime object.
    """
    if is_blank_timestamp(timestamp):
        return datetime(year=1904, month=1, day=1)
    else:
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


def _convert_datetime_to_ctype(timestamp: datetime) -> nisyscfg.types.TimestampUTC:
    """Convert a Python datetime object to nisyscfg.types.TimestampUTC.

    If the datetime is 1 Jan 1904, returns a blank timestamp (all zeros).
    Otherwise, converts the datetime to a TimestampUTC.

    Args:
        timestamp (datetime): The datetime to convert.

    Returns:
        nisyscfg.types.TimestampUTC: The corresponding timestamp.
    """
    if timestamp == datetime(year=1904, month=1, day=1):
        return nisyscfg.types.TimestampUTC(0, 0, 0, 0)
    else:
        library = nisyscfg._library_singleton.get()

        time_since_tai_epoch = timestamp - tai_epoch
        seconds_since_tai_epoch = time_since_tai_epoch.days * 86400 + time_since_tai_epoch.seconds
        fractional_seconds = (
            (time_since_tai_epoch.microseconds / 10**6)
            + (time_since_tai_epoch.femtoseconds / 10**15)
            + (time_since_tai_epoch.yoctoseconds / 10**24)
        )
        timestamp = nisyscfg.types.TimestampUTC()

        error_code = library.TimestampFromValues(
            seconds_since_tai_epoch,
            fractional_seconds,
            ctypes.pointer(timestamp),
        )
        nisyscfg.errors.handle_error(None, error_code, is_error_handling=True)

        return timestamp
