# -*- coding: utf-8 -*-
# author: timor

import time
def gen_pid():
    pid = str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))+ str(time.time()).replace('.', '')[-7:]
    return pid

