
# asyncio.run(run_ssh())

#
# Readlining
#




# ssh = local['ssh']

# -T tells ssh not to allocate a pseudo-terminal
# ssh_command = ssh['-T', sys.argv[1:]]

# ssh_proc = ssh_command.popen()

# sys.stdout.buffer.write(ssh_proc.communicate('echo hi\n'.encode())[0])


# print(datetime.datetime.now().time())
# print(type(ssh_future.stdout))
# print(ssh_future.stdout)
# print(datetime.datetime.now().time())

# ls = local["ls"]
# ls["."] & FG

# with SshMachine('apollo.lloydeverett.com', user = 'lloyd', keyfile = '~/.ssh/id_rsa') as remote:
#     remote["ls"] & FG

# readline.parse_and_bind('tab: complete')
# readline.parse_and_bind('set editing-mode vi')

# while True:
#     line = input('Prompt ("exit" to quit)')
#     if line == "exit":
#         break
#     print("Entered: %s" % line)

