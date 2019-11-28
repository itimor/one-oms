# -*- coding: utf-8 -*-
# author: itimor
# docs: https://www.zabbix.com/documentation/3.4/zh/manual/api

import requests
import json


class ZabbixApi(object):
    def __init__(self, apiurl, username, password, auth_token=None):
        self.apiurl = apiurl
        self.username = username
        self.password = password
        self.header = {"Content-Type": "application/json"}
        self.auth_token = auth_token
        self.request_id = 54088  # 意义非凡

    def request(self, method, params):
        """
        Send request to Zabbix API
        :param method: Zabbix API 请求方法
        :param params: Zabbix API 请求参数
        :param auth_token: Zabbix API token
        :return: json
        """
        data = json.dumps({"jsonrpc": "2.0",
                           "method": method,
                           "params": params,
                           "auth": self.auth_token,
                           "id": self.request_id})
        req = requests.post(self.apiurl, data=data, headers=self.header).content
        try:
            return json.loads(req)["result"]
        except:
            return json.loads(req)["error"]

    def login(self):
        method = "user.login"
        params = {
            "user": self.username,
            "password": self.password
        }
        req = self.request(method, params)
        self.auth_token = req

    def get_hosts(self, groupid=None, hostName=None, hostIp=None, search=None):
        method = "host.get"
        params = {
            "output": "extend",
            "selectGroups": "extend",
            "selectParentTemplates": "extend",
            "selectInterfaces": "extend",
            "groupids": groupid,
            "filter": {
                "host": hostName,
                "ip": hostIp
            }
        }
        if search:
            params.update({"search": {
                "host": [search],
            }})
        req = self.request(method, params)
        return req

    def create_host(self, hostName, hostgroups=[], templates=[], hostIp='0.0.0.0'):
        if self.get_hosts(hostName=hostName):
            return {"code": "10001", "message": "The host was added!"}

        group_list = [{"groupid": hostgroup_id} for hostgroup_id in hostgroups]
        template_list = [{"templateid": templete_id} for templete_id in templates]

        method = "host.create"
        params = {
            "host": hostName,
            "interfaces": [
                {
                    "type": 1,
                    "main": 1,
                    "useip": 1,
                    "ip": hostIp,
                    "dns": "",
                    "port": "10050"
                }
            ],
            "groups": group_list,
            "templates": template_list,
        }
        req = self.request(method, params)
        return req

    def update_host(self, hostId, hostName=None, hostgroups=None, templates_clear=[], hostIp='0.0.0.0'):
        """
        zabbix api更新主机模板时，主机名对模板中的一些item有依赖，无法正常更新主机，这个update用起来很不方便
        """
        group_list = [{"groupid": hostgroup_id} for hostgroup_id in hostgroups]
        # templates_clear_list = [{"templateid": templete_id} for templete_id in templates_clear]
        # template_list = [{"templateid": templete_id} for templete_id in templates]

        method = "host.update"
        params = {
            "hostid": hostId,
            "host": hostName,
            "interfaces": [
                {
                    "type": 1,
                    "main": 1,
                    "useip": 1,
                    "ip": hostIp,
                    "dns": "",
                    "port": "10050"
                }
            ],
            "groups": group_list,
            # "templates_clear": templates_clear_list,
            # "templates": template_list,
        }
        req = self.request(method, params)
        return req

    def delete_host(self, hostIds=[]):
        method = "host.delete"
        params = hostIds
        req = self.request(method, params)
        return req

    def get_hostgroups(self, hostgroupName=None):
        method = "hostgroup.get"
        params = {
            "output": "extend",
            "selectHosts": "extend",
            "filter": {
                "name": hostgroupName
            }
        }
        req = self.request(method, params)
        return req

    def create_hostgroup(self, hostgroupName):
        if self.get_hostgroups([hostgroupName]):
            return {"code": "10002", "message": "The hostgroup was added!"}

        method = "hostgroup.create"
        params = {"name": hostgroupName}
        req = self.request(method, params)
        return req

    def get_templetes(self, templateName=None):
        method = "template.get"
        params = {
            "output": "extend",
            "filter": {
                "name": templateName
            }
        }
        req = self.request(method, params)
        return req


if __name__ == "__main__":
    zabbix_url = 'http://172.16.27.250/zabbix'
    zabbix_info = {
        'apiurl': zabbix_url + '/api_jsonrpc.php',
        'username': 'Admin',
        'password': 'zabbix'
    }
    zapi = ZabbixApi(zabbix_info["apiurl"], zabbix_info["username"], zabbix_info["password"])
    zapi.login()
    groups = [
        "Zabbix servers",
        "Linux servers"
    ]
    # hosts = zapi.get_hosts()
    hosts = zapi.get_templetes('Template OS Linux')
    # hosts = zapi.get_hostgroups('Linux servers')
    h = {'hostids': ['10232']}
    # hosts = zapi.update_host('10235', hostgroups=[6])
    print(hosts)
