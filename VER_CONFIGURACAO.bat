@echo off
chcp 65001 > nul
color 0D
cls

echo ============================================================
echo   ⚙️ CONFIGURAÇÕES DO SISTEMA
echo   Sistema de IA Jurídica v2.0
echo ============================================================
echo.

python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERRO: Python não encontrado!
    pause
    exit /b 1
)

echo Exibindo configurações disponíveis...
echo.

python config.py

echo.
echo ============================================================
echo.
echo Para personalizar as configurações, edite o arquivo:
echo   config.py
echo.
echo ============================================================
echo.

pause
