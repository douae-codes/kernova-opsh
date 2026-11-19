
import os
import re
import sys
import subprocess

from contextlib import redirect_stdout

from parser import parse_command
from executor import (
    execute_external,
    execute_pipe,
    execute_background
)
from commands import execute_builtin
from signals import setup_signals
from history import (
    setup_history,
    show_history,
    setup_autocomplete
)


def expand_variables(text, last_status, last_background_pid):
    """Développe les variables d'environnement et les variables spéciales."""

    def replace_special(match):
        value = match.group(0)

        if value == "$?":
            return str(last_status)

        if value == "$!":
            return str(last_background_pid or "")

        name = match.group(1) or match.group(2)
        return os.environ.get(name, "")

    pattern = r"\$\{([^}]+)\}|\$([A-Za-z_][A-Za-z0-9_]*)|\$\?|\$!"
    return re.sub(pattern, replace_special, text)


def expand_substitution(text):
    """Exécute les substitutions $(...) et les backticks."""

    pattern = r"\$\(([^()]*)\)|`([^`]*)`"

    def replace(match):
        command = match.group(1) or match.group(2)

        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                check=False
            )
            return result.stdout.rstrip("\n")

        except OSError:
            print("Erreur pendant la substitution de commande.")
            return ""

    return re.sub(pattern, replace, text)


def execute_line(command_line, last_status, last_background_pid):
    """Analyse et exécute une ligne de commande."""

    command_line = command_line.strip()

    if not command_line:
        return last_status, last_background_pid, False

    # Détection de l'arrière-plan
    background = command_line.endswith("&")

    if background:
        command_line = command_line[:-1].strip()

    # Substitution de commandes
    command_line = expand_substitution(command_line)

    # Développement des variables
    command_line = expand_variables(
        command_line,
        last_status,
        last_background_pid
    )

    try:
        (
            command,
            args,
            input_file,
            output_file,
            append,
            pipe
        ) = parse_command(command_line)

    except ValueError as error:
        print("Erreur :", error)
        return 2, last_background_pid, False

    if command is None and pipe is None:
        return last_status, last_background_pid, False

    # Quitter OPSH
    if command == "quit":
        print("Au revoir !")
        return last_status, last_background_pid, True

    # Afficher l'historique
    if command == "history":
        show_history()
        return 0, last_background_pid, False

    # Exécuter un pipe
    if pipe:

        if background:
            print("Erreur : pipe en arrière-plan non disponible.")
            return 1, last_background_pid, False

        status = execute_pipe(pipe[0], pipe[1])
        return status, last_background_pid, False

    # Exécuter une commande en arrière-plan
    if background:

        if command in (
            "say", "echo", "go", "cd",
            "osinfo", "info", "help", "export"
        ):
            print("Erreur : commande interne non disponible en arrière-plan.")
            return 1, last_background_pid, False

        pid = execute_background(
            command,
            args,
            input_file,
            output_file,
            append
        )

        if pid is not None:
            return 0, pid, False

        return 1, last_background_pid, False

    # Redirection de la sortie des commandes internes
    if command in (
        "say", "echo", "osinfo", "info", "help"
    ) and output_file:

        mode = "a" if append else "w"

        try:
            with open(output_file, mode) as file:
                with redirect_stdout(file):
                    status = execute_builtin(command, args)

            return status, last_background_pid, False

        except OSError as error:
            print("Erreur :", error)
            return 1, last_background_pid, False

    # Commandes internes
    result = execute_builtin(command, args)

    if result is not None:
        return result, last_background_pid, False

    # Commandes externes
    status = execute_external(
        command,
        args,
        input_file,
        output_file,
        append
    )

    return status, last_background_pid, False


def load_opshrc(last_status, last_background_pid):
    """Charge le fichier .opshrc du projet."""

    project_folder = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    config_file = os.path.join(project_folder, ".opshrc")

    if not os.path.isfile(config_file):
        return last_status, last_background_pid

    print("Chargement de .opshrc...")

    with open(config_file, "r") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            last_status, last_background_pid, should_quit = execute_line(
                line,
                last_status,
                last_background_pid
            )

            if should_quit:
                break

    return last_status, last_background_pid



def evaluate_condition(condition, last_status, last_background_pid):
    """Évalue une condition simple."""

    condition = expand_variables(
        condition, last_status, last_background_pid
    )

    parts = condition.split()

    if len(parts) == 3:
        left, operator, right = parts

        if operator in ("==", "="):
            return left == right

        if operator == "!=":
            return left != right

        try:
            a = float(left)
            b = float(right)

            if operator in ("-eq",):
                return a == b
            if operator in ("-ne",):
                return a != b
            if operator in ("-gt", ">"):
                return a > b
            if operator in ("-lt", "<"):
                return a < b
            if operator in ("-ge", ">="):
                return a >= b
            if operator in ("-le", "<="):
                return a <= b

        except ValueError:
            return False

    return bool(condition)


def execute_script_lines(lines, last_status=0,
                         last_background_pid=None, depth=0):
    """Exécute les lignes d'un script avec des structures de contrôle."""

    if depth > 20:
        print("Erreur : trop de niveaux d'imbrication.")
        return last_status, last_background_pid

    i = 0

    while i < len(lines):
        line = lines[i].strip()

        if not line or line.startswith("#"):
            i += 1
            continue

        # IF
        if line.startswith("if "):
            condition = line[3:].strip()
            block = []
            else_block = []
            level = 1
            in_else = False
            i += 1

            while i < len(lines):
                current = lines[i].strip()

                if current.startswith("if "):
                    level += 1

                elif current == "endif":
                    level -= 1

                    if level == 0:
                        break

                elif current == "else" and level == 1:
                    in_else = True
                    i += 1
                    continue

                if in_else:
                    else_block.append(lines[i])
                else:
                    block.append(lines[i])

                i += 1

            if level != 0:
                print("Erreur : endif manquant.")
                return 1, last_background_pid

            if evaluate_condition(
                condition, last_status, last_background_pid
            ):
                last_status, last_background_pid = execute_script_lines(
                    block, last_status, last_background_pid, depth + 1
                )
            else:
                last_status, last_background_pid = execute_script_lines(
                    else_block, last_status, last_background_pid, depth + 1
                )

            i += 1
            continue

        # FOR
        if line.startswith("for "):
            parts = line.split()

            if len(parts) < 4 or parts[2] != "in":
                print("Erreur : syntaxe for invalide.")
                return 1, last_background_pid

            variable = parts[1]
            values = parts[3:]

            if not variable.isidentifier():
                print("Erreur : nom de variable invalide.")
                return 1, last_background_pid

            block = []
            level = 1
            i += 1

            while i < len(lines):
                current = lines[i].strip()

                if current.startswith("for "):
                    level += 1
                elif current == "endfor":
                    level -= 1
                    if level == 0:
                        break

                block.append(lines[i])
                i += 1

            if level != 0:
                print("Erreur : endfor manquant.")
                return 1, last_background_pid

            for value in values:
                os.environ[variable] = value

                last_status, last_background_pid = execute_script_lines(
                    block, last_status, last_background_pid, depth + 1
                )

            i += 1
            continue

        # WHILE
        if line.startswith("while "):
            condition = line[6:].strip()
            block = []
            level = 1
            i += 1

            while i < len(lines):
                current = lines[i].strip()

                if current.startswith("while "):
                    level += 1
                elif current == "endwhile":
                    level -= 1
                    if level == 0:
                        break

                block.append(lines[i])
                i += 1

            if level != 0:
                print("Erreur : endwhile manquant.")
                return 1, last_background_pid

            iterations = 0

            while evaluate_condition(
                condition, last_status, last_background_pid
            ):
                last_status, last_background_pid = execute_script_lines(
                    block, last_status, last_background_pid, depth + 1
                )

                iterations += 1

                if iterations >= 1000:
                    print("Erreur : limite de 1000 répétitions atteinte.")
                    break

            i += 1
            continue

        # Fin de bloc sans ouverture
        if line in ("else", "endif", "endfor", "endwhile"):
            print("Erreur : structure de contrôle inattendue :", line)
            return 1, last_background_pid

        print(f"opsh> {line}")

        last_status, last_background_pid, should_quit = execute_line(
            line, last_status, last_background_pid
        )

        if should_quit:
            return last_status, last_background_pid

        i += 1

    return last_status, last_background_pid


def run_script(script_path, last_status, last_background_pid):
    """Exécute un fichier de commandes OPSH."""

    try:
        with open(script_path, "r") as script:
            lines = script.readlines()

        return execute_script_lines(
            lines, last_status, last_background_pid
        )[0]

    except FileNotFoundError:
        print("Erreur : script introuvable.")
        return 1

    except PermissionError:
        print("Erreur : permission refusée.")
        return 1


def main():
    setup_signals()
    setup_history()
    setup_autocomplete()

    print("Bienvenue dans KERNOVA OPSH !")

    last_status = 0
    last_background_pid = None

    # Chargement de la configuration
    last_status, last_background_pid = load_opshrc(
        last_status,
        last_background_pid
    )

    # Mode script : python3 code/main.py fichier.opsh
    if len(sys.argv) > 1:
        last_status = run_script(
            sys.argv[1],
            last_status,
            last_background_pid
        )
        return

    # Mode interactif
    while True:

        try:
            command_line = input("opsh> ")

        except KeyboardInterrupt:
            print("\nUtilise quit pour quitter OPSH.")
            continue

        except EOFError:
            print("\nAu revoir !")
            break

        last_status, last_background_pid, should_quit = execute_line(
            command_line,
            last_status,
            last_background_pid
        )

        if should_quit:
            break


if __name__ == "__main__":
    main()
