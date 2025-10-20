@echo off
chcp 65001 >nul
title TXT/PDF to JSON Converter

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║  📚 CONVERSOR TXT/PDF ^> JSON                            ║
echo ║  Base de Conhecimento para IA                           ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

REM Instala/atualiza dependências silenciosamente
pip install -q -r requirements.txt 2>nul

REM Executa o programa
python main.py

echo.
pause
