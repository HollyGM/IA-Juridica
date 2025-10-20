"""
Módulo principal de processamento NLP para documentos jurídicos
Integra todos os componentes: NER, Sumarização e preparação para RAG
Implementa a metodologia "Estrategista Jurídico-Cognitivo"
"""

from typing import Dict, Any, List, Optional
import warnings
warnings.filterwarnings('ignore')

from .legal_ner import LegalEntityExtractor, extract_legal_entities
from .legal_summarizer import LegalSummarizer, summarize_legal_text
from .rag_indexer import RAGIndexer


class LegalNLPProcessor:
    """
    Processador NLP completo para documentos jurídicos brasileiros
    Aplica análise cognitiva e estruturação para sistemas RAG
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializa o processador NLP

        Args:
            config: Configurações personalizadas
        """
        self.config = config or {}

        # Componentes NLP
        self.entity_extractor = LegalEntityExtractor()
        self.summarizer = LegalSummarizer()
        self.rag_indexer = RAGIndexer()

        # Configurações
        self.enable_ner = self.config.get('enable_ner', True)
        self.enable_summarization = self.config.get('enable_summarization', True)
        self.enable_embeddings = self.config.get('enable_embeddings', False)

        print("\n" + "=" * 60)
        print("  🧠 PROCESSADOR NLP JURÍDICO INICIALIZADO")
        print("  Metodologia: Estrategista Jurídico-Cognitivo")
        print("=" * 60)
        print(f"  ✓ Extração de Entidades (NER): {'Ativo' if self.enable_ner else 'Desativado'}")
        print(f"  ✓ Sumarização: {'Ativo' if self.enable_summarization else 'Desativado'}")
        print(f"  ✓ Embeddings para RAG: {'Ativo' if self.enable_embeddings else 'Desativado'}")
        print("=" * 60 + "\n")

    def process_document(self, document: Dict[str, Any], doc_index: int) -> Dict[str, Any]:
        """
        Processa um único documento com análise NLP completa

        Args:
            document: Documento com conteúdo extraído
            doc_index: Índice do documento

        Returns:
            Documento enriquecido com análise NLP
        """
        content = document.get('content', '')
        doc_id = document.get('id', f'doc_{doc_index}')

        print(f"  [{doc_index}] Processando NLP: {document.get('filename', 'N/A')}")

        # Inicializa estrutura de análise NLP
        nlp_analysis = {
            'entidades': {},
            'sumarizacao': {},
            'analise_estrutural': {},
            'classificacao': {},
            'metricas': {}
        }

        try:
            # 1. Extração de Entidades Nomeadas (NER)
            if self.enable_ner and len(content) > 50:
                print(f"      → Extraindo entidades jurídicas...")
                entities_data = extract_legal_entities(content)

                nlp_analysis['entidades'] = entities_data['entidades']
                nlp_analysis['analise_estrutural'] = entities_data['analise_estrutural']
                nlp_analysis['metricas']['total_entidades'] = entities_data['estatisticas']['total_entidades']

            # 2. Sumarização
            if self.enable_summarization and len(content.split()) > 100:
                print(f"      → Gerando sumarização...")
                summary_data = summarize_legal_text(content, max_length=500)

                nlp_analysis['sumarizacao'] = {
                    'resumo': summary_data['summary'],
                    'metodo': summary_data['method'],
                    'pontos_chave': summary_data['key_points'],
                    'secoes': summary_data['sections'],
                    'taxa_compressao': summary_data['compression_ratio']
                }

            # 3. Classificação de Documento
            print(f"      → Classificando documento...")
            classification = self._classify_document(content)
            nlp_analysis['classificacao'] = classification

            # 4. Análise de Sentimento/Decisão
            decision_analysis = self._analyze_decision(content)
            nlp_analysis['analise_decisao'] = decision_analysis

            # 5. Métricas de complexidade
            complexity = self._calculate_complexity(content)
            nlp_analysis['metricas']['complexidade'] = complexity

            print(f"      ✓ NLP concluído")

        except Exception as e:
            print(f"      ⚠ Erro no processamento NLP: {str(e)}")
            nlp_analysis['erro'] = str(e)

        # Adiciona análise NLP ao documento
        document['nlp_analysis'] = nlp_analysis

        return document

    def _classify_document(self, content: str) -> Dict[str, Any]:
        """
        Classifica o tipo e natureza do documento jurídico

        Args:
            content: Conteúdo do documento

        Returns:
            Classificação do documento
        """
        classification = {
            'tipo_documento': 'desconhecido',
            'natureza': [],
            'area_direito': [],
            'confianca': 0.0
        }

        content_lower = content.lower()

        # Tipos de documento
        doc_types = {
            'acordao': ['acórdão', 'acordão', 'voto', 'relator'],
            'sentenca': ['sentença', 'julgo procedente', 'julgo improcedente'],
            'peticao': ['petição', 'requer', 'excelentíssimo'],
            'parecer': ['parecer', 'opina', 'manifesta-se'],
            'decisao': ['decisão', 'defiro', 'indefiro'],
            'despacho': ['despacho', 'vista', 'manifeste-se']
        }

        for doc_type, keywords in doc_types.items():
            if any(kw in content_lower for kw in keywords):
                classification['tipo_documento'] = doc_type
                break

        # Áreas do direito
        areas = {
            'civil': ['direito civil', 'obrigação', 'contrato', 'responsabilidade civil'],
            'penal': ['direito penal', 'crime', 'pena', 'código penal', 'condenação'],
            'trabalhista': ['trabalhista', 'clt', 'empregado', 'empregador', 'rescisão'],
            'tributario': ['tributário', 'imposto', 'tributo', 'icms', 'irpf'],
            'constitucional': ['constitucional', 'constituição', 'stf', 'adi', 'adpf'],
            'administrativo': ['administrativo', 'servidor público', 'licitação']
        }

        for area, keywords in areas.items():
            if any(kw in content_lower for kw in keywords):
                classification['area_direito'].append(area)

        return classification

    def _analyze_decision(self, content: str) -> Dict[str, Any]:
        """
        Analisa a decisão judicial (se aplicável)

        Args:
            content: Conteúdo do documento

        Returns:
            Análise da decisão
        """
        decision = {
            'tipo': 'nao_aplicavel',
            'resultado': None,
            'fundamentacao_principal': []
        }

        content_lower = content.lower()

        # Detecta tipo de decisão
        if any(term in content_lower for term in ['julgo procedente', 'dou provimento', 'acordam em dar provimento']):
            decision['tipo'] = 'procedente'
            decision['resultado'] = 'favoravel_autor'

        elif any(term in content_lower for term in ['julgo improcedente', 'nego provimento', 'acordam em negar']):
            decision['tipo'] = 'improcedente'
            decision['resultado'] = 'favoravel_reu'

        elif 'parcialmente procedente' in content_lower:
            decision['tipo'] = 'parcialmente_procedente'
            decision['resultado'] = 'parcial'

        return decision

    def _calculate_complexity(self, content: str) -> Dict[str, Any]:
        """
        Calcula métricas de complexidade do texto jurídico

        Args:
            content: Conteúdo do documento

        Returns:
            Métricas de complexidade
        """
        words = content.split()
        sentences = content.split('.')

        complexity = {
            'total_palavras': len(words),
            'total_sentencas': len(sentences),
            'media_palavras_sentenca': len(words) / max(len(sentences), 1),
            'palavras_complexas': 0,
            'nivel': 'simples'
        }

        # Conta palavras complexas (> 10 caracteres)
        complexity['palavras_complexas'] = sum(1 for w in words if len(w) > 10)

        # Define nível de complexidade
        avg_words = complexity['media_palavras_sentenca']
        if avg_words > 30:
            complexity['nivel'] = 'muito_complexo'
        elif avg_words > 20:
            complexity['nivel'] = 'complexo'
        elif avg_words > 15:
            complexity['nivel'] = 'medio'

        return complexity

    def process_batch(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Processa um lote de documentos

        Args:
            documents: Lista de documentos

        Returns:
            Lista de documentos processados
        """
        print(f"\n🔄 Iniciando processamento NLP de {len(documents)} documentos...")

        processed_docs = []

        for idx, doc in enumerate(documents, 1):
            processed_doc = self.process_document(doc, idx)
            processed_docs.append(processed_doc)

        print(f"✓ Processamento NLP concluído para {len(processed_docs)} documentos\n")

        return processed_docs

    def create_rag_index(
        self,
        documents: List[Dict[str, Any]],
        chunk_size: int = 512,
        overlap: int = 50
    ) -> Dict[str, Any]:
        """
        Cria índice RAG a partir dos documentos processados

        Args:
            documents: Documentos processados
            chunk_size: Tamanho dos chunks
            overlap: Sobreposição

        Returns:
            Dataset RAG indexado
        """
        print("\n🔄 Criando índice RAG...")

        rag_dataset = self.rag_indexer.prepare_rag_dataset(
            documents,
            chunk_size=chunk_size,
            overlap=overlap,
            create_embeddings=self.enable_embeddings
        )

        print("✓ Índice RAG criado com sucesso\n")

        return rag_dataset


def process_legal_documents(
    documents: List[Dict[str, Any]],
    config: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """
    Função helper para processar documentos jurídicos

    Args:
        documents: Lista de documentos
        config: Configurações

    Returns:
        Documentos processados com análise NLP
    """
    processor = LegalNLPProcessor(config)
    return processor.process_batch(documents)
