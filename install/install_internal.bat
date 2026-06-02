@echo off
echo ================================
echo Instalando aplicacion Python
echo ================================

REM Comprobamos Python
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo ERROR: Python no esta instalado
    echo Descargalo desde https://www.python.org
    pause
    exit /b 1
)

REM Creamos entorno virtual
IF NOT EXIST venv (
    echo Creando entorno virtual...
    python -m venv venv
)

REM Activamos entorno virtual
call venv\Scripts\activate

REM Actualizamos pip
python -m pip install --upgrade pip

REM Actualizar requrimientos
::pip freeze > requirements.txt


REM Instalamos dependencias
IF EXIST requirements.txt (
    pip install -r requirements.txt
) ELSE (
    echo WARNING: requirements.txt no encontrado
)

echo ================================
echo Instalacion completada
echo ================================
pause
