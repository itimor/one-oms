# -*- coding: utf-8 -*-
# author: itimor

import asyncio
import websockets
import json
import sys
import subprocess


async def send_msg(ws):
    obj = {"cmd": 'ping www.google.com'}
    await ws.send(json.dumps(obj))
    recv_text = await ws.recv()
    print(f"{recv_text}")


async def send_result(ws):
    event = {"cmd": 'ping www.google.com'}
    cmd = subprocess.Popen(event['cmd'], stdin=subprocess.PIPE, stderr=subprocess.PIPE,
                           stdout=subprocess.PIPE, universal_newlines=True, shell=True, bufsize=1)
    # 实时输出
    while True:
        line = cmd.stdout.readline()
        if line == '' and subprocess.Popen.poll(cmd) == 0:  # 判断子进程是否结束
            break
        # sys.stdout.write(line)
        sys.stdout.flush()
        if line != '':
            print(line.strip())
            obj = {"cmd": line.strip()}
            await ws.send(json.dumps(obj))
            recv_text = await ws.recv()
            print(f"{recv_text}")


# 客户端主逻辑
async def main():
    async with websockets.connect('ws://127.0.0.1:8000/ws/shell/aaa') as ws:
        await send_result(ws)


asyncio.get_event_loop().run_until_complete(main())
