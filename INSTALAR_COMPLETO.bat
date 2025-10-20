@echo off
chcp 65001 > nul
color 0B
cls

echo ============================================================
echo   📦 INSTALADOR COMPLETO
echo   Sistema de IA Jurídica v2.0
echo ============================================================
echo.

REM Verifica se Python está instalado
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERRO: Python não encontrado!
    echo.
    echo Por favor, instale o Python 3.8 ou superior:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANTE: Durante a instalação, marque a opção
    echo "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo ✓ Python encontrado:
python --version
echo.

REM Atualiza pip
echo 📦 Atualizando pip...
python -m pip install --upgrade pip
echo.

REM Instala todas as dependências
echo ============================================================
echo   📦 INSTALANDO TODAS AS DEPENDÊNCIAS
echo ============================================================
echo.
echo ⚠ ATENÇÃO: Isso pode levar 5-15 minutos dependendo da sua conexão.
echo.
echo As seguintes bibliotecas serão instaladas:
echo   • PyPDF e pdfplumber (extração de PDF)
echo   • spaCy (processamento de linguagem natural)
echo   • Transformers (modelos de IA)
echo   • PyTorch (framework de deep learning)
echo   • Sentence-transformers (embeddings)
echo   • FAISS e ChromaDB (indexação vetorial)
echo   • E outras dependências...
echo.

pause

echo.
echo 📥 Instalando dependências do requirements.txt...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo ⚠ AVISO: Algumas dependências podem ter falhado.
    echo    Tentando instalar dependências críticas individualmente...
    echo.

    REM Instala dependências críticas uma por uma
    echo Instalando pypdf...
    pip install pypdf

    echo Instalando chardet...
    pip install chardet

    echo Instalando PyMuPDF...
    pip install PyMuPDF

    echo Instalando pdfplumber...
    pip install pdfplumber

    echo Instalando python-docx...
    pip install python-docx

    echo.
    echo ✓ Dependências básicas instaladas.
    echo.
    echo ⚠ Para funcionalidades NLP completas, você pode instalar manualmente:
    echo    pip install spacy transformers torch
    echo.
) else (
    echo.
    echo ✅ Todas as dependências instaladas com sucesso!
    echo.
)

REM Baixa modelo do spaCy para português
echo.
echo ============================================================
echo   📥 BAIXANDO MODELO DE LINGUAGEM PORTUGUESA
echo ============================================================
echo.

python -m spacy download pt_core_news_sm

if %errorlevel% neq 0 (
    echo.
    echo ⚠ Aviso: Não foi possível baixar o modelo do spaCy.
    echo.
    echo Você pode baixar manualmente depois com:
    echo    python -m spacy download pt_core_news_sm
    echo.
    echo O sistema ainda funcionará, mas com funcionalidades NLP limitadas.
) else (
    echo.
    echo ✅ Modelo de linguagem baixado com sucesso!
)

echo.
echo ============================================================
echo   ✅ INSTALAÇÃO CONCLUÍDA!
echo ============================================================
echo.
echo O sistema está pronto para uso!
echo.
echo Para executar o programa, use:
echo   • EXECUTAR_IA_JURIDICA.bat
echo.
echo Ou execute diretamente:
echo   python main.py
echo.
echo ============================================================
echo.

pause
