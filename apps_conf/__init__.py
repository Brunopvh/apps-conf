#!/usr/bin/env python3

from .__main__ import (
    HOME,
    KERNEL_TYPE,
    FilePath,
    FileReader,
    FileJson,
    mkdir,
    touch,
    ConfDirs,
    AppDirs,
    get_abspath,
    __version__,
    __repo__,
)


if KERNEL_TYPE == 'Linux':
    from .__main__ import (add_home_in_path)
