# -*- coding: utf-8 -*-
# author: timor

# db
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'NAME': 'mysql',
        'USER': 'root',
        'PASSWORD': 'momo520',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
    }
}