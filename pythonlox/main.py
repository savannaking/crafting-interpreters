import sys
from scanner.scanner import Scanner


def main():
    if len(sys.argv) > 2:
        print("PythonLox accepts only 0 or 1 command line arguments.")
        print("To run the REPL, use no arguments. To run a file, supply the file name.")
    elif sys.argv.count == 1:
        runFile(sys.argv[1])
    else:
        runPrompt()


def runFile(path: str):
    # implement this later
    return


def runPrompt():
    while True:
        print(">> ")
        line = input()
        if line == None:
            break
        run(line)
        hadError = False


def run(src: str):
    scanner = Scanner(src)
    tokens = scanner.scanTokens()

    for token in tokens:
        print(token)


main()
