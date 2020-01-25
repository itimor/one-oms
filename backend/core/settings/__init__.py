# -*- coding: utf-8 -*-
# author: timor

from .base import *
import platform

os = platform.system()

if os == 'Windows':
    print("dev env..")
    from .dev import *
else:
    print("prod env..")
    from .prod import *
