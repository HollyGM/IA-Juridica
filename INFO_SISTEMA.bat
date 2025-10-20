@echo off
chcp 65001 > nul
color 0A
cls

echo ===============================================================================
echo   ℹ️  INFORMAÇÕES DO SISTEMA
echo   Sistema de IA Jurídica v2.0
echo ===============================================================================
echo.

python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python NÃO instalado
    echo.
    echo Por favor, instale Python 3.8+ de: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo 📊 VERSÃO DO PYTHON:
python --version
echo.

echo ===============================================================================
echo   📁 ESTRUTURA DO PROJETO
echo ===============================================================================
echo.

echo 📂 Módulos Python:
echo   • file_scanner.py      - Escaneia diretórios
echo   • txt_reader.py        - Lê arquivos TXT
echo   • pdf_reader.py        - Lê arquivos PDF
echo   • json_generator.py    - Gera JSON otimizado
echo   • legal_ner.py         - Extração de entidades jurídicas
echo   • legal_summarizer.py  - Sumarização de textos
echo   • nlp_processor.py     - Processador NLP principal
echo   • rag_indexer.py       - Indexação para RAG
echo.

echo 📄 Arquivos de Configuração:
echo   • config.py            - Configurações do sistema
echo   • requirements.txt     - Dependências Python
echo   • main.py              - Programa principal
echo.

echo 📚 Documentação:
echo   • START_HERE.txt       - Início rápido
echo   • GUIA_RAPIDO.md       - Tutorial passo a passo
echo   • README_V2.md         - Documentação completa
echo.

echo 🚀 Executáveis (.bat):
echo   • EXECUTAR_IA_JURIDICA.bat  - Execução completa
echo   • INSTALAR_COMPLETO.bat     - Instalador
echo   • MODO_RAPIDO.bat           - Modo rápido
echo   • TESTAR_NLP.bat            - Teste de módulos
echo   • VER_CONFIGURACAO.bat      - Ver config
echo   • INFO_SISTEMA.bat          - Este arquivo
echo.

echo ===============================================================================
echo   📊 ESTATÍSTICAS DO CÓDIGO
echo ===============================================================================
echo.

python -c "import os; py_files = [f for f in os.listdir('modules') if f.endswith('.py')]; print(f'Total de módulos Python: {len(py_files)}')"
python -c "import os; lines = 0; [lines := lines + len(open(f'modules/{f}', encoding='utf-8').readlines()) for f in os.listdir('modules') if f.endswith('.py')]; print(f'Total de linhas de código: {lines}')"

echo.

echo ===============================================================================
echo   🔍 VERIFICAÇÃO DE DEPENDÊNCIAS
echo ===============================================================================
echo.

python -c "import pypdf; print('✓ pypdf instalado')" 2>nul || echo "❌ pypdf NÃO instalado"
python -c "import chardet; print('✓ chardet instalado')" 2>nul || echo "❌ chardet NÃO instalado"
python -c "import spacy; print('✓ spaCy instalado')" 2>nul || echo "⚠ spaCy NÃO instalado (opcional para NLP)"
python -c "import transformers; print('✓ transformers instalado')" 2>nul || echo "⚠ transformers NÃO instalado (opcional para NLP)"
python -c "import torch; print('✓ PyTorch instalado')" 2>nul || echo "⚠ PyTorch NÃO instalado (opcional para NLP)"
python -c "from sentence_transformers import SentenceTransformer; print('✓ sentence-transformers instalado')" 2>nul || echo "⚠ sentence-transformers NÃO instalado (opcional para embeddings)"

echo.

echo ===============================================================================
echo   💾 ESPAÇO EM DISCO
echo ===============================================================================
echo.

python -c "import os; size = sum(os.path.getsize(os.path.join('modules', f)) for f in os.listdir('modules') if f.endswith('.py')) / 1024; print(f'Tamanho dos módulos: {size:.1f} KB')"

echo.

echo ===============================================================================
echo   🎯 RECURSOS DISPONÍVEIS
echo ===============================================================================
echo.

python -c "try: from modules.nlp_processor import LegalNLPProcessor; print('✓ Processador NLP disponível')\nexcept: print('⚠ Processador NLP não disponível')"

python -c "try: from modules.legal_ner import LegalEntityExtractor; print('✓ Extração de entidades disponível')\nexcept: print('⚠ Extração de entidades não disponível')"

python -c "try: from modules.legal_summarizer import LegalSummarizer; print('✓ Sumarização disponível')\nexcept: print('⚠ Sumarização não disponível')"

python -c "try: from modules.rag_indexer import RAGIndexer; print('✓ Indexação RAG disponível')\nexcept: print('⚠ Indexação RAG não disponível')"

echo.

echo ===============================================================================
echo   ℹ️  INFORMAÇÕES ADICIONAIS
echo ===============================================================================
echo.

python -c "from config import SYSTEM_INFO; print(f'Nome: {SYSTEM_INFO[\"name\"]}'); print(f'Versão: {SYSTEM_INFO[\"version\"]}'); print(f'Descrição: {SYSTEM_INFO[\"description\"]}')"

echo.

echo ===============================================================================
echo.

echo Para começar a usar o sistema:
echo   1. Execute INSTALAR_COMPLETO.bat (se ainda não instalou)
echo   2. Execute EXECUTAR_IA_JURIDICA.bat
echo.

echo Para mais informações:
echo   • Leia START_HERE.txt
echo   • Consulte GUIA_RAPIDO.md
echo.

echo ===============================================================================
echo.

pause
