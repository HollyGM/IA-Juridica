@echo off
cls

echo ============================================================
echo   DEBUG COMPLETO DO SISTEMA
echo ============================================================
echo.
echo Este script mostra informacoes detalhadas para diagnostico.
echo.
pause
cls

echo.
echo ========================================
echo INFORMACAO 1: Versao do Windows
echo ========================================
echo.
ver
echo.
pause

echo.
echo ========================================
echo INFORMACAO 2: Pasta atual
echo ========================================
echo.
cd
echo.
pause

echo.
echo ========================================
echo INFORMACAO 3: Arquivos na pasta
echo ========================================
echo.
dir /b *.py *.bat *.txt *.md
echo.
pause

echo.
echo ========================================
echo INFORMACAO 4: Python
echo ========================================
echo.
where python
echo.
python --version
echo.
pause

echo.
echo ========================================
echo INFORMACAO 5: Testar Python basico
echo ========================================
echo.
python -c "print('Python esta funcionando!')"
python -c "print('2 + 2 =', 2+2)"
echo.
pause

echo.
echo ========================================
echo INFORMACAO 6: Testar imports
echo ========================================
echo.
python -c "import sys; print('Versao Python:', sys.version)"
python -c "import os; print('Sistema:', os.name)"
echo.
pause

echo.
echo ========================================
echo INFORMACAO 7: Testar modulos do projeto
echo ========================================
echo.
python -c "from modules import file_scanner; print('file_scanner: OK')"
python -c "from modules import txt_reader; print('txt_reader: OK')"
python -c "from modules import pdf_reader; print('pdf_reader: OK')"
python -c "from modules import json_generator; print('json_generator: OK')"
echo.
pause

echo.
echo ========================================
echo INFORMACAO 8: Dependencias PyPI
echo ========================================
echo.
python -c "try: import pypdf; print('pypdf: INSTALADO')\nexcept: print('pypdf: NAO INSTALADO')"
python -c "try: import chardet; print('chardet: INSTALADO')\nexcept: print('chardet: NAO INSTALADO')"
python -c "try: import spacy; print('spacy: INSTALADO')\nexcept: print('spacy: NAO INSTALADO')"
echo.
pause

echo.
echo ========================================
echo INFORMACAO 9: Tentar executar main.py
echo ========================================
echo.
echo Executando: python main.py
echo.
echo ATENCAO: O programa vai iniciar normalmente.
echo          Uma janela de selecao de pasta aparecera.
echo.
pause

python main.py

set ERROR_CODE=%errorlevel%

echo.
echo ========================================
echo RESULTADO
echo ========================================
echo.
echo Codigo de saida: %ERROR_CODE%
echo.

if %ERROR_CODE%==0 (
    echo Status: SUCESSO
) else (
    echo Status: ERRO
)

echo.
echo ========================================
echo FIM DO DEBUG
echo ========================================
echo.
pause
