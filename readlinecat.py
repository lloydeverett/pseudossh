import readline
readline.parse_and_bind("set editing-mode vi")
try:
    while True:
        print(input())
except EOFError:
    pass

