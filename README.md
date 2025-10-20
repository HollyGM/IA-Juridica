# Sistema de IA Jurídica - Estrategista Jurídico-Cognitivo

**Versão 3.0**

Este projeto é uma ferramenta de linha de comando robusta e avançada, projetada para converter documentos jurídicos (`.txt`, `.pdf`, `.docx`) em uma base de conhecimento `JSON` estruturada. O sistema utiliza Processamento de Linguagem Natural (NLP) para enriquecer os dados, preparando-os para uso em modelos de IA como Claude, GPT e Gemini.

## 🌟 Funcionalidades Principais

- **Suporte a Múltiplos Formatos**: Extrai texto de `.txt`, `.pdf` e `.docx`.
- **Modo Interativo e Autônomo**:
  - **Interface Gráfica**: Um seletor de pastas para uso fácil e interativo.
  - **Linha de Comando**: Argumentos para automação completa de tarefas.
- **Análise NLP Avançada**:
  - **NER Jurídico**: Identifica leis, processos, tribunais e outras entidades.
  - **Sumarização Automática**: Gera resumos inteligentes dos documentos.
  - **Classificação e Análise Estrutural**: Entende o propósito e a estrutura do texto.
- **Logs Detalhados**: Registra cada passo do processo em um arquivo `processing.log` para fácil depuração e auditoria.
- **Relatório em HTML**: Gera um relatório final claro e profissional com estatísticas e resultados.
- **Preparação para RAG**: Otimiza os dados para sistemas de *Retrieval-Augmented Generation*.
- **Configuração Flexível**: Permite escolher o nível de processamento NLP (`rapido`, `padrao`, `completo`).

## 🚀 Começo Rápido

### Requisitos

- Python 3.7+
- `tkinter` (para o modo interativo)

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone [URL-do-seu-repositorio]
    cd [nome-do-repositorio]
    ```
2.  **Instale as dependências:**
    Use o script para Windows ou o `pip` para outros sistemas.
    ```bash
    # Windows
    INSTALAR_COMPLETO.bat

    # Linux/Mac
    pip install -r requirements.txt
    ```

### Modos de Execução

#### Modo Interativo (Recomendado para começar)

Basta executar o script principal. Ele fará perguntas para guiar o processo.

-   **Windows**: Dê um duplo clique em `EXECUTAR_IA_JURIDICA.bat`.
-   **Linux/Mac**:
    ```bash
    python main.py
    ```

#### Modo Autônomo (via Linha de Comando)

Use argumentos para especificar a pasta, o modo de NLP e o tamanho máximo do JSON.

```bash
python main.py --pasta "/caminho/para/seus/documentos" --nlp "padrao" --tamanho-max 100
```

-   `--pasta` ou `-p`: Define o diretório dos documentos.
-   `--nlp` ou `-n`: Escolhe o nível de análise (`nenhum`, `rapido`, `padrao`, `completo`).
-   `--tamanho-max` ou `-t`: Define o tamanho máximo de cada arquivo JSON em MB.

## 📄 Saídas do Processo

Ao final da execução, você encontrará os seguintes arquivos no diretório:

-   `knowledge_base_... .json`: Um ou mais arquivos JSON com os dados estruturados.
-   `relatorio_... .html`: Um relatório resumido com as estatísticas do processo.
-   `processing.log`: Um log detalhado de cada etapa da execução.

## 🏗️ Estrutura do Projeto

O projeto é modular para facilitar a manutenção:

```
/
├── main.py                    # Script principal
├── config.py                  # Configurações avançadas
├── requirements.txt           # Dependências
├── processing.log             # Arquivo de log gerado
│
├── *.bat                      # Scripts para Windows
│
└── modules/
    ├── file_scanner.py        # Localiza arquivos
    ├── (leitores de arquivo)  # txt_reader.py, pdf_reader.py, docx_reader.py
    ├── json_generator.py      # Gera o JSON
    ├── report_generator.py    # Gera o relatório HTML
    └── (módulos de NLP)       # nlp_processor.py, legal_ner.py, etc.
```

## ⚙️ Configuração Avançada

Para especialistas, o arquivo `config.py` oferece controle fino sobre os modelos de NLP, parâmetros de sumarização, e configurações de RAG.

## 🤝 Contribuições

Este projeto foi aprimorado pela IA Claude. Contribuições são bem-vindas! Sinta-se à vontade para abrir *issues* ou enviar *pull requests*.
