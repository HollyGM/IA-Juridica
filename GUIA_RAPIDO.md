# ⚡ Guia Rápido - Sistema de IA Jurídica v2.0

## 🚀 Início Rápido (3 passos)

### 1️⃣ Instalação (primeira vez)
```bash
# Clique duas vezes em:
INSTALAR_COMPLETO.bat

# Aguarde a instalação (5-15 minutos)
```

### 2️⃣ Execução
```bash
# Clique duas vezes em:
EXECUTAR_IA_JURIDICA.bat

# Siga as instruções na tela
```

### 3️⃣ Selecione sua pasta
- Escolha a pasta com seus arquivos PDF/TXT
- Aguarde o processamento
- Pronto! JSON gerado na pasta do programa

## 📋 Arquivos .BAT Disponíveis

### 🎯 Principais

| Arquivo | Descrição | Quando Usar |
|---------|-----------|-------------|
| `EXECUTAR_IA_JURIDICA.bat` | **Execução completa** | Uso normal do sistema |
| `INSTALAR_COMPLETO.bat` | Instala todas dependências | Primeira vez / Atualizar |
| `MODO_RAPIDO.bat` | Execução sem NLP | Teste rápido / Documentos simples |

### 🔧 Utilitários

| Arquivo | Descrição |
|---------|-----------|
| `TESTAR_NLP.bat` | Verifica se NLP está funcionando |
| `VER_CONFIGURACAO.bat` | Mostra configurações disponíveis |

## ⚙️ Opções de Processamento

Quando executar o programa, você verá estas opções:

### 🧠 Ativar NLP?
- **SIM** → Análise completa com IA
- **NÃO** → Apenas extração de texto (mais rápido)

### 📊 Modo de Processamento (se ativou NLP)
1. **RÁPIDO** → Apenas extração de entidades (5s/doc)
2. **PADRÃO** → NER + Sumarização (10s/doc) ✅ Recomendado
3. **COMPLETO** → Tudo + Embeddings (30s/doc)

### 💾 Tamanho máximo do JSON
- Digite o tamanho em MB (padrão: 50MB)
- O sistema divide automaticamente se necessário

## 📂 O que o Sistema Extrai

### 📄 De TODOS os documentos:
- ✅ Texto completo
- ✅ Metadados (tamanho, data, tipo)
- ✅ Estatísticas (palavras, caracteres)

### 🧠 Com NLP Ativado (modo PADRÃO ou COMPLETO):
- ✅ **Entidades jurídicas**: processos, leis, tribunais, ministros
- ✅ **Resumo automático** do documento
- ✅ **Classificação**: tipo de documento, área do direito
- ✅ **Análise estrutural**: teses, argumentos
- ✅ **Pontos-chave** mais importantes

### 🚀 Modo COMPLETO adiciona:
- ✅ Embeddings vetoriais (para busca semântica)
- ✅ Indexação FAISS
- ✅ Preparação completa para RAG

## 🎯 Exemplos de Uso

### Exemplo 1: Teste Rápido
```bash
1. Execute: MODO_RAPIDO.bat
2. Selecione uma pasta com 2-3 PDFs
3. Aguarde ~5 segundos
4. JSON gerado!
```

### Exemplo 2: Análise Completa de Acórdãos
```bash
1. Execute: EXECUTAR_IA_JURIDICA.bat
2. Ative NLP: SIM
3. Escolha modo: PADRÃO (2)
4. Tamanho JSON: 50 MB
5. Selecione pasta com acórdãos
6. Aguarde processamento
7. Confira JSON com análise completa!
```

### Exemplo 3: Grande Volume de Documentos
```bash
1. Execute: EXECUTAR_IA_JURIDICA.bat
2. Ative NLP: SIM
3. Escolha modo: RÁPIDO (1) - para economizar tempo
4. Tamanho JSON: 25 MB - arquivos menores
5. Selecione pasta
6. Sistema divide em múltiplos JSONs automaticamente
```

## ❓ Resolução de Problemas

### ⚠️ "Python não encontrado"
```bash
1. Instale Python 3.8+ de: python.org
2. IMPORTANTE: Marque "Add Python to PATH" na instalação
3. Reinicie o computador
4. Execute novamente
```

### ⚠️ "Módulos NLP não disponíveis"
```bash
1. Execute: INSTALAR_COMPLETO.bat
2. Aguarde instalação completa
3. Execute: TESTAR_NLP.bat para verificar
```

### ⚠️ "Erro ao processar PDF"
```bash
- Alguns PDFs com proteção podem falhar
- PDFs escaneados (imagem) precisam OCR
- Tente com outro PDF para testar
```

### ⚠️ Processamento muito lento
```bash
1. Use MODO_RAPIDO.bat para testar
2. Ou desative NLP na execução normal
3. Considere processar menos documentos por vez
```

### ⚠️ Memória insuficiente
```bash
1. Feche outros programas
2. Processe menos documentos por vez
3. Use modo RÁPIDO ou PADRÃO (evite COMPLETO)
4. Reduza chunk_size em config.py
```

## 📊 Entendendo o JSON Gerado

### Estrutura básica:
```json
{
  "metadata": {
    "total_files": 10,        // Quantos arquivos foram processados
    "nlp_enabled": true       // NLP foi usado?
  },
  "documents": [              // Lista de documentos
    {
      "id": "doc_0001",
      "filename": "acordao.pdf",
      "content": "...",       // Texto completo
      "nlp_analysis": {       // Análise NLP (se ativado)
        "entidades": {...},   // Entidades extraídas
        "sumarizacao": {...}, // Resumo e pontos-chave
        "classificacao": {...} // Tipo e área do direito
      }
    }
  ]
}
```

## 🎓 Dicas Pro

### 💡 Para Melhor Performance:
1. Organize documentos por pasta/tipo antes
2. Use modo apropriado para sua necessidade
3. Processe em lotes de 50-100 documentos
4. Mantenha JSONs entre 25-50MB

### 💡 Para Melhor Análise NLP:
1. Use modo PADRÃO para documentos importantes
2. Use modo RÁPIDO para triagem inicial
3. Use modo COMPLETO para base RAG definitiva

### 💡 Para Economizar Tempo:
1. Primeira vez: teste com 2-3 documentos
2. Ajuste configurações em `config.py`
3. Depois processe todo o acervo

## 📞 Precisa de Ajuda?

1. ✅ Execute: `TESTAR_NLP.bat`
2. ✅ Leia: `README_V2.md` (documentação completa)
3. ✅ Edite: `config.py` (personalizações)

---

## 🎯 Comandos Rápidos (Resumo)

| Ação | Comando |
|------|---------|
| Primeira instalação | `INSTALAR_COMPLETO.bat` |
| Usar o sistema | `EXECUTAR_IA_JURIDICA.bat` |
| Teste rápido | `MODO_RAPIDO.bat` |
| Verificar NLP | `TESTAR_NLP.bat` |
| Ver configurações | `VER_CONFIGURACAO.bat` |
| Ver config avançada | Editar `config.py` |

---

**⚡ Guia Rápido - Sistema de IA Jurídica v2.0**

*Agora você está pronto para processar seus documentos jurídicos!*
