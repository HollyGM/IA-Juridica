# Início Rápido

## ⚡ Windows - Modo Super Fácil (Recomendado)

**Apenas dê duplo clique em:**

```
INICIAR.bat
```

Pronto! O programa instalará as dependências automaticamente e iniciará.

---

## 🐧 Linux/Mac ou Modo Manual

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Executar o programa
```bash
python main.py
```

---

## 📂 Processo de Uso

### 1. Selecionar pasta
- Uma janela se abrirá para você escolher a pasta
- Pode conter arquivos na raiz ou em subpastas
- Serão processados apenas arquivos .txt e .pdf

### 2. Aguardar processamento
- O programa mostrará o progresso no terminal
- Cada arquivo será processado individualmente

### 3. JSON gerado
- Um arquivo JSON será criado no diretório do programa
- Nome no formato: `knowledge_base_[pasta]_[data]_[hora].json`

## O que você terá no final

Um arquivo JSON estruturado assim:

```json
{
  "metadata": {
    "source_directory": "sua/pasta",
    "creation_date": "2025-01-13T...",
    "total_files": 10,
    "file_types": {"txt": 7, "pdf": 3}
  },
  "documents": [
    {
      "id": "doc_0001",
      "filename": "documento.txt",
      "relative_path": "pasta/documento.txt",
      "content": "Conteúdo completo aqui...",
      "char_count": 1500,
      "word_count": 250
    }
  ]
}
```

## Usando com IA

### Claude
Faça upload do JSON e pergunte qualquer coisa sobre os documentos.

### ChatGPT
Use o JSON como contexto em conversas ou com a API de Assistants.

### Gemini
Carregue o JSON e aproveite o contexto longo do Gemini.

### Perplexity
Use como base de conhecimento para pesquisas especializadas.

## 🔧 Opções Adicionais (Windows)

### executar.bat
Execução com verificações detalhadas:
- Verifica se Python está instalado
- Mostra versão do Python
- Verifica dependências
- Instala apenas se necessário
- Pausa no final para ver resultado

### instalar_dependencias.bat
Apenas instala as dependências:
- Útil se você só quer preparar o ambiente
- Mostra informações detalhadas
- Verifica Python e pip

### INICIAR.bat (Recomendado)
Modo simplificado:
- Instala/atualiza dependências automaticamente
- Executa o programa imediatamente
- Interface limpa e direta

## 🆘 Problemas Comuns

### "Python não encontrado"
- Instale Python 3.7+ de: https://www.python.org/downloads/
- **IMPORTANTE**: Marque "Add Python to PATH" durante instalação

### "pip não encontrado"
- Reinstale Python marcando todas as opções
- Ou execute: `python -m ensurepip --upgrade`

### "Erro ao instalar pypdf"
- Execute manualmente: `pip install pypdf chardet`
- Verifique conexão com internet

## 📚 Dúvidas?

Veja `README.md` para documentação completa ou `EXEMPLO_USO.md` para exemplos detalhados.
