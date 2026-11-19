
import signal

background_processes = []


def register_background_process(process):
    """Enregistre un processus en arrière-plan."""

    if process.poll() is None:
        background_processes.append(process)
    else:
        print(
            f"\n[Arrière-plan] Processus {process.pid} terminé."
        )


def handle_sigint(signum, frame):
    """Gère Ctrl+C."""
    print(
        "\nOPSH : interruption reçue. "
        "Utilise quit pour quitter."
    )


def handle_sigchld(signum, frame):
    """Détecte les processus enfants terminés."""

    for process in background_processes[:]:

        return_code = process.poll()

        if return_code is not None:
            print(
                f"\n[Arrière-plan] Processus {process.pid} terminé."
            )
            background_processes.remove(process)


def setup_signals():
    """Configure les signaux du mini-shell."""

    signal.signal(signal.SIGINT, handle_sigint)
    signal.signal(signal.SIGCHLD, handle_sigchld)
