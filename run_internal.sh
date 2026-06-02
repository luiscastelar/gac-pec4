#!/bin/sh
# ============================================
# Lanzador de la aplicación Python (Linux/macOS)
# ============================================

# Cambiar al directorio del script
cd "$(dirname "$0")" || exit 1

# Comprobar Python
if ! command -v python3 >/dev/null 2>&1; then
    echo "ERROR: python3 no está instalado"
    exit 1
fi

while true; do
    runningNginx=$(docker inspect tarea2-nginx-1 | jq '.[].State.Running')
    if $runningNginx != "true"; then
        docker compose up -d
        sleep 3
    else
        break
    fi
done

# Ejecutar la aplicación
python3 App.py
exit 0