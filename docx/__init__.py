"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

__title__ = 'docx'
__author__ = 'lmaotrigine'
__license__ = 'MPL-2.0'
__copyright__ = 'Copyright 2023-present lmaotrigine'
__version__ = '0.1.0a'

__path__ = __import__('pkgutil').extend_path(__path__, __name__)


from typing import Literal, NamedTuple

from .document import *


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal['alpha', 'beta', 'candidate', 'final']
    serial: int


version_info: VersionInfo = VersionInfo(major=0, minor=1, micro=0, releaselevel='alpha', serial=0)

del NamedTuple, Literal, VersionInfo
