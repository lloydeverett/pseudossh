#!/usr/bin/env python3
import os
import sys
import select
import termios
import tty
import pty
import time
from subprocess import Popen

# It seems like it's better to run ssh in a shell here as otherwise detecting an EOF
# is strangely difficult.
command = ['bash', '-c', 'ssh -t apollo.lloydeverett.com bash']
# PS1=${PS1}DEADBEEF 

# save original tty setting then set it to raw mode
old_tty = termios.tcgetattr(sys.stdin)
tty.setraw(sys.stdin.fileno())

# open pseudo-terminal to interact with subprocess
master_fd, slave_fd = pty.openpty()

# open another pseudo-terminal to interact with another subprocess
# command2 = "vim".split()
# master_fd2, slave_fd2 = pty.openpty()

# Same deal for readlinecat
readline_command = ['env', 'python3', 'readlinecat.py']
readline_master_fd, readline_slave_fd = pty.openpty()

try:
    # use os.setsid() make it run in a new process group, or bash job control will not be enabled
    p = Popen(command,
              preexec_fn=os.setsid,
              stdin=slave_fd,
              stdout=slave_fd,
              stderr=slave_fd,
              universal_newlines=True)
    readline_p = Popen(readline_command,
              preexec_fn=os.setsid,
              stdin=readline_slave_fd,
              stdout=readline_slave_fd,
              stderr=readline_slave_fd,
              universal_newlines=True)

#    start = time.time()
#    while time.time() - start < 5:
#        r, w, e = select.select([sys.stdin, master_fd], [], [])
#        if sys.stdin in r:
#            d = os.read(sys.stdin.fileno(), 10240)
#            os.write(master_fd, d)
#        elif master_fd in r:
#            o = os.read(master_fd, 10240)
#            if o:
#                os.write(sys.stdout.fileno(), o)
#
#    p2 = Popen(command2,
#              preexec_fn=os.setsid,
#              stdin=slave_fd2,
#              stdout=slave_fd2,
#              stderr=slave_fd2,
#              universal_newlines=True)
#    start = time.time()
#    while p2.poll() is None: # time.time() - start < 5:
#        r, w, e = select.select([sys.stdin, master_fd2], [], [])
#        if sys.stdin in r:
#            d = os.read(sys.stdin.fileno(), 10240)
#            os.write(master_fd2, d)
#        elif master_fd2 in r:
#            o = os.read(master_fd2, 10240)
#            if o:
#                os.write(sys.stdout.fileno(), o)
    accumulated = b''
    queued = b''

    # Setup prompt
    os.write(master_fd, b"export PS1=${PS1}DEADBEEF > /dev/null\n")

    # jostle readline
    os.write(readline_master_fd, b"hello world\n")

    while p.poll() is None:
        r, w, e = select.select([sys.stdin, master_fd, readline_master_fd], [], [])
        if sys.stdin in r:
            d = os.read(sys.stdin.fileno(), 10240)
            if d.decode("utf-8").isalnum():
                accumulated = accumulated + d
                os.write(sys.stdout.fileno(), d)
            else:
                # TODO: Use escape sequences? And maybe clear what you've written.
                queued = queued + b'\b' * len(accumulated)
                os.write(master_fd, accumulated + d)
                accumulated = b''
        elif master_fd in r:
            o = os.read(master_fd, 10240)
            if not o:
                continue
            os.write(sys.stdout.fileno(), queued + o)
            queued = b''
        elif readline_master_fd in r:
            o = os.read(readline_master_fd, 10240)
            if not o:
                continue
            print(o)
finally:
    # restore tty settings back
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_tty)

