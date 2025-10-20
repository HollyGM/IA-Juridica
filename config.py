"""
Arquivo de configuração para o sistema de IA jurídica
Personalize as configurações conforme suas necessidades
"""

# ============================================================
# CONFIGURAÇÕES DE PROCESSAMENTO NLP
# ============================================================

NLP_CONFIG = {
    # Ativa ou desativa módulos NLP
    'enable_ner': True,  # Extração de Entidades Nomeadas
    'enable_summarization': True,  # Sumarização de textos
    'enable_embeddings': False,  # Embeddings para RAG (requer mais recursos)

    # Modelos a serem utilizados
    'models': {
        'embedding_model': 'sentence-transformers/paraphrase-multilingual-mpnet-base-v2',
        'summarization_model': None,  # None = usa sumarização extrativa
        'spacy_model': 'pt_core_news_lg',  # ou 'pt_core_news_sm'
    },

    # Configurações de sumarização
    'summarization': {
        'max_length': 500,  # Comprimento máximo do resumo (palavras)
        'min_length': 100,  # Comprimento mínimo do resumo (palavras)
        'compression_ratio': 0.3,  # Razão de compressão (0.0 a 1.0)
        'method': 'auto',  # 'extractive', 'abstractive', ou 'auto'
    },

    # Configurações RAG
    'rag': {
        'chunk_size': 512,  # Tamanho dos chunks (tokens/palavras)
        'overlap': 50,  # Sobreposição entre chunks
        'create_faiss_index': False,  # Criar índice FAISS (requer mais memória)
    }
}

# ============================================================
# CONFIGURAÇÕES DE EXTRAÇÃO DE TEXTO
# ============================================================

EXTRACTION_CONFIG = {
    # Extensões de arquivo suportadas
    'supported_extensions': ['.txt', '.pdf', '.doc', '.docx'],

    # Configurações de PDF
    'pdf': {
        'extract_images': False,  # Extrair texto de imagens (OCR)
        'preserve_layout': True,  # Preservar layout do documento
    },

    # Codificações a tentar para arquivos TXT
    'txt_encodings': [
        'utf-8',
        'utf-8-sig',
        'latin-1',
        'cp1252',
        'iso-8859-1'
    ]
}

# ============================================================
# CONFIGURAÇÕES DE OUTPUT JSON
# ============================================================

JSON_CONFIG = {
    # Tamanho máximo por arquivo JSON (MB)
    'max_size_mb': 50,

    # Indentação do JSON (2 = mais legível, None = mais compacto)
    'indent': 2,

    # Incluir estatísticas detalhadas
    'include_statistics': True,

    # Incluir índices de busca
    'create_indices': True,

    # Estrutura de dados
    'schema_version': '2.0',  # Versão do schema com suporte a NLP
}

# ============================================================
# CONFIGURAÇÕES DE PERFORMANCE
# ============================================================

PERFORMANCE_CONFIG = {
    # Número de documentos a processar em paralelo
    'batch_size': 10,

    # Limite de memória (MB) - ajuste conforme seu sistema
    'memory_limit_mb': 4096,

    # Modo de processamento
    'processing_mode': 'standard',  # 'fast', 'standard', 'thorough'

    # Verbose output
    'verbose': True,
}

# ============================================================
# CONFIGURAÇÕES ESPECÍFICAS PARA DOMÍNIO JURÍDICO
# ============================================================

LEGAL_CONFIG = {
    # Áreas do direito a detectar
    'areas_direito': [
        'civil',
        'penal',
        'trabalhista',
        'tributario',
        'constitucional',
        'administrativo',
        'empresarial',
        'consumidor'
    ],

    # Tipos de documentos jurídicos
    'tipos_documento': [
        'acordao',
        'sentenca',
        'peticao',
        'parecer',
        'decisao',
        'despacho',
        'contrato',
        'lei'
    ],

    # Tribunais brasileiros
    'tribunais': [
        'STF', 'STJ', 'TST', 'TSE', 'STM',
        'TRF', 'TRT', 'TRE', 'TJ'
    ]
}

# ============================================================
# MODO RÁPIDO (Para testes e desenvolvimento)
# ============================================================

FAST_MODE_CONFIG = {
    'enable_ner': True,
    'enable_summarization': False,
    'enable_embeddings': False,
    'rag': {
        'chunk_size': 256,
        'overlap': 25,
        'create_faiss_index': False,
    }
}

# ============================================================
# MODO COMPLETO (Análise profunda com todos os recursos)
# ============================================================

FULL_MODE_CONFIG = {
    'enable_ner': True,
    'enable_summarization': True,
    'enable_embeddings': True,
    'rag': {
        'chunk_size': 512,
        'overlap': 50,
        'create_faiss_index': True,
    }
}


# ============================================================
# FUNÇÃO HELPER PARA SELECIONAR CONFIGURAÇÃO
# ============================================================

def get_config(mode: str = 'standard') -> dict:
    """
    Retorna configuração baseada no modo selecionado

    Args:
        mode: 'fast', 'standard', ou 'full'

    Returns:
        Dicionário de configuração
    """
    if mode == 'fast':
        return FAST_MODE_CONFIG
    elif mode == 'full':
        return FULL_MODE_CONFIG
    else:
        return NLP_CONFIG


# ============================================================
# INFORMAÇÕES DO SISTEMA
# ============================================================

SYSTEM_INFO = {
    'name': 'Sistema de IA Jurídica - Estrategista Jurídico-Cognitivo',
    'version': '2.0.0',
    'description': 'Sistema avançado de processamento de documentos jurídicos com NLP e RAG',
    'author': 'Desenvolvido com Claude',
    'features': [
        'Extração de texto de PDF, TXT e DOC',
        'Reconhecimento de Entidades Nomeadas (NER) jurídicas',
        'Sumarização automática de documentos',
        'Análise estrutural de argumentos e teses',
        'Classificação de documentos jurídicos',
        'Preparação para sistemas RAG',
        'Indexação vetorial com FAISS',
        'Chunking inteligente com sobreposição',
        'Export para JSON otimizado'
    ]
}


if __name__ == '__main__':
    """Exibe informações de configuração"""
    import json

    print("=" * 60)
    print(f"  {SYSTEM_INFO['name']}")
    print(f"  Versão {SYSTEM_INFO['version']}")
    print("=" * 60)
    print("\nRecursos disponíveis:")
    for feature in SYSTEM_INFO['features']:
        print(f"  ✓ {feature}")

    print("\n" + "=" * 60)
    print("Configurações disponíveis:")
    print("=" * 60)

    print("\n📊 Configuração PADRÃO:")
    print(json.dumps(NLP_CONFIG, indent=2, ensure_ascii=False))

    print("\n⚡ Configuração RÁPIDA (para testes):")
    print(json.dumps(FAST_MODE_CONFIG, indent=2, ensure_ascii=False))

    print("\n🚀 Configuração COMPLETA (análise profunda):")
    print(json.dumps(FULL_MODE_CONFIG, indent=2, ensure_ascii=False))
