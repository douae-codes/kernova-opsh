
def say(args):
    """Affiche le message donne par l'utilisateur."""
    print(" ".join(args))


def osinfo():
    """Affiche les informations du cours."""
    print("Systèmes d'Exploitation - UIR/ESIN")


def help_command():
    """Affiche les commandes disponibles."""
    print("Commandes disponibles :")
    print("say     : afficher un message")
    print("osinfo  : afficher les informations du cours")
    print("help    : afficher cette aide")
    print("quit    : quitter OPSH")


def execute_builtin(command, args):
    """Reconnait et execute les commandes integrees."""

    if command == "say":
        say(args)

    elif command == "osinfo":
        osinfo()

    elif command == "help":
        help_command()

    else:
        return False

    return True
