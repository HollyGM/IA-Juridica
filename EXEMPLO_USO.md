# Guia de Uso - Conversor TXT/PDF para JSON

## Passo a Passo

### 1. Preparação

Certifique-se de ter Python 3.7+ instalado:

```bash
python --version
```

### 2. Instalação das Dependências

```bash
pip install -r requirements.txt
```

### 3. Executar o Programa

```bash
python main.py
```

### 4. Selecionar a Pasta

Uma janela de diálogo será aberta. Navegue até a pasta que contém seus arquivos TXT/PDF e clique em "Selecionar Pasta".

### 5. Aguardar o Processamento

O programa irá:
- Escanear todos os arquivos
- Processar cada um deles
- Exibir o progresso no terminal

### 6. Verificar o Resultado

Ao final, um arquivo JSON será criado com nome no formato:
```
knowledge_base_[nome_da_pasta]_[data]_[hora].json
```

## Exemplo de Estrutura de Pasta

```
MeusProjetos/
├── documentacao.txt
├── relatorio.pdf
├── capitulo1/
│   ├── intro.txt
│   └── conceitos.pdf
└── capitulo2/
    └── conclusao.txt
```

Todos esses arquivos serão processados mantendo a hierarquia.

## Exemplo de Saída no Terminal

```
============================================================
  📚 CONVERSOR TXT/PDF → JSON
  Base de Conhecimento para Modelos de IA
============================================================

🔍 Escaneando pasta: C:\Users\Usuario\MeusProjetos
✅ Encontrados 5 arquivo(s)

📄 Processando arquivos...
  [1/5] documentacao.txt ... ✅
  [2/5] relatorio.pdf ... ✅
  [3/5] capitulo1\intro.txt ... ✅
  [4/5] capitulo1\conceitos.pdf ... ✅
  [5/5] capitulo2\conclusao.txt ... ✅

💾 Salvando arquivo JSON...
✅ Arquivo salvo com sucesso!

📁 Localização: E:\TXT-PDF = JSON\knowledge_base_MeusProjetos_20250113_143000.json
📊 Tamanho: 125.43 KB
📄 Total de documentos: 5
📝 Total de caracteres: 52,340
🔤 Total de palavras: 8,456

✨ Pronto para uso em modelos de IA (Claude, GPT, Gemini, Perplexity)

============================================================
Processo concluído com sucesso! 🎉
============================================================
```

## Como Usar o JSON com Modelos de IA

### Claude (Anthropic)

**Opção 1: Upload de Arquivo**
- Faça upload do JSON diretamente na interface do Claude
- Pergunte sobre qualquer informação contida nos documentos

**Opção 2: API**
```python
import anthropic
import json

with open('knowledge_base.json', 'r', encoding='utf-8') as f:
    knowledge = json.load(f)

client = anthropic.Anthropic(api_key="sua-chave")
message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": f"Base de conhecimento: {json.dumps(knowledge)}\n\nSua pergunta aqui"
    }]
)
```

### GPT (OpenAI)

**Com Assistants API:**
```python
import openai
import json

with open('knowledge_base.json', 'r', encoding='utf-8') as f:
    knowledge = json.load(f)

# Criar assistente com a base de conhecimento
assistant = openai.beta.assistants.create(
    name="Assistente de Documentos",
    instructions="Você é um assistente que responde perguntas baseado na base de conhecimento fornecida.",
    model="gpt-4-turbo-preview",
)

# Usar em conversas
thread = openai.beta.threads.create()
message = openai.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=f"Base: {json.dumps(knowledge)}\n\nPergunta: ..."
)
```

### Gemini (Google)

```python
import google.generativeai as genai
import json

with open('knowledge_base.json', 'r', encoding='utf-8') as f:
    knowledge = json.load(f)

genai.configure(api_key="sua-chave")
model = genai.GenerativeModel('gemini-pro')

response = model.generate_content(
    f"Base de conhecimento: {json.dumps(knowledge)}\n\nPergunta: ..."
)
print(response.text)
```

### Perplexity

Use a API da Perplexity ou faça upload do JSON como contexto para pesquisas aprimoradas.

## Dicas e Boas Práticas

### 1. Organização de Arquivos

Organize seus documentos em pastas lógicas antes de processar:

```
Projeto/
├── fundamentos/
├── avancado/
└── referencias/
```

### 2. Nomes Descritivos

Use nomes de arquivo descritivos:
- ✅ `introducao_machine_learning.txt`
- ❌ `doc1.txt`

### 3. Formato dos Arquivos

- **TXT**: Use UTF-8 sempre que possível
- **PDF**: Certifique-se de que o texto é selecionável (não imagens)

### 4. Tamanho dos Arquivos

- Arquivos muito grandes serão divididos automaticamente
- Para melhor performance, considere dividir documentos gigantes manualmente

### 5. Validação do JSON

Após gerar, você pode validar o JSON:

```python
import json

with open('knowledge_base.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    print(f"✅ JSON válido!")
    print(f"📄 Documentos: {len(data['documents'])}")
```

## Solução de Problemas

### Erro: "Biblioteca PyPDF não instalada"

```bash
pip install pypdf
```

### Erro de Encoding em TXT

O programa tenta múltiplos encodings automaticamente, mas se persistir:
- Abra o arquivo no Notepad++
- Converta para UTF-8
- Salve e tente novamente

### PDF sem texto extraível

Se o PDF for uma imagem escaneada:
- Use OCR primeiro (Tesseract, Adobe Acrobat)
- Depois processe com este programa

### Janela de seleção não abre

Verifique se tkinter está instalado:

```bash
python -m tkinter
```

## Exemplos de Perguntas para IA

Após carregar o JSON em um modelo de IA:

- "Faça um resumo de todos os documentos na pasta 'fundamentos'"
- "Liste os principais conceitos mencionados em relatorio.pdf"
- "Compare as informações entre capitulo1 e capitulo2"
- "Extraia todas as datas mencionadas nos documentos"
- "Crie um índice temático de toda a base de conhecimento"

## Personalização

### Adicionar Novos Formatos

Edite `modules/file_scanner.py` e adicione extensões:

```python
extensions = ['.txt', '.pdf', '.md', '.docx']
```

### Modificar Estrutura JSON

Edite `modules/json_generator.py` para adicionar campos:

```python
document = {
    "id": ...,
    "custom_field": "seu_valor",
    # ...
}
```

## Atualizações Futuras

Possíveis melhorias:
- [ ] Suporte para DOCX
- [ ] Suporte para Markdown
- [ ] Interface gráfica completa
- [ ] Processamento paralelo
- [ ] Compressão de JSON
- [ ] Geração de embeddings

## Contato e Suporte

Para dúvidas, problemas ou sugestões, abra uma issue no repositório.

Aproveite sua base de conhecimento automatizada! 🚀
