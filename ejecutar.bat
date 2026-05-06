@echo off
title Analizador de Textos - Christian Lera
color 0A

echo ================================================
echo    ANALIZADOR DE TEXTOS AVANZADO
echo    Autor: Christian Lera
echo ================================================
echo.

echo [INFO] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado o no esta en el PATH.
    echo [SOLUCION] Instala Python desde https://www.python.org/downloads/
    echo           Asegurate de marcar "Add Python to PATH" durante la instalacion.
    pause
    exit /b 1
)

echo [OK] Python encontrado
echo.

echo [INFO] Verificando dependencias...
pip show matplotlib >nul 2>&1
if errorlevel 1 (
    echo [ADVERTENCIA] Matplotlib no instalado
    echo [INFO] Instalando dependencias...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Error al instalar dependencias
        pause
        exit /b 1
    )
    echo [OK] Dependencias instaladas correctamente
) else (
    echo [OK] Dependencias verificadas
)
echo.

echo [INFO] Iniciando aplicacion...
echo.
echo ================================================
python ContadorDePalabras.py

if errorlevel 1 (
    echo.
    echo [ERROR] La aplicacion se cerro inesperadamente
    echo [INFO] Verifica que todos los archivos esten presentes
    pause
) else (
    echo.
    echo [INFO] Aplicacion cerrada correctamente
    timeout /t 2 >nul
)