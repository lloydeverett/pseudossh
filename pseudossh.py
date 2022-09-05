#!/usr/bin/env python3

# import readline
import sys
import asyncio

#
# Plumbing for async
#

async def areadline() -> str:
    return await asyncio.get_event_loop().run_in_executor(
                  None, sys.stdin.readline)

#
# SSHing
#

async def ssh_init():
    return await asyncio.create_subprocess_exec(
                  'ssh',
                  *(['-T'] + sys.argv[1:]), # -T disables TTY allocation
                  stdin=asyncio.subprocess.PIPE,
                  stdout=asyncio.subprocess.PIPE,
                  stderr=asyncio.subprocess.PIPE)

async def ssh_hello_world(ssh_proc):
    sys.stdout.buffer.write((await ssh_proc.communicate(b'echo hello world'))[0])
    sys.stdout.buffer.flush()

#
# Tie everything together
#

async def main():
    await ssh_hello_world(await ssh_init())
    await areadline()

asyncio.run(main())

