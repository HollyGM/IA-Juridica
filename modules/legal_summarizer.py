"""
Módulo para sumarização de textos jurídicos em português
Usa técnicas extrativas e abstrativas quando modelos estão disponíveis
"""

import re
from typing import List, Dict, Any, Optional
import warnings
warnings.filterwarnings('ignore')


class LegalSummarizer:
    """
    Sumarizador especializado em textos jurídicos brasileiros
    """

    def __init__(self, model_name: Optional[str] = None):
        """
        Inicializa o sumarizador

        Args:
            model_name: Nome do modelo transformers a usar (opcional)
        """
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.initialized = False
        self.use_ml_model = False

    def initialize_model(self):
        """Inicializa modelo de sumarização se disponível"""
        if self.initialized:
            return

        try:
            from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

            # Tenta carregar modelo específico para português jurídico
            models_to_try = [
                self.model_name,
                'unicamp-dl/ptt5-base-portuguese-vocab',  # Modelo T5 em português
                'facebook/mbart-large-50',  # MBART multilíngue
            ]

            for model_name in models_to_try:
                if model_name is None:
                    continue
                try:
                    print(f"Tentando carregar modelo: {model_name}")
                    self.summarizer = pipeline(
                        "summarization",
                        model=model_name,
                        tokenizer=model_name
                    )
                    self.use_ml_model = True
                    print(f"✓ Modelo {model_name} carregado com sucesso")
                    break
                except Exception as e:
                    print(f"⚠ Não foi possível carregar {model_name}: {str(e)}")
                    continue

            if not self.use_ml_model:
                print("⚠ Nenhum modelo de sumarização ML disponível. Usando sumarização extrativa.")

        except ImportError:
            print("⚠ Transformers não instalado. Usando apenas sumarização extrativa.")
            self.use_ml_model = False

        self.initialized = True

    def summarize(
        self,
        text: str,
        max_length: int = 500,
        min_length: int = 100,
        ratio: float = 0.3,
        method: str = 'auto'
    ) -> Dict[str, Any]:
        """
        Sumariza texto jurídico

        Args:
            text: Texto a ser sumarizado
            max_length: Comprimento máximo do resumo (em palavras)
            min_length: Comprimento mínimo do resumo (em palavras)
            ratio: Razão de compressão (0.0 a 1.0)
            method: 'extractive', 'abstractive' ou 'auto'

        Returns:
            Dicionário com resumo e metadados
        """
        if not self.initialized:
            self.initialize_model()

        # Decide o método
        if method == 'auto':
            method = 'abstractive' if self.use_ml_model else 'extractive'

        # Pré-processa o texto
        text_clean = self._preprocess_text(text)

        if method == 'abstractive' and self.use_ml_model:
            summary = self._summarize_abstractive(text_clean, max_length, min_length)
            summary_method = 'abstractive_ml'
        else:
            summary = self._summarize_extractive(text_clean, ratio, max_length)
            summary_method = 'extractive'

        # Extrai pontos-chave
        key_points = self._extract_key_points(text_clean)

        # Identifica seções importantes
        sections = self._identify_sections(text)

        return {
            'summary': summary,
            'method': summary_method,
            'key_points': key_points,
            'sections': sections,
            'original_length': len(text.split()),
            'summary_length': len(summary.split()),
            'compression_ratio': len(summary.split()) / max(len(text.split()), 1)
        }

    def _preprocess_text(self, text: str) -> str:
        """Pré-processa o texto para sumarização"""
        # Remove múltiplos espaços
        text = re.sub(r'\s+', ' ', text)

        # Remove marcadores de página se existirem
        text = re.sub(r'---\s*Página\s+\d+\s*---', '', text)

        return text.strip()

    def _summarize_abstractive(
        self,
        text: str,
        max_length: int,
        min_length: int
    ) -> str:
        """Sumarização abstrativa usando modelo ML"""
        try:
            # Limita o tamanho do texto de entrada
            max_input = 1024
            words = text.split()
            if len(words) > max_input:
                text = ' '.join(words[:max_input])

            result = self.summarizer(
                text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False
            )

            return result[0]['summary_text']

        except Exception as e:
            print(f"⚠ Erro na sumarização abstrativa: {str(e)}")
            return self._summarize_extractive(text, 0.3, max_length)

    def _summarize_extractive(
        self,
        text: str,
        ratio: float,
        max_length: int
    ) -> str:
        """
        Sumarização extrativa baseada em scoring de sentenças
        Adaptado para textos jurídicos
        """
        # Divide em sentenças
        sentences = self._split_sentences(text)

        if len(sentences) <= 3:
            return text

        # Calcula scores para cada sentença
        scores = self._score_sentences(sentences, text)

        # Ordena sentenças por score
        ranked = sorted(
            enumerate(scores),
            key=lambda x: x[1],
            reverse=True
        )

        # Seleciona top sentenças mantendo ordem original
        num_sentences = max(3, int(len(sentences) * ratio))
        selected_indices = sorted([idx for idx, _ in ranked[:num_sentences]])

        # Constrói resumo
        summary_sentences = [sentences[i] for i in selected_indices]
        summary = ' '.join(summary_sentences)

        # Limita ao tamanho máximo
        words = summary.split()
        if len(words) > max_length:
            summary = ' '.join(words[:max_length]) + '...'

        return summary

    def _split_sentences(self, text: str) -> List[str]:
        """Divide texto em sentenças (adaptado para textos jurídicos)"""
        # Padrão para sentenças, considerando abreviações jurídicas
        pattern = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s'
        sentences = re.split(pattern, text)

        # Remove sentenças muito curtas
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]

        return sentences

    def _score_sentences(self, sentences: List[str], full_text: str) -> List[float]:
        """
        Calcula score de importância para cada sentença
        Baseado em: posição, palavras-chave jurídicas, comprimento
        """
        scores = []

        # Palavras-chave importantes no domínio jurídico
        keywords = {
            'decidiu', 'determinou', 'condenou', 'absolveu', 'julgou',
            'acordão', 'sentença', 'voto', 'fundamentação', 'dispositivo',
            'lei', 'artigo', 'jurisprudência', 'súmula', 'precedente',
            'tese', 'entendimento', 'decisão', 'provimento', 'recurso'
        }

        for i, sentence in enumerate(sentences):
            score = 0.0
            words = sentence.lower().split()

            # Score por posição (primeiras e últimas sentenças são importantes)
            if i < 3:
                score += 2.0
            elif i >= len(sentences) - 3:
                score += 1.5

            # Score por palavras-chave jurídicas
            keyword_count = sum(1 for word in words if word in keywords)
            score += keyword_count * 1.5

            # Score por comprimento (sentenças médias são preferidas)
            length = len(words)
            if 15 <= length <= 40:
                score += 1.0
            elif length > 40:
                score += 0.5

            # Score por presença de números (processos, leis, etc.)
            if re.search(r'\d+', sentence):
                score += 0.5

            # Score por presença de termos conclusivos
            conclusive_terms = ['portanto', 'assim', 'logo', 'consequentemente', 'conclui']
            if any(term in sentence.lower() for term in conclusive_terms):
                score += 1.0

            scores.append(score)

        return scores

    def _extract_key_points(self, text: str) -> List[str]:
        """Extrai pontos-chave do texto"""
        key_points = []

        # Marcadores de pontos importantes
        markers = [
            r'(?:decidiu|determinou|julgou)(?:\s+que)?\s+([^.]+\.)',
            r'(?:tese|entendimento|posicionamento)(?:\s+fixado)?\s*[:]\s*([^.]+\.)',
            r'(?:fundamentação|razões?)(?:\s+de\s+decidir)?\s*[:]\s*([^.]+\.)',
        ]

        for pattern in markers:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                point = match.group(1).strip()
                if len(point) > 20:
                    key_points.append(point)

        # Remove duplicatas
        key_points = list(dict.fromkeys(key_points))

        return key_points[:5]  # Retorna top 5

    def _identify_sections(self, text: str) -> Dict[str, str]:
        """Identifica seções estruturadas do documento jurídico"""
        sections = {}

        # Padrões de seções comuns
        section_patterns = {
            'ementa': r'EMENTA\s*[:]\s*([^\n]+(?:\n(?!\n)[^\n]+)*)',
            'relatorio': r'RELAT[ÓO]RIO\s*[:]\s*([^\n]+(?:\n(?!\n)[^\n]+)*)',
            'voto': r'VOTO\s*[:]\s*([^\n]+(?:\n(?!\n)[^\n]+)*)',
            'decisao': r'DECIS[ÃA]O\s*[:]\s*([^\n]+(?:\n(?!\n)[^\n]+)*)',
            'dispositivo': r'DISPOSITIVO\s*[:]\s*([^\n]+(?:\n(?!\n)[^\n]+)*)',
        }

        for section_name, pattern in section_patterns.items():
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                content = match.group(1).strip()
                # Limita o tamanho
                if len(content) > 500:
                    content = content[:500] + '...'
                sections[section_name] = content

        return sections


def summarize_legal_text(text: str, max_length: int = 500) -> Dict[str, Any]:
    """
    Função helper para sumarização rápida de texto jurídico

    Args:
        text: Texto jurídico
        max_length: Comprimento máximo do resumo

    Returns:
        Dicionário com resumo e análise
    """
    summarizer = LegalSummarizer()
    return summarizer.summarize(text, max_length=max_length)
