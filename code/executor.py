
import subprocess

from signals import register_background_process


ALIASES = {
    "list": "ls",
    "path": "pwd",
    "show": "cat",
    "copy": "cp",
    "move": "mv",
    "del": "rm",
    "newdir": "mkdir",
    "newfile": "touch"
}


def get_real_command(command):
    """Traduit un alias OPSH en commande système."""
    return ALIASES.get(command, command)


def execute_external(command, args, input_file=None,
                     output_file=None, append=False):
    """Exécute une commande externe avec redirections."""

    real_command = get_real_command(command)

    try:
        with open(input_file, "r") if input_file else open("/dev/null", "r") as source:

            if output_file:
                mode = "a" if append else "w"

                with open(output_file, mode) as output:
                    result = subprocess.run(
                        [real_command] + args,
                        stdin=source if input_file else None,
                        stdout=output
                    )
            else:
                result = subprocess.run(
                    [real_command] + args,
                    stdin=source if input_file else None
                )

        return result.returncode

    except FileNotFoundError:
        print("Erreur : commande ou fichier introuvable.")
        return 127

    except PermissionError:
        print("Erreur : permission refusée.")
        return 126

    except IsADirectoryError:
        print("Erreur : le chemin indiqué est un dossier.")
        return 1


def execute_pipe(first_command, second_command):
    """Relie deux commandes avec un pipe."""

    first_name = get_real_command(first_command[0])
    second_name = get_real_command(second_command[0])

    first_process = None

    try:
        first_process = subprocess.Popen(
            [first_name] + first_command[1:],
            stdout=subprocess.PIPE
        )

        second_process = subprocess.Popen(
            [second_name] + second_command[1:],
            stdin=first_process.stdout
        )

        first_process.stdout.close()

        second_process.wait()
        first_process.wait()

        return second_process.returncode

    except FileNotFoundError:
        print("Erreur : commande introuvable.")

        if first_process is not None:
            first_process.terminate()
            first_process.wait()

        return 127

    except PermissionError:
        print("Erreur : permission refusée.")

        if first_process is not None:
            first_process.terminate()
            first_process.wait()

        return 126


def execute_background(command, args, input_file=None,
                       output_file=None, append=False):
    """Lance une commande en arrière-plan."""

    real_command = get_real_command(command)

    source = None
    output = None

    try:
        if input_file:
            source = open(input_file, "r")

        if output_file:
            mode = "a" if append else "w"
            output = open(output_file, mode)

        process = subprocess.Popen(
            [real_command] + args,
            stdin=source,
            stdout=output
        )

        register_background_process(process)

        print(
            "[Arrière-plan] Processus lancé. PID :",
            process.pid
        )

        return process.pid

    except FileNotFoundError:
        print("Erreur : commande ou fichier introuvable.")
        return None

    except PermissionError:
        print("Erreur : permission refusée.")
        return None

    finally:
        if source is not None:
            source.close()

        if output is not None:
            output.close()
