#!/bin/sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

x-terminal-emulator

open_terminal() {
    if command -v gnome-terminal >/dev/null 2>&1; then
        gnome-terminal -- bash -c "$1"
    elif command -v konsole >/dev/null 2>&1; then
        konsole -e bash -c "$1"
    elif command -v xterm >/dev/null 2>&1; then
        xterm -e bash -c "$1"
    else
        echo "Este script no puede determinar tu emulador de terminal."
        echo "Deberás lanzar la aplicación manualmente con: 'python3 html2graphml.py'"
        exit 1
    fi
}

open_terminal "$SCRIPT_DIR/run_internal.sh"
