# 🧠 Sistema de IA Jurídica - Estrategista Jurídico-Cognitivo v2.0

Sistema avançado de processamento de documentos jurídicos com análise NLP, extração de entidades, sumarização e preparação para sistemas RAG (Retrieval-Augmented Generation).

## 🎯 Características Principais

### Versão 2.0 - Novidades

- ✅ **Extração de Entidades Jurídicas (NER)**
  - Processos, números de ação
  - Leis, artigos, decretos
  - Tribunais (STF, STJ, TJs, TRFs)
  - Ministros e desembargadores
  - Varas e comarcas
  - Súmulas e jurisprudências
  - Valores monetários
  - Datas e documentos (CPF/CNPJ)

- ✅ **Sumarização Inteligente**
  - Sumarização extrativa (baseada em scoring)
  - Sumarização abstrativa (com modelos ML quando disponível)
  - Extração de pontos-chave
  - Identificação de seções (ementa, voto, decisão)

- ✅ **Análise Estrutural**
  - Identificação de teses principais e subsidiárias
  - Extração de argumentos favoráveis e contrários
  - Detecção de refutações
  - Análise de fundamentação

- ✅ **Classificação de Documentos**
  - Tipo de documento (acórdão, sentença, petição, etc.)
  - Área do direito (civil, penal, trabalhista, etc.)
  - Análise de decisão (procedente, improcedente)
  - Métricas de complexidade

- ✅ **Preparação para RAG**
  - Chunking inteligente com sobreposição
  - Geração de embeddings vetoriais
  - Indexação com FAISS
  - Mapeamento de chunks para documentos

## 📦 Instalação

### Instalação Rápida (Recomendado)

```bash
# Execute o instalador automático
INSTALAR_COMPLETO.bat
```

### Instalação Manual

```bash
# 1. Instale as dependências
pip install -r requirements.txt

# 2. Baixe o modelo de linguagem portuguesa
python -m spacy download pt_core_news_sm
```

## 🚀 Como Usar

### Método 1: Executável com Interface

```bash
# Execute o arquivo .bat
EXECUTAR_IA_JURIDICA.bat
```

### Método 2: Linha de Comando

```bash
# Execução padrão (com opções interativas)
python main.py
```

### Método 3: Modo Rápido (sem NLP)

```bash
# Processamento rápido sem análise NLP
MODO_RAPIDO.bat
```

## ⚙️ Modos de Processamento

### 1. Modo RÁPIDO
- Apenas extração de texto
- Geração de JSON básico
- Ideal para testes rápidos
- Tempo: ~1-2 segundos por documento

### 2. Modo PADRÃO (Recomendado)
- Extração de texto
- NER (entidades jurídicas)
- Sumarização
- Classificação
- Tempo: ~5-10 segundos por documento

### 3. Modo COMPLETO
- Todos os recursos do modo padrão
- Geração de embeddings vetoriais
- Indexação FAISS
- Preparação completa para RAG
- Tempo: ~15-30 segundos por documento

## 📁 Estrutura de Saída JSON

```json
{
  "schema_version": "2.0",
  "generated_at": "2024-10-14T...",
  "system": {
    "name": "Sistema de IA Jurídica",
    "version": "2.0.0",
    "features": ["NER", "Sumarização", "RAG", "Classificação"]
  },
  "metadata": {
    "source_directory": "...",
    "total_files": 10,
    "nlp_enabled": true
  },
  "statistics": {
    "total_documents": 10,
    "total_characters": 50000,
    "total_words": 8000,
    "nlp_analysis": {
      "documents_with_nlp": 10,
      "total_entities": 245,
      "entity_types": {
        "processos": 15,
        "leis": 28,
        "tribunais": 12
      },
      "document_types": {
        "acordao": 5,
        "sentenca": 3
      }
    }
  },
  "documents": [
    {
      "id": "doc_0001",
      "filename": "documento.pdf",
      "content": "...",
      "nlp_analysis": {
        "entidades": {
          "processos": [...],
          "leis": [...],
          "tribunais": [...]
        },
        "sumarizacao": {
          "resumo": "...",
          "pontos_chave": [...]
        },
        "classificacao": {
          "tipo_documento": "acordao",
          "area_direito": ["civil", "consumidor"]
        },
        "analise_estrutural": {
          "teses_principais": [...],
          "argumentos_favoraveis": [...]
        }
      }
    }
  ]
}
```

## 🔧 Configuração Avançada

Edite o arquivo `config.py` para personalizar:

```python
NLP_CONFIG = {
    'enable_ner': True,              # Extração de entidades
    'enable_summarization': True,    # Sumarização
    'enable_embeddings': False,      # Embeddings (requer mais recursos)

    'summarization': {
        'max_length': 500,           # Tamanho máximo do resumo
        'compression_ratio': 0.3,    # Razão de compressão
    },

    'rag': {
        'chunk_size': 512,           # Tamanho dos chunks
        'overlap': 50,               # Sobreposição entre chunks
    }
}
```

## 🧪 Testar Instalação

```bash
# Verifica se todos os módulos NLP estão funcionando
TESTAR_NLP.bat
```

## 📊 Estatísticas de Performance

| Modo | Tempo/Doc | Memória RAM | CPU |
|------|-----------|-------------|-----|
| Rápido | 1-2s | ~200MB | Baixo |
| Padrão | 5-10s | ~500MB | Médio |
| Completo | 15-30s | ~2GB | Alto |

## 🎓 Casos de Uso

### 1. Pesquisa Jurídica
- Extração automática de jurisprudências
- Identificação de súmulas e precedentes
- Análise de argumentos

### 2. Escritórios de Advocacia
- Organização de acervo documental
- Busca semântica em processos
- Geração de resumos executivos

### 3. Tribunais
- Catalogação de decisões
- Extração de teses fixadas
- Análise estatística de julgamentos

### 4. Sistemas de IA (RAG)
- Base de conhecimento vetorizada
- Busca semântica eficiente
- Contexto estruturado para LLMs

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **spaCy** - NLP para português
- **Flair** - NER contextualizado
- **Transformers** - Modelos de linguagem
- **PyTorch** - Deep learning
- **Sentence-Transformers** - Embeddings
- **FAISS** - Busca vetorial
- **PyPDF** - Extração de PDF
- **pdfplumber** - Análise avançada de PDF

## 📚 Modelos Suportados

### Embeddings
- `paraphrase-multilingual-mpnet-base-v2` (padrão)
- Qualquer modelo Sentence-Transformers

### Sumarização
- Sumarização extrativa (sem dependências)
- `unicamp-dl/ptt5-base-portuguese-vocab`
- `facebook/mbart-large-50`

### NER
- spaCy `pt_core_news_lg` / `pt_core_news_sm`
- Modelos Flair para português

## 🤝 Contribuindo

Este é um sistema em constante evolução. Sugestões e melhorias são bem-vindas!

## 📄 Licença

Desenvolvido com Claude AI para fins educacionais e profissionais.

## 📞 Suporte

Para problemas ou dúvidas:
1. Verifique se todas as dependências estão instaladas
2. Execute `TESTAR_NLP.bat` para diagnosticar
3. Consulte a documentação em `config.py`

## 🔄 Histórico de Versões

### v2.0.0 (2024-10)
- ✅ Sistema completo de NLP jurídico
- ✅ Extração de entidades especializadas
- ✅ Sumarização inteligente
- ✅ Preparação para RAG
- ✅ Classificação de documentos

### v1.0.0 (2024-10)
- ✅ Extração básica de texto
- ✅ Conversão para JSON
- ✅ Suporte a PDF e TXT

---

**🧠 Sistema de IA Jurídica - Estrategista Jurídico-Cognitivo v2.0**

*Transformando documentos jurídicos em conhecimento estruturado para IA*
