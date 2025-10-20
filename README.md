# Conversor TXT/PDF para JSON - Base de Conhecimento para IA

Programa Python que converte arquivos TXT e PDF de uma pasta (incluindo subpastas) em arquivo(s) JSON otimizado(s) para uso como base de conhecimento em modelos de IA como Claude, GPT, Gemini e Perplexity.

## Características

- Interface gráfica para seleção de pasta
- Processamento recursivo de diretórios (mantém hierarquia)
- Suporte para arquivos TXT e PDF
- Detecção automática de encoding para arquivos TXT
- Extração de texto de PDFs com múltiplas páginas
- Geração de JSON estruturado e otimizado
- Metadados detalhados de cada documento
- Estatísticas de processamento
- Divisão automática em múltiplos JSONs se necessário

## Requisitos

- Python 3.7 ou superior
- tkinter (geralmente incluído no Python)

## Instalação

1. Clone ou baixe este repositório

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

Ou instale manualmente:

```bash
pip install pypdf chardet
```

## Uso

### Windows (Modo Fácil)

Basta dar duplo clique em um dos arquivos:

- **INICIAR.bat** - Executa tudo automaticamente (recomendado)
- **executar.bat** - Executa com verificações detalhadas
- **instalar_dependencias.bat** - Apenas instala as dependências

### Linux/Mac ou Manual

Execute o programa:

```bash
python main.py
```

O programa irá:

1. Abrir uma janela para você selecionar a pasta desejada
2. Escanear recursivamente todos os arquivos .txt e .pdf
3. Processar cada arquivo extraindo seu conteúdo
4. Gerar um arquivo JSON com toda a base de conhecimento
5. Salvar o arquivo no mesmo diretório do programa

## Estrutura do JSON Gerado

```json
{
  "metadata": {
    "source_directory": "caminho/da/pasta",
    "creation_date": "2025-01-13T10:30:00",
    "total_files": 15,
    "file_types": {
      "txt": 10,
      "pdf": 5
    }
  },
  "documents": [
    {
      "id": "doc_0001",
      "filename": "exemplo.txt",
      "relative_path": "pasta/exemplo.txt",
      "type": "txt",
      "size_bytes": 1024,
      "modified_date": "2025-01-10T15:20:00",
      "content": "Conteúdo do arquivo...",
      "char_count": 500,
      "word_count": 100
    }
  ]
}
```

## Estrutura do Projeto

```
TXT-PDF = JSON/
├── main.py                      # Programa principal
├── requirements.txt             # Dependências
├── README.md                    # Documentação
│
├── INICIAR.bat                  # Executar (Windows - simples)
├── executar.bat                 # Executar (Windows - detalhado)
├── instalar_dependencias.bat    # Instalar apenas
│
├── QUICK_START.md               # Guia de início rápido
├── EXEMPLO_USO.md              # Exemplos detalhados
│
└── modules/                     # Módulos do programa
    ├── __init__.py
    ├── file_scanner.py          # Scanner de diretórios
    ├── txt_reader.py            # Leitor de arquivos TXT
    ├── pdf_reader.py            # Leitor de arquivos PDF
    └── json_generator.py        # Gerador de JSON
```

## Recursos Avançados

### Detecção Automática de Encoding
O programa tenta múltiplos encodings para garantir leitura correta:
- UTF-8
- UTF-8 com BOM
- Latin-1
- CP1252 (Windows)
- ISO-8859-1

### Processamento de PDFs
- Extrai texto de todas as páginas
- Mantém separação entre páginas
- Tratamento de erros por página

### Organização Hierárquica
- Mantém estrutura de pastas original
- Caminhos relativos preservados
- Facilita localização dos documentos

## Uso com Modelos de IA

### Claude (Anthropic)
```python
# Carregue o JSON e use como contexto
with open('knowledge_base.json', 'r', encoding='utf-8') as f:
    knowledge = json.load(f)
```

### GPT (OpenAI)
Ideal para uso com Assistants API ou embeddings.

### Gemini (Google)
Compatível com contextos longos do Gemini.

### Perplexity
Use como fonte de conhecimento para pesquisas.

## Tratamento de Erros

O programa é robusto e:
- Continua processando mesmo se um arquivo falhar
- Exibe claramente quais arquivos tiveram problemas
- Não interrompe a execução por erros individuais

## Limitações

- PDFs com imagens: apenas o texto é extraído
- PDFs protegidos: podem não ser lidos
- Arquivos muito grandes: podem ser divididos em múltiplos JSONs

## Licença

Este projeto foi gerado por Claude AI e é livre para uso e modificação.

## Contribuições

Sinta-se livre para melhorar o código e adicionar novas funcionalidades!

## Suporte

Para problemas ou dúvidas, abra uma issue no repositório.
