#!/usr/bin/env python3

import os
import sys

r_child_stdin, w_child_stdin = os.pipe()
r_child_stdout, w_child_stdout = os.pipe()

pid = os.fork()
if pid: # Parent
    os.close(r_child_stdin)
    os.close(w_child_stdout)

    f_w_child_stdin = os.fdopen(w_child_stdin, 'wb', 0)
    f_r_child_stdout = os.fdopen(r_child_stdout, 'rb', 0)

    f_w_child_stdin.write(b'hello\n')
    while True:
        data = f_r_child_stdout.readline()
        if not data: break
        print('child stdout to parent: ' + data.decode())
else:
    os.close(w_child_stdin)
    os.close(r_child_stdout)
    os.dup2(r_child_stdin, sys.stdin.fileno())
    os.dup2(w_child_stdout, sys.stdout.fileno())
    os.close(r_child_stdin)
    os.close(w_child_stdout)
    s = input()
    print(s)
    # w = os.fdopen(w_p, 'wb', 0)
    # for i in range(10):
    #     w.write(b'line\n')
    #     w.flush()
    #     print('hello child')
    #     time.sleep(1)

