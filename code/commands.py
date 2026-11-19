
import os


def say(args):
    """Affiche un message."""
    print(" ".join(args))
    return 0


def osinfo():
    """Affiche les informations du cours."""
    print("Systèmes d’Exploitation – UIR/ESIN")
    return 0


def go(args):
    """Change le répertoire courant."""
    path = args[0] if args else os.path.expanduser("~")

    try:
        os.chdir(os.path.expanduser(path))
        return 0
    except FileNotFoundError:
        print("Erreur : répertoire introuvable.")
    except NotADirectoryError:
        print("Erreur : ce n'est pas un répertoire.")
    except PermissionError:
        print("Erreur : permission refusée.")

    return 1


def export_variable(args):
    """Définit des variables d'environnement."""
    if not args:
        print("Utilisation : export NOM=valeur")
        return 1

    for assignment in args:
        if "=" not in assignment:
            print("Erreur : utilise NOM=valeur.")
            return 1

        name, value = assignment.split("=", 1)

        if not name.isidentifier():
            print("Erreur : nom de variable invalide.")
            return 1

        os.environ[name] = value

    return 0


def help_command():
    """Affiche l'aide."""
    print("Commandes KERNOVA OPSH :")
    print("go      : changer de répertoire")
    print("list    : afficher les fichiers")
    print("path    : afficher le répertoire courant")
    print("show    : afficher un fichier")
    print("copy    : copier un fichier")
    print("move    : déplacer un fichier")
    print("del     : supprimer un fichier")
    print("newdir  : créer un répertoire")
    print("newfile : créer un fichier")
    print("say     : afficher un message")
    print("info    : afficher cette aide")
    print("osinfo  : informations du cours")
    print("export  : définir une variable")
    print("history : afficher l'historique")
    print("quit    : quitter OPSH")
    return 0


def execute_builtin(command, args):
    """Exécute une commande interne."""

    if command in ("say", "echo"):
        return say(args)

    if command in ("go", "cd"):
        return go(args)

    if command == "osinfo":
        return osinfo()

    if command in ("info", "help"):
        return help_command()

    if command == "export":
        return export_variable(args)

    return None
