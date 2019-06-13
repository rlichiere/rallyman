# -*- coding: utf-8 -*-
from .utils import version as _version


version = _version.Version(
    MAJOR=0,
    MINOR=0,
    BUILD=1,
    STATUS=_version.VersionStatus.ALPHA,
    REVISION=1,
    COMMENT='',
)
