#!/usr/bin/python
# -*- coding: UTF-8 -*-


import requests
import re
import os

index = 'http://18h.mm-cg.com'
y = 70
c = 74  # 7001~7100, 6901~7000,6801~6900
for m in range(c, 100):
    p = 100 * y + m
    url = index + '/18H_%s.html' % p

    html = requests.get(url)

    a = html.content

    b = str(a, encoding="utf-8")

    c = re.findall(r'Large_cgurl\[\d+\] = "(.*)";', b)

    save_dir = '/data/avmh'

    for n in c:
        print(n)
        lst = n.split('/')
        tmp = '{}_{}'.format(p, lst[-2:-1][0])
        mh_dir = os.path.join(save_dir, tmp)

        if not os.path.exists(mh_dir):
            os.makedirs(mh_dir)

        findall_name = os.path.join(mh_dir, lst[-1])
        if not os.path.isfile(findall_name):
            h = requests.get(n)
            with open(findall_name, 'wb') as fn:
                fn.write(h.content)
