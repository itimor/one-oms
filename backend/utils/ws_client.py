# -*- coding: utf-8 -*-
# author: itimor

import asyncio
import websockets


# 向服务器端认证，用户名密码通过才能退出循环
async def auth_system(ws):
    while True:
        cred_text = input("please enter your username: ")
        await ws.send(cred_text)
        response_str = await ws.recv()
        print(response_str)
        if "congratulation" in response_str:
            return True


# 向服务器端发送认证后的消息
async def send_msg(ws):
    while True:
        _text = input("please enter your context: ")
        if _text == "exit" or _text == 'quit':
            print(f'you have enter "exit", goodbye')
            await ws.close(reason="user exit")
            return False
        await ws.send(_text)
        response_str = await ws.recv()
        print(response_str)


# 客户端主逻辑
async def main():
    async with websockets.connect('ws://127.0.0.1:9527') as ws:
        await auth_system(ws)
        await send_msg(ws)
