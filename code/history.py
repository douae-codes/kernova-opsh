import os
import readline
import atexit

HISTORY_FILE = os.path.expanduser("~/.opsh_history")

COMMANDS = [
    "say", "go", "list", "path", "show",
    "copy", "move", "del", "newdir", "newfile",
    "osinfo", "help", "quit", "history", "export"
]


def setup_history():
    """Active et sauvegarde l'historique."""

    try:
        readline.read_history_file(HISTORY_FILE)
    except FileNotFoundError:
        pass

    readline.set_history_length(1000)
    atexit.register(readline.write_history_file, HISTORY_FILE)


def show_history():
    """Affiche l'historique des commandes."""

    for i in range(1, readline.get_current_history_length() + 1):
        command = readline.get_history_item(i)
        print(f"{i}: {command}")


def autocomplete(text, state):
    """Complète automatiquement les commandes."""

    matches = [
        command for command in COMMANDS
        if command.startswith(text)
    ]

    if state < len(matches):
        return matches[state]

    return None


def setup_autocomplete():
    """Active l'autocomplétion avec Tab."""

    readline.set_completer(autocomplete)
    readline.parse_and_bind("bind ^I rl_complete")