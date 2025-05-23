"""This module provides a Python interface to the NI System Configuration API.

It includes classes and functions for managing system configuration, resources, and sessions.
The API allows users to interact with hardware and software components, retrieve information,
and perform operations such as importing and exporting configurations, managing resources, and
handling errors.

The API is designed to be used with National Instruments hardware and software, and it provides
a high-level interface for developers to work with system configuration tasks in a Pythonic way.
"""

from nisyscfg import enums, errors, types
from nisyscfg.system import Session

__all__ = [
    "Session",
    "enums",
    "errors",
    "types",
]
