@echo off
echo ============================================================
echo   TESTE SIMPLES DO SISTEMA
echo ============================================================
echo.
echo Este script testa os componentes basicos do sistema.
echo.
echo Pressione qualquer tecla para iniciar o teste...
pause >nul
cls

echo.
echo ============================================================
echo   TESTE 1: Python
echo ============================================================
echo.
echo Testando se Python esta instalado...
echo.

python --version

if %errorlevel% neq 0 (
    echo.
    echo [FALHOU] Python NAO encontrado!
    echo.
    echo Instale Python de: https://www.python.org/downloads/
    echo.
    goto :fim
)

echo.
echo [OK] Python encontrado!
echo.
pause

echo.
echo ============================================================
echo   TESTE 2: Arquivo main.py
echo ============================================================
echo.
echo Verificando se main.py existe...
echo.

if exist main.py (
    echo [OK] main.py encontrado!
    dir main.py
) else (
    echo [FALHOU] main.py NAO encontrado!
    echo.
    echo Pasta atual: %CD%
    echo.
    goto :fim
)

echo.
pause

echo.
echo ============================================================
echo   TESTE 3: Modulos Python
echo ============================================================
echo.
echo Testando importacao dos modulos basicos...
echo.

python -c "print('Testando imports...')"
if %errorlevel% neq 0 (
    echo [FALHOU] Erro ao executar Python
    goto :fim
)

python -c "from modules import file_scanner; print('[OK] file_scanner')"
python -c "from modules import txt_reader; print('[OK] txt_reader')"
python -c "from modules import pdf_reader; print('[OK] pdf_reader')"
python -c "from modules import json_generator; print('[OK] json_generator')"

echo.
pause

echo.
echo ============================================================
echo   TESTE 4: Dependencias
echo ============================================================
echo.
echo Verificando dependencias instaladas...
echo.

python -c "import pypdf; print('[OK] pypdf instalado')" 2>nul
if %errorlevel% neq 0 (
    echo [AVISO] pypdf NAO instalado
)

python -c "import chardet; print('[OK] chardet instalado')" 2>nul
if %errorlevel% neq 0 (
    echo [AVISO] chardet NAO instalado
)

echo.
pause

echo.
echo ============================================================
echo   TESTE 5: Executar main.py com --help
echo ============================================================
echo.
echo Tentando executar o programa principal...
echo.

python main.py

echo.
echo Codigo de saida: %errorlevel%
echo.

:fim
echo.
echo ============================================================
echo   FIM DOS TESTES
echo ============================================================
echo.
echo Se todos os testes passaram, o sistema esta funcionando.
echo.
echo Para executar o programa completo, use:
echo   EXECUTAR_IA_JURIDICA.bat
echo.
echo Ou instale as dependencias com:
echo   INSTALAR_COMPLETO.bat
echo.
echo ============================================================
echo.
pause
