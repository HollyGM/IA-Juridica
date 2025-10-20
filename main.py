#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de IA Jurídica - Estrategista Jurídico-Cognitivo
Conversor de TXT/PDF para JSON com análise NLP avançada
Versão 2.0 - Com suporte a NER, Sumarização e RAG

Autor: Desenvolvido com Claude
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from tkinter import Tk, filedialog

# Configurar encoding UTF-8 para o console Windows
if sys.platform == 'win32':
    try:
        # Tenta configurar UTF-8 no console
        os.system('chcp 65001 > nul 2>&1')
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass  # Se falhar, continua sem emojis

from modules.file_scanner import scan_directory
from modules.txt_reader import read_txt_file
from modules.pdf_reader import read_pdf_file
from modules.json_generator import generate_knowledge_base_json, split_large_json

# Importa módulos NLP (com tratamento de erro)
try:
    from modules.nlp_processor import LegalNLPProcessor
    from modules.rag_indexer import RAGIndexer
    NLP_AVAILABLE = True
except ImportError as e:
    print(f"⚠ Módulos NLP não disponíveis: {str(e)}")
    NLP_AVAILABLE = False

# Importa configurações
try:
    from config import NLP_CONFIG, get_config
except ImportError:
    print("⚠ Arquivo de configuração não encontrado. Usando configurações padrão.")
    NLP_CONFIG = {
        'enable_ner': True,
        'enable_summarization': True,
        'enable_embeddings': False
    }
    def get_config(mode='standard'):
        return NLP_CONFIG


def select_folder():
    """Abre diálogo para seleção de pasta"""
    root = Tk()
    root.withdraw()  # Esconde a janela principal do Tkinter
    root.attributes('-topmost', True)  # Traz o diálogo para frente

    folder_path = filedialog.askdirectory(
        title="Selecione a pasta com os arquivos TXT/PDF",
        initialdir=os.path.expanduser("~")
    )

    root.destroy()
    return folder_path


def process_files(folder_path, enable_nlp=False, nlp_config=None):
    """
    Processa todos os arquivos TXT e PDF na pasta selecionada

    Args:
        folder_path: Caminho da pasta a ser processada
        enable_nlp: Se True, aplica análise NLP nos documentos
        nlp_config: Configurações NLP personalizadas

    Returns:
        dict: Estrutura de dados com todos os arquivos processados
    """
    print(f"\n🔍 Escaneando pasta: {folder_path}")

    # Escaneia diretório e encontra todos os arquivos TXT e PDF
    files_found = scan_directory(folder_path)

    if not files_found:
        print("⚠️  Nenhum arquivo TXT ou PDF encontrado!")
        return None

    print(f"✅ Encontrados {len(files_found)} arquivo(s)")

    # Estrutura de dados que será convertida em JSON
    knowledge_base = {
        "metadata": {
            "source_directory": str(folder_path),
            "creation_date": datetime.now().isoformat(),
            "total_files": len(files_found),
            "file_types": {
                "txt": sum(1 for f in files_found if f.get('type') == 'txt'),
                "pdf": sum(1 for f in files_found if f.get('type') == 'pdf')
            },
            "nlp_enabled": enable_nlp
        },
        "documents": []
    }

    # Processa cada arquivo
    print("\n📄 Processando arquivos...")
    for idx, file_info in enumerate(files_found, 1):
        file_path = file_info['path']
        file_type = file_info['type']
        relative_path = file_info['relative_path']

        print(f"  [{idx}/{len(files_found)}] {relative_path}", end=" ... ")

        try:
            # Lê o conteúdo do arquivo baseado no tipo
            if file_type == 'txt':
                content = read_txt_file(file_path)
            elif file_type == 'pdf':
                content = read_pdf_file(file_path)
            else:
                print("❌ Tipo não suportado")
                continue

            # Adiciona documento à base de conhecimento
            document = {
                "id": f"doc_{idx:04d}",
                "filename": os.path.basename(file_path),
                "relative_path": relative_path,
                "type": file_type,
                "size_bytes": os.path.getsize(file_path),
                "modified_date": datetime.fromtimestamp(
                    os.path.getmtime(file_path)
                ).isoformat(),
                "content": content,
                "char_count": len(content),
                "word_count": len(content.split())
            }

            knowledge_base["documents"].append(document)
            print("✅")

        except Exception as e:
            print(f"❌ Erro: {str(e)}")
            continue

    # Aplica análise NLP se habilitado
    if enable_nlp and NLP_AVAILABLE and knowledge_base["documents"]:
        print("\n" + "=" * 60)
        print("  🧠 INICIANDO ANÁLISE NLP AVANÇADA")
        print("=" * 60)

        try:
            processor = LegalNLPProcessor(nlp_config or NLP_CONFIG)
            knowledge_base["documents"] = processor.process_batch(knowledge_base["documents"])
            print("✅ Análise NLP concluída com sucesso")
        except Exception as e:
            print(f"⚠ Erro na análise NLP: {str(e)}")
            print("   Continuando sem análise NLP...")

    return knowledge_base


def save_json(data, output_path):
    """
    Salva os dados em arquivo JSON

    Args:
        data: Dados a serem salvos
        output_path: Caminho do arquivo de saída
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"❌ Erro ao salvar JSON: {str(e)}")
        return False


def save_multiple_json_files(data_list, base_output_path):
    """
    Salva múltiplos arquivos JSON quando os dados foram divididos

    Args:
        data_list: Lista de dicionários (cada um será um arquivo separado)
        base_output_path: Caminho base para os arquivos de saída

    Returns:
        list: Lista de caminhos dos arquivos salvos com sucesso
    """
    saved_files = []
    total_parts = len(data_list)

    # Se há apenas uma parte, salva com o nome original
    if total_parts == 1:
        if save_json(data_list[0], base_output_path):
            saved_files.append(base_output_path)
        return saved_files

    # Divide o caminho para adicionar sufixo de parte
    base_dir = os.path.dirname(base_output_path)
    base_name = os.path.basename(base_output_path)
    name_without_ext = os.path.splitext(base_name)[0]

    print(f"\n💾 Salvando {total_parts} arquivos JSON...")

    for i, data_part in enumerate(data_list, 1):
        # Cria o nome do arquivo com sufixo de parte
        part_filename = f"{name_without_ext}_parte_{i}_de_{total_parts}.json"
        part_path = os.path.join(base_dir, part_filename)

        print(f"   Salvando parte {i}/{total_parts}...", end=" ")

        if save_json(data_part, part_path):
            saved_files.append(part_path)
            file_size_mb = os.path.getsize(part_path) / (1024 * 1024)
            print(f"✅ ({file_size_mb:.2f} MB)")
        else:
            print(f"❌ Falha")

    return saved_files


def ask_max_json_size():
    """
    Pergunta ao usuário o tamanho máximo desejado para cada arquivo JSON

    Returns:
        int: Tamanho máximo em MB
    """
    print("\n" + "=" * 60)
    print("⚙️  CONFIGURAÇÃO DE TAMANHO DOS ARQUIVOS JSON")
    print("=" * 60)
    print("\n📏 Informe o tamanho máximo para cada arquivo JSON.")
    print("   (Recomendado: 50 MB para Gemini e outros modelos)")
    print("   (Limite do Gemini: 100 MB, mas é melhor usar um valor menor)")

    while True:
        try:
            user_input = input("\n💾 Tamanho máximo por arquivo (MB) [padrão: 50]: ").strip()

            # Se o usuário não digitar nada, usa o valor padrão de 50MB
            if not user_input:
                max_size = 50
                print(f"✅ Usando tamanho padrão: {max_size} MB")
                break

            max_size = int(user_input)

            # Validação do tamanho
            if max_size < 1:
                print("❌ O tamanho deve ser no mínimo 1 MB. Tente novamente.")
                continue
            elif max_size > 100:
                print("⚠️  Aviso: Tamanhos acima de 100 MB podem exceder o limite de alguns modelos.")
                confirm = input("   Deseja continuar mesmo assim? (s/n): ").strip().lower()
                if confirm == 's' or confirm == 'sim':
                    break
                else:
                    continue
            else:
                print(f"✅ Tamanho configurado: {max_size} MB")
                break

        except ValueError:
            print("❌ Por favor, digite um número válido.")
        except KeyboardInterrupt:
            print("\n\n⚠️  Operação cancelada pelo usuário.")
            sys.exit(0)

    return max_size


def ask_nlp_processing():
    """
    Pergunta ao usuário se deseja processar com NLP

    Returns:
        tuple: (enable_nlp, config_mode)
    """
    if not NLP_AVAILABLE:
        print("\n⚠ Módulos NLP não estão disponíveis.")
        print("   Para usar NLP, instale as dependências: pip install -r requirements.txt")
        return False, None

    print("\n" + "=" * 60)
    print("⚙️  CONFIGURAÇÃO DE PROCESSAMENTO NLP")
    print("=" * 60)
    print("\n🧠 Deseja aplicar análise NLP avançada nos documentos?")
    print("   Isso inclui:")
    print("   • Extração de entidades jurídicas (NER)")
    print("   • Sumarização automática")
    print("   • Classificação de documentos")
    print("   • Análise estrutural")
    print("\n⚠ ATENÇÃO: O processamento NLP pode levar mais tempo.")

    while True:
        response = input("\n🔹 Ativar NLP? (s/n) [padrão: s]: ").strip().lower()

        if not response or response in ['s', 'sim', 'y', 'yes']:
            enable_nlp = True

            # Pergunta o modo de processamento
            print("\n📊 Escolha o modo de processamento:")
            print("   1. RÁPIDO - Apenas NER (mais rápido)")
            print("   2. PADRÃO - NER + Sumarização (recomendado)")
            print("   3. COMPLETO - NER + Sumarização + Embeddings (mais lento)")

            mode_input = input("\n🔹 Escolha o modo (1/2/3) [padrão: 2]: ").strip()

            if mode_input == '1':
                config_mode = 'fast'
                print("✅ Modo RÁPIDO selecionado")
            elif mode_input == '3':
                config_mode = 'full'
                print("✅ Modo COMPLETO selecionado")
            else:
                config_mode = 'standard'
                print("✅ Modo PADRÃO selecionado")

            return True, config_mode

        elif response in ['n', 'nao', 'não', 'no']:
            print("✅ Processamento sem NLP")
            return False, None
        else:
            print("❌ Resposta inválida. Digite 's' ou 'n'.")


def main():
    """Função principal do programa"""
    print("=" * 60)
    print("  🧠 SISTEMA DE IA JURÍDICA")
    print("  Estrategista Jurídico-Cognitivo v2.0")
    print("=" * 60)
    print("  Conversor TXT/PDF → JSON + Análise NLP")
    print("=" * 60)

    # Seleciona a pasta
    folder_path = select_folder()

    if not folder_path:
        print("\n❌ Nenhuma pasta selecionada. Encerrando...")
        sys.exit(1)

    if not os.path.isdir(folder_path):
        print(f"\n❌ Caminho inválido: {folder_path}")
        sys.exit(1)

    # Pergunta sobre processamento NLP
    enable_nlp, config_mode = ask_nlp_processing()

    # Obtém configuração NLP
    nlp_config = get_config(config_mode) if config_mode else None

    # Pergunta o tamanho máximo desejado para cada arquivo JSON
    max_size_mb = ask_max_json_size()

    # Processa os arquivos
    knowledge_base = process_files(folder_path, enable_nlp=enable_nlp, nlp_config=nlp_config)

    if not knowledge_base or not knowledge_base.get('documents'):
        print("\n⚠️  Nenhum documento foi processado com sucesso.")
        sys.exit(1)

    # Define o nome base do arquivo de saída
    folder_name = os.path.basename(folder_path.rstrip(os.sep))
    output_filename = f"knowledge_base_{folder_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_filename)

    # Verifica se precisa dividir em múltiplos arquivos
    print(f"\n🔍 Verificando tamanho do JSON...")
    json_parts = split_large_json(knowledge_base, max_size_mb)

    if len(json_parts) > 1:
        print(f"⚠️  O arquivo será dividido em {len(json_parts)} partes para respeitar o limite de {max_size_mb} MB")

    # Salva os arquivos JSON
    saved_files = save_multiple_json_files(json_parts, output_path)

    if saved_files:
        print(f"\n✅ {len(saved_files)} arquivo(s) salvo(s) com sucesso!")

        # Estatísticas gerais
        total_chars = sum(doc['char_count'] for doc in knowledge_base['documents'])
        total_words = sum(doc['word_count'] for doc in knowledge_base['documents'])

        print(f"\n📊 ESTATÍSTICAS GERAIS:")
        print(f"   📄 Total de documentos processados: {len(knowledge_base['documents'])}")
        print(f"   📝 Total de caracteres: {total_chars:,}")
        print(f"   🔤 Total de palavras: {total_words:,}")

        # Lista os arquivos salvos
        print(f"\n📁 ARQUIVO(S) GERADO(S):")
        total_size_mb = 0
        for file_path in saved_files:
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
            total_size_mb += file_size_mb
            print(f"   • {os.path.basename(file_path)} ({file_size_mb:.2f} MB)")

        print(f"\n   💾 Tamanho total: {total_size_mb:.2f} MB")
        print(f"   📂 Localização: {os.path.dirname(saved_files[0])}")

        print("\n✨ Pronto para uso em modelos de IA (Claude, GPT, Gemini, Perplexity)")
    else:
        print("❌ Falha ao salvar os arquivos.")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("Processo concluído com sucesso! 🎉")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Operação cancelada pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {str(e)}")
        sys.exit(1)
