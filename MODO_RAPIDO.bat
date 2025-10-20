@echo off
chcp 65001 > nul
color 0E
cls

echo ============================================================
echo   ⚡ MODO RÁPIDO
echo   Sistema de IA Jurídica v2.0
echo ============================================================
echo   Processamento rápido sem análise NLP completa
echo ============================================================
echo.

REM Verifica Python
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERRO: Python não encontrado!
    pause
    exit /b 1
)

echo ⚡ Executando em modo rápido (apenas extração de texto)...
echo.
echo Este modo:
echo   ✓ Extrai texto de PDF e TXT
echo   ✓ Gera JSON otimizado
echo   ✗ NÃO faz análise NLP (mais rápido)
echo.

REM Cria um arquivo temporário de configuração
echo enable_nlp = False > temp_config.txt

echo ============================================================
echo   🚀 INICIANDO...
echo ============================================================
echo.

python main.py

del temp_config.txt 2>nul

echo.
pause
