#!/usr/bin/env python3

# import readline
import sys
import asyncio
import aioconsole

#
# Async stuff
#

async def get_steam_reader(pipe) -> asyncio.StreamReader:
    loop = asyncio.get_event_loop()
    reader = asyncio.StreamReader(loop=loop)
    protocol = asyncio.StreamReaderProtocol(reader)
    await loop.connect_read_pipe(lambda: protocol, pipe)
    return reader

#
# Async handles for standard in/out/err
#

astdin = None
astdout = None
astderr = None

#
# SSHing
#

async def ssh_init():
    return await asyncio.create_subprocess_exec(
                  'ssh',
                  *(['-t'] + sys.argv[1:]), # -t forces TTY allocation
                  stdin=asyncio.subprocess.PIPE,
                  stdout=asyncio.subprocess.PIPE,
                  stderr=asyncio.subprocess.PIPE)

async def my_pipe_stdout(ssh_proc):
    while True:
        data = await ssh_proc.stdout.read(1)
        astdout.write(data)

async def my_pipe_stderr(ssh_proc):
    while True:
        data = await astderr.read(1)
        ssh_proc.stderr.write(data)

async def my_pipe_stdin(ssh_proc):
    while True:
        data = await astdin.read(1)
        ssh_proc.stdin.write(data)

async def ssh_hello_world(ssh_proc):
    await asyncio.gather(my_pipe_stdout(ssh_proc), my_pipe_stdin(ssh_proc))
    # sys.stdout.buffer.write((await ssh_proc.communicate(b'echo hello world'))[0])
    # sys.stdout.buffer.flush()

#
# Tie everything together
#

async def main():
    global astdin
    global astdout
    global astderr
    astdin, astdout = await aioconsole.get_standard_streams()
    _, astderr = await aioconsole.get_standard_streams(use_stderr=False)
    await ssh_hello_world(await ssh_init())

asyncio.run(main())

# might need to get name of current shell
# match it to a list of expected shells [bash, zsh], if it matches ok, otherwise complain
# syntax checking: bash -nc "echo hi'"

