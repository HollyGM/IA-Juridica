@echo off
cls

echo ============================================================
echo   SISTEMA DE IA JURIDICA v2.0
echo   Modo Simples e Direto
echo ============================================================
echo.
echo.

echo Passo 1: Verificando Python...
python --version
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo.
    echo Instale de: https://www.python.org/downloads/
    echo.
    pause
    exit
)
echo OK!
echo.
echo.

echo Passo 2: Verificando arquivo main.py...
if not exist main.py (
    echo ERRO: main.py nao encontrado!
    echo Pasta atual: %CD%
    echo.
    pause
    exit
)
echo OK!
echo.
echo.

echo Passo 3: Iniciando programa...
echo.
echo ============================================================
echo.

python main.py

echo.
echo ============================================================
echo.
echo Programa finalizado!
echo Codigo de saida: %errorlevel%
echo.
echo.

pause
