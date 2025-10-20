"""
Módulo para geração de JSON otimizado para modelos de IA
Versão 2.0 - Com suporte a análise NLP e estrutura RAG
"""

import json
from datetime import datetime
from typing import Dict, Any, List, Optional


def generate_knowledge_base_json(documents, metadata=None, include_nlp=True):
    """
    Gera estrutura JSON otimizada para uso em modelos de IA

    Args:
        documents: Lista de documentos processados
        metadata: Metadados adicionais (opcional)
        include_nlp: Se True, inclui análise NLP nos documentos

    Returns:
        dict: Estrutura de dados pronta para serialização JSON
    """
    if metadata is None:
        metadata = {}

    # Calcula estatísticas gerais
    stats = {
        "total_documents": len(documents),
        "total_characters": sum(doc.get('char_count', 0) for doc in documents),
        "total_words": sum(doc.get('word_count', 0) for doc in documents)
    }

    # Estatísticas de NLP se disponível
    if include_nlp:
        nlp_stats = calculate_nlp_statistics(documents)
        stats['nlp_analysis'] = nlp_stats

    knowledge_base = {
        "schema_version": "2.0",  # Nova versão com suporte NLP
        "generated_at": datetime.now().isoformat(),
        "system": {
            "name": "Sistema de IA Jurídica - Estrategista Jurídico-Cognitivo",
            "version": "2.0.0",
            "features": ["NER", "Sumarização", "RAG", "Classificação"]
        },
        "metadata": metadata,
        "statistics": stats,
        "documents": documents
    }

    return knowledge_base


def calculate_nlp_statistics(documents: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calcula estatísticas de análise NLP dos documentos

    Args:
        documents: Lista de documentos com análise NLP

    Returns:
        Estatísticas agregadas de NLP
    """
    stats = {
        "documents_with_nlp": 0,
        "total_entities": 0,
        "documents_with_summary": 0,
        "entity_types": {},
        "document_types": {},
        "legal_areas": {}
    }

    for doc in documents:
        nlp = doc.get('nlp_analysis', {})

        if nlp:
            stats['documents_with_nlp'] += 1

            # Conta entidades
            entities = nlp.get('entidades', {})
            for entity_type, entity_list in entities.items():
                if entity_list:
                    stats['total_entities'] += len(entity_list)
                    if entity_type not in stats['entity_types']:
                        stats['entity_types'][entity_type] = 0
                    stats['entity_types'][entity_type] += len(entity_list)

            # Conta documentos com resumo
            if nlp.get('sumarizacao', {}).get('resumo'):
                stats['documents_with_summary'] += 1

            # Conta tipos de documento
            classification = nlp.get('classificacao', {})
            doc_type = classification.get('tipo_documento', 'desconhecido')
            if doc_type not in stats['document_types']:
                stats['document_types'][doc_type] = 0
            stats['document_types'][doc_type] += 1

            # Conta áreas do direito
            areas = classification.get('area_direito', [])
            for area in areas:
                if area not in stats['legal_areas']:
                    stats['legal_areas'][area] = 0
                stats['legal_areas'][area] += 1

    return stats


def optimize_for_ai_model(knowledge_base, model_type="general"):
    """
    Otimiza a estrutura JSON para modelos específicos de IA

    Args:
        knowledge_base: Base de conhecimento base
        model_type: Tipo de modelo ('general', 'claude', 'gpt', 'gemini')

    Returns:
        dict: Estrutura otimizada
    """
    optimized = knowledge_base.copy()

    if model_type == "claude":
        # Claude prefere contexto estruturado com marcadores claros
        for doc in optimized.get('documents', []):
            doc['context_markers'] = {
                'source': doc.get('filename', ''),
                'path': doc.get('relative_path', ''),
                'type': doc.get('type', '')
            }

    elif model_type == "gpt":
        # GPT se beneficia de chunking para contextos longos
        optimized['chunking_strategy'] = 'sliding_window'
        optimized['max_chunk_size'] = 4000

    elif model_type == "gemini":
        # Gemini aprecia hierarquia clara
        optimized['hierarchical_structure'] = True

    return optimized


def split_large_json(knowledge_base, max_size_mb=50):
    """
    Divide um JSON grande em múltiplos arquivos se necessário

    Esta função calcula o tamanho real de cada parte e garante que nenhuma
    ultrapasse o limite especificado.

    Args:
        knowledge_base: Base de conhecimento completa
        max_size_mb: Tamanho máximo em MB por arquivo

    Returns:
        list: Lista de dicionários (cada um será um arquivo JSON separado)
    """
    # Converte MB para bytes
    max_size_bytes = max_size_mb * 1024 * 1024

    # Verifica o tamanho do JSON completo
    json_str = json.dumps(knowledge_base, ensure_ascii=False, indent=2)
    total_size_bytes = len(json_str.encode('utf-8'))

    if total_size_bytes <= max_size_bytes:
        # Não precisa dividir
        return [knowledge_base]

    # Prepara os metadados base (compartilhados por todas as partes)
    base_metadata = {
        "schema_version": knowledge_base.get("schema_version", "1.0"),
        "generated_at": knowledge_base.get("generated_at"),
        "metadata": knowledge_base.get("metadata", {})
    }

    # Calcula o tamanho dos metadados base
    metadata_size = len(json.dumps(base_metadata, ensure_ascii=False, indent=2).encode('utf-8'))

    # Calcula quanto espaço resta para documentos em cada arquivo
    available_space = max_size_bytes - metadata_size - 500  # 500 bytes de margem de segurança

    documents = knowledge_base.get('documents', [])
    total_docs = len(documents)

    result = []
    current_chunk = []
    current_size = 0

    for doc in documents:
        # Calcula o tamanho do documento
        doc_json = json.dumps(doc, ensure_ascii=False, indent=2)
        doc_size = len(doc_json.encode('utf-8'))

        # Verifica se adicionar este documento excederia o limite
        if current_size + doc_size > available_space and current_chunk:
            # Salva o chunk atual
            result.append(current_chunk)
            current_chunk = []
            current_size = 0

        # Adiciona o documento ao chunk atual
        current_chunk.append(doc)
        current_size += doc_size

    # Adiciona o último chunk se houver documentos
    if current_chunk:
        result.append(current_chunk)

    # Cria as estruturas finais com metadados completos
    final_result = []
    num_parts = len(result)

    for i, doc_chunk in enumerate(result):
        chunk_data = {
            "schema_version": base_metadata.get("schema_version", "1.0"),
            "generated_at": base_metadata.get("generated_at"),
            "part_info": {
                "current_part": i + 1,
                "total_parts": num_parts,
                "part_label": f"parte_{i+1}_de_{num_parts}"
            },
            "metadata": base_metadata.get("metadata", {}),
            "statistics": {
                "documents_in_this_part": len(doc_chunk),
                "total_documents_all_parts": total_docs,
                "total_characters_this_part": sum(doc.get('char_count', 0) for doc in doc_chunk),
                "total_words_this_part": sum(doc.get('word_count', 0) for doc in doc_chunk)
            },
            "documents": doc_chunk
        }

        final_result.append(chunk_data)

    return final_result


def create_index(knowledge_base):
    """
    Cria um índice para facilitar buscas na base de conhecimento

    Args:
        knowledge_base: Base de conhecimento

    Returns:
        dict: Índice estruturado
    """
    index = {
        "by_type": {},
        "by_directory": {},
        "by_filename": {}
    }

    for doc in knowledge_base.get('documents', []):
        doc_id = doc.get('id')
        doc_type = doc.get('type', 'unknown')
        directory = doc.get('relative_path', '').rsplit('/', 1)[0] if '/' in doc.get('relative_path', '') else 'root'
        filename = doc.get('filename', '')

        # Índice por tipo
        if doc_type not in index['by_type']:
            index['by_type'][doc_type] = []
        index['by_type'][doc_type].append(doc_id)

        # Índice por diretório
        if directory not in index['by_directory']:
            index['by_directory'][directory] = []
        index['by_directory'][directory].append(doc_id)

        # Índice por nome de arquivo
        index['by_filename'][filename] = doc_id

    return index
