"""
Módulo para indexação e vetorização de documentos jurídicos para sistemas RAG
Prepara os dados para Recuperação Aumentada por Geração (Retrieval-Augmented Generation)
"""

import json
import numpy as np
from typing import List, Dict, Any, Optional
import warnings
warnings.filterwarnings('ignore')


class RAGIndexer:
    """
    Indexador de documentos para sistemas RAG
    Cria embeddings e estruturas de busca eficientes
    """

    def __init__(self, embedding_model: str = 'sentence-transformers/paraphrase-multilingual-mpnet-base-v2'):
        """
        Inicializa o indexador

        Args:
            embedding_model: Nome do modelo de embeddings
        """
        self.embedding_model_name = embedding_model
        self.model = None
        self.index = None
        self.initialized = False
        self.use_embeddings = False

    def initialize_model(self):
        """Inicializa modelo de embeddings"""
        if self.initialized:
            return

        try:
            from sentence_transformers import SentenceTransformer

            print(f"Carregando modelo de embeddings: {self.embedding_model_name}")
            self.model = SentenceTransformer(self.embedding_model_name)
            self.use_embeddings = True
            print("✓ Modelo de embeddings carregado com sucesso")

        except ImportError:
            print("⚠ sentence-transformers não instalado. Indexação sem embeddings.")
            self.use_embeddings = False
        except Exception as e:
            print(f"⚠ Erro ao carregar modelo: {str(e)}")
            self.use_embeddings = False

        self.initialized = True

    def create_chunks(
        self,
        text: str,
        chunk_size: int = 512,
        overlap: int = 50,
        metadata: Optional[Dict] = None
    ) -> List[Dict[str, Any]]:
        """
        Divide texto em chunks sobrepostos para RAG

        Args:
            text: Texto a ser dividido
            chunk_size: Tamanho máximo de cada chunk (em tokens/palavras)
            overlap: Sobreposição entre chunks
            metadata: Metadados a adicionar a cada chunk

        Returns:
            Lista de chunks com metadados
        """
        words = text.split()
        chunks = []

        if len(words) <= chunk_size:
            # Se o texto é pequeno, retorna como um único chunk
            chunks.append({
                'text': text,
                'chunk_id': 0,
                'start_word': 0,
                'end_word': len(words),
                'metadata': metadata or {}
            })
            return chunks

        # Cria chunks sobrepostos
        start = 0
        chunk_id = 0

        while start < len(words):
            end = min(start + chunk_size, len(words))
            chunk_words = words[start:end]
            chunk_text = ' '.join(chunk_words)

            chunks.append({
                'text': chunk_text,
                'chunk_id': chunk_id,
                'start_word': start,
                'end_word': end,
                'metadata': metadata or {}
            })

            chunk_id += 1
            start += (chunk_size - overlap)

        return chunks

    def create_embeddings(self, texts: List[str]) -> Optional[np.ndarray]:
        """
        Cria embeddings vetoriais para lista de textos

        Args:
            texts: Lista de textos

        Returns:
            Array numpy com embeddings ou None
        """
        if not self.initialized:
            self.initialize_model()

        if not self.use_embeddings:
            return None

        try:
            embeddings = self.model.encode(
                texts,
                show_progress_bar=True,
                batch_size=32
            )
            return embeddings

        except Exception as e:
            print(f"⚠ Erro ao criar embeddings: {str(e)}")
            return None

    def create_faiss_index(self, embeddings: np.ndarray) -> Optional[Any]:
        """
        Cria índice FAISS para busca rápida

        Args:
            embeddings: Array de embeddings

        Returns:
            Índice FAISS ou None
        """
        try:
            import faiss

            dimension = embeddings.shape[1]
            index = faiss.IndexFlatL2(dimension)
            index.add(embeddings.astype('float32'))

            print(f"✓ Índice FAISS criado com {embeddings.shape[0]} vetores")
            return index

        except ImportError:
            print("⚠ FAISS não instalado. Busca vetorial não disponível.")
            return None
        except Exception as e:
            print(f"⚠ Erro ao criar índice FAISS: {str(e)}")
            return None

    def prepare_rag_dataset(
        self,
        documents: List[Dict[str, Any]],
        chunk_size: int = 512,
        overlap: int = 50,
        create_embeddings: bool = True
    ) -> Dict[str, Any]:
        """
        Prepara dataset completo para RAG

        Args:
            documents: Lista de documentos processados
            chunk_size: Tamanho dos chunks
            overlap: Sobreposição entre chunks
            create_embeddings: Se True, cria embeddings

        Returns:
            Dataset preparado para RAG
        """
        print("\n🔄 Preparando dataset para RAG...")

        all_chunks = []
        chunk_to_doc_map = []

        # Processa cada documento
        for doc_idx, doc in enumerate(documents):
            doc_id = doc.get('id', f'doc_{doc_idx}')
            content = doc.get('content', '')

            # Cria metadados do documento
            metadata = {
                'doc_id': doc_id,
                'filename': doc.get('filename', ''),
                'type': doc.get('type', ''),
                'relative_path': doc.get('relative_path', '')
            }

            # Se houver dados de NLP, adiciona aos metadados
            if 'nlp_analysis' in doc:
                nlp = doc['nlp_analysis']
                metadata['has_entities'] = len(nlp.get('entidades', {})) > 0
                metadata['has_summary'] = 'summary' in nlp.get('sumarizacao', {})

            # Cria chunks do documento
            doc_chunks = self.create_chunks(
                content,
                chunk_size=chunk_size,
                overlap=overlap,
                metadata=metadata
            )

            # Adiciona chunks e mapeia para o documento original
            for chunk in doc_chunks:
                chunk['global_chunk_id'] = len(all_chunks)
                chunk_to_doc_map.append(doc_idx)
                all_chunks.append(chunk)

        print(f"✓ Criados {len(all_chunks)} chunks de {len(documents)} documentos")

        # Cria embeddings se solicitado
        embeddings = None
        faiss_index = None

        if create_embeddings and self.use_embeddings:
            print("\n🔄 Criando embeddings...")
            chunk_texts = [chunk['text'] for chunk in all_chunks]
            embeddings = self.create_embeddings(chunk_texts)

            if embeddings is not None:
                # Salva embeddings como lista para JSON
                embeddings_list = embeddings.tolist()

                # Cria índice FAISS
                faiss_index = self.create_faiss_index(embeddings)
        else:
            print("⚠ Embeddings não criados (modelo não disponível ou desabilitado)")
            embeddings_list = None

        # Monta estrutura final
        rag_dataset = {
            'chunks': all_chunks,
            'chunk_to_doc_map': chunk_to_doc_map,
            'embeddings': embeddings_list,
            'config': {
                'chunk_size': chunk_size,
                'overlap': overlap,
                'embedding_model': self.embedding_model_name if self.use_embeddings else None,
                'total_chunks': len(all_chunks),
                'total_documents': len(documents)
            }
        }

        # Adiciona estatísticas
        rag_dataset['statistics'] = {
            'avg_chunk_length': np.mean([len(c['text'].split()) for c in all_chunks]),
            'min_chunk_length': min([len(c['text'].split()) for c in all_chunks]),
            'max_chunk_length': max([len(c['text'].split()) for c in all_chunks]),
            'total_chunks': len(all_chunks)
        }

        print("✓ Dataset RAG preparado com sucesso")

        return rag_dataset

    def create_inverted_index(self, documents: List[Dict[str, Any]]) -> Dict[str, List[int]]:
        """
        Cria índice invertido para busca por palavras-chave

        Args:
            documents: Lista de documentos

        Returns:
            Índice invertido {palavra: [doc_ids]}
        """
        inverted_index = {}

        for doc_idx, doc in enumerate(documents):
            content = doc.get('content', '').lower()
            words = set(content.split())

            for word in words:
                # Remove pontuação
                word = ''.join(c for c in word if c.isalnum())
                if len(word) > 3:  # Ignora palavras muito curtas
                    if word not in inverted_index:
                        inverted_index[word] = []
                    inverted_index[word].append(doc_idx)

        return inverted_index


def prepare_for_rag(
    documents: List[Dict[str, Any]],
    chunk_size: int = 512,
    create_embeddings: bool = True
) -> Dict[str, Any]:
    """
    Função helper para preparar documentos para RAG

    Args:
        documents: Lista de documentos
        chunk_size: Tamanho dos chunks
        create_embeddings: Se True, cria embeddings

    Returns:
        Dataset preparado para RAG
    """
    indexer = RAGIndexer()
    return indexer.prepare_rag_dataset(
        documents,
        chunk_size=chunk_size,
        create_embeddings=create_embeddings
    )
