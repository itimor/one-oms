# -*- coding: utf-8 -*-
# author: itimor

import platform
from .base import *

if platform.system() == 'Windows':
    print('进入 dev ')
    from .dev import *
else:
    if platform.node() == "xxoo":
        print('进入 test ')
        from .test import *
    else:
        print('进入 prod ')
        from .prod import *
