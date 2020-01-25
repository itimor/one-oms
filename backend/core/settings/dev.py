# -*- coding: utf-8 -*-
# author: timor

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# db
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../core.db'),
    }
}