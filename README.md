# Sistema de IA Jurídica - Estrategista Jurídico-Cognitivo

**Versão 2.0**

Este projeto é uma ferramenta avançada de processamento de documentos jurídicos, projetada para converter arquivos `TXT` e `PDF` em uma base de conhecimento estruturada em formato `JSON`. O sistema foi desenvolvido com foco em IA, aplicando técnicas de Processamento de Linguagem Natural (NLP) para enriquecer os dados e prepará-los para uso em modelos como Claude, GPT, e Gemini.

## 🌟 Funcionalidades Principais

- **Interface Gráfica**: Seleção de pastas de forma intuitiva.
- **Processamento Recursivo**: Analisa todos os subdiretórios, mantendo a estrutura hierárquica.
- **Suporte a Múltiplos Formatos**: Extrai texto de arquivos `.txt`, `.pdf`, e `.docx`.
- **Análise NLP Avançada**:
  - **Reconhecimento de Entidades Nomeadas (NER)**: Identifica termos jurídicos como leis, processos, tribunais, etc.
  - **Sumarização Automática**: Gera resumos extrativos e abstrativos.
  - **Análise Estrutural**: Identifica teses, argumentos e decisões.
  - **Classificação de Documentos**: Determina o tipo de documento e a área do direito.
- **Preparação para RAG**: Otimiza os dados para sistemas de *Retrieval-Augmented Generation*.
- **Divisão de Arquivos Grandes**: Separa a base de conhecimento em múltiplos arquivos `JSON` para se adequar aos limites dos modelos de IA.
- **Configuração Flexível**: Permite escolher o nível de processamento NLP (rápido, padrão, completo).

## 🚀 Começo Rápido

### Requisitos

- Python 3.7 ou superior
- `tkinter` (geralmente incluído no Python)

### Instalação

1. **Clone ou baixe este repositório.**

2. **Instale as dependências:**
   O método recomendado é usar o `pip` com o arquivo `requirements.txt`.
   ```bash
   pip install -r requirements.txt
   ```
   Caso prefira, pode usar o script de instalação para Windows:
   - `instalar_dependencias.bat`

### Execução

- **Windows (Modo Fácil)**:
  - **`INICIAR.bat`**: Executa o programa com uma interface gráfica simples.
  - **`MODO_RAPIDO.bat`**: Executa com configurações de NLP otimizadas para velocidade.

- **Linux/Mac ou Manualmente**:
  ```bash
  python main.py
  ```

O programa guiará você através das seguintes etapas:
1. **Seleção da pasta** com os documentos.
2. **Configuração do processamento NLP** (se deseja ativar e em qual modo).
3. **Definição do tamanho máximo** para os arquivos `JSON` de saída.

## 🏗️ Estrutura do Projeto

O projeto é organizado de forma modular para facilitar a manutenção e expansão:

```
/
├── main.py                    # Script principal que orquestra o processo
├── config.py                  # Configurações de NLP, extração e performance
├── requirements.txt           # Dependências do projeto
├── README.md                  # Esta documentação
│
├── *.bat                      # Scripts para facilitar a execução no Windows
│
└── modules/                   # Módulos especializados
    ├── __init__.py
    ├── file_scanner.py        # Escaneia diretórios e localiza arquivos
    ├── txt_reader.py          # Lê arquivos de texto com detecção de encoding
    ├── pdf_reader.py          # Extrai texto de arquivos PDF
    ├── json_generator.py      # Gera e formata o JSON de saída
    ├── nlp_processor.py       # Orquestra a análise NLP
    ├── legal_ner.py           # Reconhecimento de Entidades Jurídicas
    ├── legal_summarizer.py    # Sumarização de textos jurídicos
    └── rag_indexer.py         # Prepara os dados para sistemas RAG
```

## 📄 Estrutura do JSON Gerado

O `JSON` de saída é enriquecido com uma análise NLP detalhada, tornando-o pronto para uso em aplicações de IA.

```json
{
  "schema_version": "2.0",
  "generated_at": "2025-10-20T12:00:00",
  "metadata": {
    "source_directory": "/path/to/your/documents",
    "nlp_enabled": true
  },
  "statistics": {
    "total_documents": 1,
    "nlp_analysis": {
      "total_entities": 50,
      "entity_types": { "processo": 5, "lei": 10 }
    }
  },
  "documents": [
    {
      "id": "doc_0001",
      "filename": "documento.pdf",
      "content": "...",
      "nlp_analysis": {
        "entidades": {
          "processos": [{ "text": "000123-45.2023.0.00.0000" }],
          "leis": [{ "text": "Lei nº 9.099/95" }]
        },
        "sumarizacao": {
          "resumo": "Este é um resumo do documento...",
          "pontos_chave": ["Ponto 1", "Ponto 2"]
        },
        "classificacao": {
          "tipo_documento": "sentenca",
          "area_direito": ["civil"]
        }
      }
    }
  ]
}
```

## ⚙️ Configuração Avançada

O arquivo `config.py` permite personalizar diversos aspectos do sistema:
- **Modelos de NLP**: Especifique quais modelos do `spaCy` ou `transformers` utilizar.
- **Parâmetros de Sumarização**: Ajuste o comprimento e a taxa de compressão dos resumos.
- **Configurações de RAG**: Defina o tamanho dos *chunks* e a sobreposição.

## 🤝 Contribuições

Este projeto foi desenvolvido com o auxílio da IA Claude. Sinta-se à vontade para abrir *issues*, sugerir melhorias ou enviar *pull requests*. Toda contribuição é bem-vinda!

## 📜 Licença

Este projeto é de código aberto e livre para uso e modificação.
