"""
Módulo para Reconhecimento de Entidades Nomeadas (NER) em textos jurídicos brasileiros
Baseado em Flair, spaCy e modelos customizados para o domínio jurídico
"""

import re
from typing import Dict, List, Any, Optional
import warnings
warnings.filterwarnings('ignore')


class LegalEntityExtractor:
    """
    Extrator de entidades jurídicas específicas do domínio legal brasileiro
    """

    def __init__(self):
        """Inicializa o extrator com padrões regex para entidades jurídicas"""
        self.initialized = False
        self.use_ml_models = False

        # Padrões regex para entidades jurídicas brasileiras
        self.patterns = {
            'processo': [
                r'\d{7}-\d{2}\.\d{4}\.\d{1}\.\d{2}\.\d{4}',  # Formato CNJ
                r'\d{4}\.\d{2}\.\d{4}\.\d{7}-\d{1}',  # Formato antigo
                r'processo\s+n[°º]?\s*[\d\.\-/]+',
            ],
            'lei': [
                r'Lei\s+(?:Federal\s+)?n[°º]?\s*[\d\.]+(?:/\d{4})?',
                r'LC\s+n[°º]?\s*[\d\.]+(?:/\d{4})?',  # Lei Complementar
                r'MP\s+n[°º]?\s*[\d\.]+(?:/\d{4})?',  # Medida Provisória
                r'Decreto\s+n[°º]?\s*[\d\.]+(?:/\d{4})?',
            ],
            'artigo': [
                r'art(?:igo)?\.?\s+\d+[°º]?(?:\s*,\s*(?:§|art\.)\s*\d+[°º]?)*',
                r'inciso\s+[IVXLCDM]+',
                r'alínea\s+[a-z]',
            ],
            'jurisprudencia': [
                r'S[úu]mula\s+(?:Vinculante\s+)?n[°º]?\s*\d+',
                r'(?:RE|REsp|AI|AgRg|HC|MS|ADI|ADC)\s+n[°º]?\s*[\d\.]+',
                r'Recurso\s+Extraordinário\s+n[°º]?\s*[\d\.]+',
                r'Recurso\s+Especial\s+n[°º]?\s*[\d\.]+',
            ],
            'tribunal': [
                r'STF|Supremo\s+Tribunal\s+Federal',
                r'STJ|Superior\s+Tribunal\s+de\s+Justi[çc]a',
                r'TST|Tribunal\s+Superior\s+do\s+Trabalho',
                r'TSE|Tribunal\s+Superior\s+Eleitoral',
                r'TJ[A-Z]{2}|Tribunal\s+de\s+Justi[çc]a\s+(?:do|de|da)\s+\w+',
                r'TRF[-\s]?\d{1}|Tribunal\s+Regional\s+Federal\s+da\s+\d[ªº]?\s+Regi[ãa]o',
                r'TRT[-\s]?\d{1,2}|Tribunal\s+Regional\s+do\s+Trabalho\s+da\s+\d{1,2}[ªº]?\s+Regi[ãa]o',
            ],
            'ministro': [
                r'(?:Ministro|Ministra|Min\.|Desembargador|Desembargadora|Des\.)\s+[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][a-záàâãéêíóôõúç]+(?:\s+[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][a-záàâãéêíóôõúç]+)*',
            ],
            'vara': [
                r'\d{1,2}[ªº]?\s+Vara\s+(?:C[íi]vel|Criminal|Federal|Estadual|do\s+Trabalho|da\s+Fam[íi]lia)',
                r'Vara\s+(?:C[íi]vel|Criminal|Federal)\s+da\s+Comarca\s+de\s+\w+',
            ],
            'data': [
                r'\d{1,2}\s+de\s+(?:janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro)\s+de\s+\d{4}',
                r'\d{1,2}/\d{1,2}/\d{4}',
                r'\d{4}-\d{2}-\d{2}',
            ],
            'valor_monetario': [
                r'R\$\s*[\d\.]+,\d{2}',
                r'(?:valor|quantia|montante)\s+de\s+R?\$?\s*[\d\.,]+',
            ],
            'cpf_cnpj': [
                r'\d{3}\.\d{3}\.\d{3}-\d{2}',  # CPF
                r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}',  # CNPJ
            ],
        }

    def initialize_ml_models(self):
        """Inicializa modelos de ML (spaCy, Flair) se disponíveis"""
        try:
            import spacy
            try:
                self.nlp = spacy.load('pt_core_news_lg')
                self.use_ml_models = True
                print("✓ Modelo spaCy carregado para português")
            except:
                try:
                    self.nlp = spacy.load('pt_core_news_sm')
                    self.use_ml_models = True
                    print("✓ Modelo spaCy básico carregado")
                except:
                    print("⚠ Modelo spaCy não encontrado. Usando apenas regex.")
                    self.use_ml_models = False
        except ImportError:
            print("⚠ spaCy não instalado. Usando apenas regex.")
            self.use_ml_models = False

        self.initialized = True

    def extract_entities(self, text: str, use_ml: bool = True) -> Dict[str, List[Dict[str, Any]]]:
        """
        Extrai entidades nomeadas do texto jurídico

        Args:
            text: Texto a ser analisado
            use_ml: Se True, usa modelos ML quando disponíveis

        Returns:
            Dicionário com entidades extraídas por categoria
        """
        if not self.initialized:
            self.initialize_ml_models()

        entities = {
            'processos': [],
            'leis': [],
            'artigos': [],
            'jurisprudencias': [],
            'tribunais': [],
            'ministros': [],
            'varas': [],
            'datas': [],
            'valores_monetarios': [],
            'documentos': [],
            'pessoas': [],
            'organizacoes': [],
            'locais': []
        }

        # Extração baseada em regex
        entities['processos'] = self._extract_by_pattern(text, 'processo')
        entities['leis'] = self._extract_by_pattern(text, 'lei')
        entities['artigos'] = self._extract_by_pattern(text, 'artigo')
        entities['jurisprudencias'] = self._extract_by_pattern(text, 'jurisprudencia')
        entities['tribunais'] = self._extract_by_pattern(text, 'tribunal')
        entities['ministros'] = self._extract_by_pattern(text, 'ministro')
        entities['varas'] = self._extract_by_pattern(text, 'vara')
        entities['datas'] = self._extract_by_pattern(text, 'data')
        entities['valores_monetarios'] = self._extract_by_pattern(text, 'valor_monetario')
        entities['documentos'] = self._extract_by_pattern(text, 'cpf_cnpj')

        # Extração com modelos ML (spaCy) se disponível
        if use_ml and self.use_ml_models:
            ml_entities = self._extract_with_spacy(text)
            entities['pessoas'].extend(ml_entities.get('PER', []))
            entities['organizacoes'].extend(ml_entities.get('ORG', []))
            entities['locais'].extend(ml_entities.get('LOC', []))

        # Remove duplicatas
        for key in entities:
            entities[key] = self._remove_duplicates(entities[key])

        return entities

    def _extract_by_pattern(self, text: str, entity_type: str) -> List[Dict[str, Any]]:
        """Extrai entidades usando padrões regex"""
        entities = []
        patterns = self.patterns.get(entity_type, [])

        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                entities.append({
                    'text': match.group(0),
                    'start': match.start(),
                    'end': match.end(),
                    'type': entity_type
                })

        return entities

    def _extract_with_spacy(self, text: str) -> Dict[str, List[Dict[str, Any]]]:
        """Extrai entidades usando spaCy"""
        entities = {'PER': [], 'ORG': [], 'LOC': []}

        try:
            doc = self.nlp(text[:1000000])  # Limita para evitar OOM

            for ent in doc.ents:
                if ent.label_ in ['PER', 'PERSON']:
                    entities['PER'].append({
                        'text': ent.text,
                        'start': ent.start_char,
                        'end': ent.end_char,
                        'type': 'pessoa'
                    })
                elif ent.label_ in ['ORG']:
                    entities['ORG'].append({
                        'text': ent.text,
                        'start': ent.start_char,
                        'end': ent.end_char,
                        'type': 'organizacao'
                    })
                elif ent.label_ in ['LOC', 'GPE']:
                    entities['LOC'].append({
                        'text': ent.text,
                        'start': ent.start_char,
                        'end': ent.end_char,
                        'type': 'local'
                    })
        except Exception as e:
            print(f"⚠ Erro ao processar com spaCy: {str(e)}")

        return entities

    def _remove_duplicates(self, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove entidades duplicadas"""
        seen = set()
        unique = []

        for entity in entities:
            text_lower = entity['text'].lower().strip()
            if text_lower not in seen:
                seen.add(text_lower)
                unique.append(entity)

        return unique

    def extract_teses_argumentos(self, text: str) -> Dict[str, List[str]]:
        """
        Extrai teses, argumentos e refutações (análise estrutural básica)

        Args:
            text: Texto jurídico

        Returns:
            Dicionário com teses, argumentos e refutações
        """
        result = {
            'teses_principais': [],
            'teses_subsidiarias': [],
            'argumentos_favoraveis': [],
            'argumentos_contrarios': [],
            'refutacoes': []
        }

        # Marcadores textuais comuns
        tese_markers = [
            r'(?:sustenta-se|alega-se|defende-se|propõe-se)\s+que\s+([^.]+\.)',
            r'tese\s+(?:principal|central|defendida)[:\s]+([^.]+\.)',
            r'(?:entende-se|considera-se)\s+que\s+([^.]+\.)'
        ]

        argumento_fav_markers = [
            r'(?:em|de)\s+favor\s+(?:de|da|do)\s+([^.]+\.)',
            r'(?:corrobora|reforça|sustenta)\s+(?:a|o)\s+([^.]+\.)',
            r'argumenta-se\s+que\s+([^.]+\.)'
        ]

        argumento_contra_markers = [
            r'(?:em|de)\s+(?:desfavor|contrário)\s+(?:de|da|do)\s+([^.]+\.)',
            r'(?:rebate|contesta|refuta)\s+(?:a|o)\s+([^.]+\.)',
            r'contra-argumenta-se\s+que\s+([^.]+\.)'
        ]

        # Extrai teses
        for pattern in tese_markers:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                result['teses_principais'].append(match.group(1).strip())

        # Extrai argumentos favoráveis
        for pattern in argumento_fav_markers:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                result['argumentos_favoraveis'].append(match.group(1).strip())

        # Extrai argumentos contrários
        for pattern in argumento_contra_markers:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                result['argumentos_contrarios'].append(match.group(1).strip())

        return result


def extract_legal_entities(text: str) -> Dict[str, Any]:
    """
    Função helper para extração rápida de entidades jurídicas

    Args:
        text: Texto jurídico

    Returns:
        Dicionário com entidades e análise estrutural
    """
    extractor = LegalEntityExtractor()

    # Extrai entidades
    entities = extractor.extract_entities(text)

    # Extrai teses e argumentos
    teses_argumentos = extractor.extract_teses_argumentos(text)

    return {
        'entidades': entities,
        'analise_estrutural': teses_argumentos,
        'estatisticas': {
            'total_processos': len(entities['processos']),
            'total_leis': len(entities['leis']),
            'total_jurisprudencias': len(entities['jurisprudencias']),
            'total_tribunais': len(entities['tribunais']),
            'total_entidades': sum(len(v) for v in entities.values())
        }
    }
