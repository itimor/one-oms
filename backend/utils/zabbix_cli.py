# -*- coding: utf-8 -*-
# author: timor


import click
from zabbix_api import ZabbixApi

zabbix_url = 'http://172.16.27.250/zabbix'
zabbix_info = {
    'apiurl': zabbix_url + '/api_jsonrpc.php',
    'username': 'Admin',
    'password': 'zabbix'
}


@click.group()
def cli():
    click.secho('开始使用zabbix api!', fg='yellow', underline=True)


@cli.command()
def gethosts():
    """获取zabbix主机"""
    req = zapi.get_hosts()
    for host in req:
        click.secho('主机名：{}，IP：{}'.format(host["host"], host["interfaces"][0]["ip"]), fg='green')


@cli.command()
@click.option('-h', '--hostname', default='test001', help='主机名，like test001')
@click.option('-g', '--groupnames', default='Linux servers', help='主机组名称，用 | 分隔， like aaa|bbb|ccc')
@click.option('-t', '--templatenames', default='Template OS Linux', help='模板名称，用 | 分隔， like aaa|bbb|ccc')
@click.option('-ip', '--ip', default='0.0.0.0', help='主机ip， like 1.1.1.1')
def addhost(hostname, groupnames, templatenames, ip):
    """添加zabbix主机"""
    hostgroups = []
    templates = []
    for hostgroupName in groupnames.split('|'):
        res = zapi.get_hostgroups(hostgroupName)[0]
        hostgroups.append(res['groupid'])
    for templateName in templatenames.split('|'):
        res = zapi.get_templetes(templateName)[0]
        templates.append(res['templateid'])

    req = zapi.create_host(hostname, hostgroups, templates, ip)
    if 'code' not in req.keys():
        click.secho("%s 添加成功！" % hostname, fg='green')
    else:
        click.secho("%s 添加失败！" % hostname, fg='red')
        click.secho('status: {}, message: {}'.format(req['code'], req['message']), fg='red')


if __name__ == '__main__':
    zapi = ZabbixApi(zabbix_info["apiurl"], zabbix_info["username"], zabbix_info["password"])
    zapi.login()
    cli()
