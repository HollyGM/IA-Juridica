@echo off
chcp 65001 >nul
title Instalação de Dependências
color 0B

echo ============================================================
echo   📦 INSTALADOR DE DEPENDÊNCIAS
echo   Conversor TXT/PDF para JSON
echo ============================================================
echo.

REM Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERRO: Python não está instalado!
    echo.
    echo Por favor, instale Python 3.7 ou superior de:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANTE: Durante a instalação, marque a opção
    echo "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo ✅ Python encontrado:
python --version
echo.

REM Verifica se pip está disponível
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERRO: pip não está disponível!
    echo.
    echo Reinstale Python marcando todas as opções
    echo.
    pause
    exit /b 1
)

echo ✅ pip encontrado:
pip --version
echo.

echo ============================================================
echo   📥 Instalando dependências do requirements.txt
echo ============================================================
echo.

pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ❌ Erro ao instalar dependências!
    echo.
    echo Tente manualmente:
    echo   pip install pypdf chardet
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   ✅ INSTALAÇÃO CONCLUÍDA COM SUCESSO!
echo ============================================================
echo.
echo Você já pode usar o programa executando:
echo   - executar.bat (recomendado)
echo   - python main.py
echo.
pause
