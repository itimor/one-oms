#!/usr/bin/env python
# coding: utf8

import json
import requests

class OpenFalcon(object):
    def __init__(self, url, user, passwd):
        self.url = url
        self.user = user
        self.passwd = passwd
        self.falcon_header = self.getFalconHeader()

    # 获取open-falcon session，返回falcon headeres
    def getFalconHeader(self):
        api_url = self.url + '/user/login'
        res = s.post(url=api_url, data={'name': user, 'password': passwd})
        sig = json.loads(res.text)
        sig = sig['sig']
        api_token = '{"name":"' + user + '", "sig":"' + sig + '"}'
        falcon_header = {
            "Apitoken": api_token,
            "X-Forwarded-For": "127.0.0.1",
            "Content-Type": "application/json",
            "name": user,
            "sig": sig
        }
        return falcon_header

    def getAggId(self):
        api_url = '{}/hostgroup/1/aggregators'.format(self.url)
        params = {
            'url': api_url,
            'headers': self.falcon_header,
            'timeout': 30
        }
        resp = s.get(**params)
        _resp = [data['numerator'] for data in json.loads(resp.text)['aggregators']]
        return _resp

    # 批量删除 aggregators
    def bulk_delete(self, id):
        api_url = '{}/aggregator/{}'.format(self.url, id)
        params = {
            'url': api_url,
            'headers': self.falcon_header,
            'timeout': 30
        }
        req = s.delete(**params)
        return req.json()

if __name__ == '__main__':
    # open-falcon配置
    user = 'root'
    passwd = 'v5benzro-gf*TY1k'
    url = 'http://127.0.0.1:8080/api/v1'
    s = requests.Session()
    conn = OpenFalcon(url, user, passwd)

    for id in range(1,2):
        print(conn.bulk_delete(id))
