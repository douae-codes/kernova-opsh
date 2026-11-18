
from commands import execute_builtin


def main():
    print("Bienvenue dans KERNOVA OPSH !")

    while True:
        command_line = input("opsh> ")
        parts = command_line.split()

        if not parts:
            continue

        command = parts[0]
        args = parts[1:]

        if command == "quit":
            print("Au revoir !")
            break

        execute_builtin(command, args)


if __name__ == "__main__":
    main()
