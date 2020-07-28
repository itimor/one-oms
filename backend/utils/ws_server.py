# -*- coding: utf-8 -*-
# author: itimor

import asyncio
import websockets


# 检测客户端权限，用户名密码通过才能退出循环
async def check_permit(ws):
    while True:
        recv_text = await ws.recv()
        if recv_text == "admin":
            response_text = "congratulation, you have connect with server\r\nnow, you can do something else"
            await ws.send(response_text)
            return True
        else:
            response_text = "sorry, the username or password is wrong, please submit again"
            await ws.send(response_text)


# 接收客户端消息并处理，这里只是简单把客户端发来的返回回去
async def recv_msg(ws):
    while True:
        recv_text = await ws.recv()
        response_text = f"your submit context: {recv_text}"
        await ws.send(response_text)


# 服务器端主逻辑
# websocket和path是该函数被回调时自动传过来的，不需要自己传
async def main(ws, path):
    await check_permit(ws)

    await recv_msg(ws)


# 把ip换成自己本地的ip
start_server = websockets.serve(main, '127.0.0.1', 9527)
# 如果要给被回调的main_logic传递自定义参数，可使用以下形式
# 一、修改回调形式
# import functools
# start_server = websockets.serve(functools.partial(main_logic, other_param="test_value"), '10.10.6.91', 5678)
# 修改被回调函数定义，增加相应参数
# async def main_logic(websocket, path, other_param)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
