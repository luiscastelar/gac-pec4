#!/bin/sh

echo "================================"
echo "Instalando aplicacion Python"
echo "================================"

# Comprobar python3
if ! command -v python3 >/dev/null 2>&1; then
    echo "ERROR: python3 no esta instalado"
    exit 1
fi

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
. venv/bin/activate

# Actualizar pip
pip install --upgrade pip

# Actualizar requrimientos
#pip freeze > requirements.txt


# Instalar dependencias
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
else
    echo "WARNING: requirements.txt no encontrado"
fi

echo "================================"
echo "Instalacion completada"
echo "================================"
sleep 5