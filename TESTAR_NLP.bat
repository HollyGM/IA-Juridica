@echo off
chcp 65001 > nul
color 0C
cls

echo ============================================================
echo   🧪 TESTE DE MÓDULOS NLP
echo   Sistema de IA Jurídica v2.0
echo ============================================================
echo.

python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERRO: Python não encontrado!
    pause
    exit /b 1
)

echo Testando importação de módulos NLP...
echo.

python -c "from modules.nlp_processor import LegalNLPProcessor; print('✓ nlp_processor OK')" 2>nul
if %errorlevel% neq 0 (
    echo ❌ nlp_processor - FALHOU
) else (
    echo ✓ nlp_processor - OK
)

python -c "from modules.legal_ner import LegalEntityExtractor; print('✓ legal_ner OK')" 2>nul
if %errorlevel% neq 0 (
    echo ❌ legal_ner - FALHOU
) else (
    echo ✓ legal_ner - OK
)

python -c "from modules.legal_summarizer import LegalSummarizer; print('✓ legal_summarizer OK')" 2>nul
if %errorlevel% neq 0 (
    echo ❌ legal_summarizer - FALHOU
) else (
    echo ✓ legal_summarizer - OK
)

python -c "from modules.rag_indexer import RAGIndexer; print('✓ rag_indexer OK')" 2>nul
if %errorlevel% neq 0 (
    echo ❌ rag_indexer - FALHOU
) else (
    echo ✓ rag_indexer - OK
)

echo.
echo Testando bibliotecas externas...
echo.

python -c "import spacy; print('✓ spaCy instalado'); m = spacy.load('pt_core_news_sm'); print('  ✓ Modelo português disponível')" 2>nul
if %errorlevel% neq 0 (
    echo ❌ spaCy ou modelo português - NÃO DISPONÍVEL
    echo    Instale com: python -m spacy download pt_core_news_sm
) else (
    echo ✓ spaCy - OK
)

python -c "import transformers; print('✓ Transformers instalado')" 2>nul
if %errorlevel% neq 0 (
    echo ❌ Transformers - NÃO INSTALADO
) else (
    echo ✓ Transformers - OK
)

python -c "import torch; print('✓ PyTorch instalado')" 2>nul
if %errorlevel% neq 0 (
    echo ❌ PyTorch - NÃO INSTALADO
) else (
    echo ✓ PyTorch - OK
)

python -c "from sentence_transformers import SentenceTransformer; print('✓ Sentence-Transformers instalado')" 2>nul
if %errorlevel% neq 0 (
    echo ❌ Sentence-Transformers - NÃO INSTALADO
) else (
    echo ✓ Sentence-Transformers - OK
)

python -c "import faiss; print('✓ FAISS instalado')" 2>nul
if %errorlevel% neq 0 (
    echo ⚠ FAISS - NÃO INSTALADO (opcional)
) else (
    echo ✓ FAISS - OK
)

echo.
echo ============================================================
echo   RESUMO
echo ============================================================
echo.
echo Se todos os módulos essenciais estão OK, o sistema está
echo pronto para usar com análise NLP completa.
echo.
echo Se algum módulo falhou, execute:
echo   INSTALAR_COMPLETO.bat
echo.
echo ============================================================
echo.

pause
