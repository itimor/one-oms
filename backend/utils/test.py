import subprocess
import time
import sys


# def run_shell(shell):
#     cmd = subprocess.Popen(shell, stdin=subprocess.PIPE, stderr=subprocess.PIPE,
#                            stdout=subprocess.PIPE, universal_newlines=True, shell=True, bufsize=1)
#     # 实时输出
#     while True:
#         line = cmd.stdout.readline()
#         print(line, end='')
#         if subprocess.Popen.poll(cmd) == 0:  # 判断子进程是否结束
#             break
#     cmd.stdout.close()
#     cmd.wait()
#     return cmd.returncode

def run_shell(shell):
    cmd = subprocess.Popen(shell, stdin=subprocess.PIPE, stderr=sys.stderr, close_fds=True,
                           stdout=sys.stdout, universal_newlines=True, shell=True, bufsize=1)
    out, err = cmd.communicate()
    errcode = cmd.returncode

    return errcode, out, err


if __name__ == '__main__':
    print(run_shell("ping -n 10 www.gogole.com"))
