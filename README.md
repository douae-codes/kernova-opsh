# kernova-opsh
KERNOVA - Python Mini-shell (OPSH) Project
# KERNOVA OPSH — Mini Shell en Python

## 1. Présentation du projet

KERNOVA OPSH est un mini-shell développé en Python dans le cadre du module Systèmes d'exploitation.

Son objectif est de reproduire certaines fonctionnalités d'un terminal Linux en proposant une interface en ligne de commande simple et personnalisée.

L'utilisateur peut saisir des commandes, exécuter des programmes externes et utiliser plusieurs mécanismes classiques des systèmes d'exploitation.

## 2. Fonctionnalités

Le projet propose notamment :

- **REPL** : interface interactive avec l'invite `opsh>`.
- **Commandes internes** : `say`, `go`, `osinfo`, `info`, `export`.
- **Alias personnalisés** : `list`, `path`, `show`, `copy`, `move`, `del`, `newdir`, `newfile`.
- **Redirections** : `>`, `>>` et `<`.
- **Pipelines** : opérateur personnalisé `->`.
- **Processus en arrière-plan** : opérateur `&`.
- **Signaux** : gestion de `SIGINT` et `SIGCHLD`.
- **Variables d'environnement** : `export`, `$VAR` et `${VAR}`.
- **Variables spéciales** : `$?` et `$!`.
- **Substitution de commandes** : `$(...)` et les backticks.
- **Historique** : conservation des commandes précédentes.
- **Autocomplétion** : complétion des commandes avec la touche Tab.
- **Fichier de configuration** : `.opshrc`.
- **Mode script** : exécution de fichiers `.opsh` avec des structures simples `if`, `for` et `while`.

## 3. Technologies utilisées

- Langage : Python 3
- Environnement de développement : Visual Studio Code
- Système de développement : macOS
- Gestion de versions : Git et GitHub
- Bibliothèques : os, sys, subprocess, shlex, signal, readline, re


## 4. Organisation du projet

```text
kernova-opsh/
├── .opshrc
├── README.md
├── test.opsh
└── code/
    ├── main.py
    ├── parser.py
    ├── executor.py
    ├── commands.py
    ├── signals.py
    └── history.py
```

## 5. Installation et exécution

### Prérequis

- Python 3 installé.
- Un terminal compatible.

### Lancer le shell

Depuis le dossier principal du projet :

```bash
python3 code/main.py
```

### Exécuter un script

```bash
python3 code/main.py test.opsh
```

## 6. Exemples d'utilisation

### Commandes simples

```text
opsh> say hi
opsh> list
opsh> path
opsh> go ..
opsh> osinfo
```

### Redirections

```text
opsh> say hi > message.txt
opsh> say hello >> message.txt
opsh> show < message.txt
```

### Pipeline

```text
opsh> show message.txt -> wc -l
```

### Arrière-plan

```text
opsh> sleep 5 &
```

### Variables

```text
opsh> export NOM=KERNOVA
opsh> say hi $NOM
```

### Historique et autocomplétion

```text
opsh> history
```

La touche Tab permet de compléter les noms de commandes.

## 7. Liens avec le cours

Le développement de KERNOVA OPSH permet de mettre en pratique plusieurs concepts du module Systèmes d'exploitation :

- Gestion des processus et exécution de commandes.
- Variables d'environnement.
- Communication entre processus avec les pipes.
- Redirections des entrées et sorties.
- Gestion des signaux.
- Interpréteurs de commandes et environnement utilisateur.

## 8. Limites et améliorations possibles

Certaines fonctionnalités sont simplifiées par rapport à un shell complet comme Bash. Les structures de contrôle du mode script prennent en charge une syntaxe limitée.

Des améliorations possibles comprennent la gestion avancée des processus, les pipes multiples, les redirections d'erreurs, la complétion des chemins et un véritable système de contrôle des jobs.

## 9. Équipe

**Nom du groupe : KERNOVA**

Projet réalisé dans le cadre du module Systèmes d'exploitation — UIR.