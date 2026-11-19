
import shlex


def parse_command(command_line):
    """Analyse les commandes, les pipes et les redirections."""

    command_line = command_line.replace(
        "->", " __OPSH_PIPE__ "
    )

    lexer = shlex.shlex(
        command_line,
        posix=True,
        punctuation_chars="<>"
    )

    lexer.whitespace_split = True
    lexer.commenters = ""

    parts = list(lexer)

    if not parts:
        return None, [], None, None, False, None

    # Gestion du pipe OPSH
    if "__OPSH_PIPE__" in parts:

        if parts.count("__OPSH_PIPE__") > 1:
            raise ValueError("Un seul pipe est autorisé.")

        index = parts.index("__OPSH_PIPE__")

        first = parts[:index]
        second = parts[index + 1:]

        if not first or not second:
            raise ValueError("Commande manquante autour du pipe.")

        return None, [], None, None, False, (first, second)

    command = parts[0]
    args = []

    input_file = None
    output_file = None
    append = False

    i = 1

    while i < len(parts):

        token = parts[i]

        if token == "<":

            if i + 1 >= len(parts):
                raise ValueError("Fichier d'entrée manquant.")

            input_file = parts[i + 1]
            i += 2

        elif token == ">":

            if i + 1 >= len(parts):
                raise ValueError("Fichier de sortie manquant.")

            output_file = parts[i + 1]
            append = False
            i += 2

        elif token == ">>":

            if i + 1 >= len(parts):
                raise ValueError("Fichier de sortie manquant.")

            output_file = parts[i + 1]
            append = True
            i += 2

        else:

            args.append(token)
            i += 1

    return command, args, input_file, output_file, append, None
