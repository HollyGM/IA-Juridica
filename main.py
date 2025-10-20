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
    NLP_AVAILABLE = True
except ImportError as e:
    print(f"⚠ Módulos NLP não disponíveis: {str(e)}")
    NLP_AVAILABLE = False

# Importa configurações
try:
    from config import get_config
except ImportError:
    print("⚠ Arquivo de configuração não encontrado. Usando configurações padrão.")
    def get_config(mode='standard'):
        return {
            'enable_ner': True,
            'enable_summarization': True,
            'enable_embeddings': False
        }


def select_folder():
    """Abre diálogo para seleção de pasta"""
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)

    folder_path = filedialog.askdirectory(
        title="Selecione a pasta com os arquivos TXT/PDF",
        initialdir=os.path.expanduser("~")
    )

    root.destroy()
    return folder_path


def process_files(folder_path, enable_nlp=False, nlp_config=None):
    """
    Escaneia, lê e processa todos os arquivos TXT e PDF, retornando uma lista de documentos.
    """
    print(f"\n🔍 Escaneando pasta: {folder_path}")
    files_found = scan_directory(folder_path)

    if not files_found:
        print("⚠️  Nenhum arquivo TXT ou PDF encontrado!")
        return []

    print(f"✅ Encontrados {len(files_found)} arquivo(s)")

    documents = []
    print("\n📄 Processando arquivos...")
    for idx, file_info in enumerate(files_found, 1):
        file_path = file_info['path']
        relative_path = file_info['relative_path']
        print(f"  [{idx}/{len(files_found)}] {relative_path}", end=" ... ")

        try:
            content = ""
            if file_info['type'] == 'txt':
                content = read_txt_file(file_path)
            elif file_info['type'] == 'pdf':
                content = read_pdf_file(file_path)
            else:
                print("❌ Tipo não suportado")
                continue

            document = {
                "id": f"doc_{idx:04d}",
                "filename": os.path.basename(file_path),
                "relative_path": relative_path,
                "type": file_info['type'],
                "size_bytes": os.path.getsize(file_path),
                "modified_date": datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat(),
                "content": content,
                "char_count": len(content),
                "word_count": len(content.split())
            }
            documents.append(document)
            print("✅")

        except Exception as e:
            print(f"❌ Erro: {str(e)}")
            continue

    if enable_nlp and NLP_AVAILABLE and documents:
        print("\n" + "=" * 60)
        print("  🧠 INICIANDO ANÁLISE NLP AVANÇADA")
        print("=" * 60)
        try:
            processor = LegalNLPProcessor(nlp_config)
            documents = processor.process_batch(documents)
            print("✅ Análise NLP concluída com sucesso")
        except Exception as e:
            print(f"⚠ Erro na análise NLP: {str(e)}")

    return documents


def save_json(data, output_path):
    """Salva os dados em arquivo JSON"""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"❌ Erro ao salvar JSON: {str(e)}")
        return False


def save_multiple_json_files(data_list, base_output_path):
    """Salva múltiplos arquivos JSON quando os dados foram divididos"""
    saved_files = []
    total_parts = len(data_list)

    if total_parts == 1:
        if save_json(data_list[0], base_output_path):
            saved_files.append(base_output_path)
        return saved_files

    base_dir = os.path.dirname(base_output_path)
    base_name, ext = os.path.splitext(os.path.basename(base_output_path))

    print(f"\n💾 Salvando {total_parts} arquivos JSON...")
    for i, data_part in enumerate(data_list, 1):
        part_filename = f"{base_name}_parte_{i}_de_{total_parts}{ext}"
        part_path = os.path.join(base_dir, part_filename)

        print(f"   Salvando parte {i}/{total_parts}...", end=" ")
        if save_json(data_part, part_path):
            saved_files.append(part_path)
            file_size_mb = os.path.getsize(part_path) / (1024 * 1024)
            print(f"✅ ({file_size_mb:.2f} MB)")
        else:
            print("❌ Falha")

    return saved_files


def ask_max_json_size():
    """Pergunta ao usuário o tamanho máximo para cada arquivo JSON"""
    print("\n" + "=" * 60)
    print("⚙️  CONFIGURAÇÃO DE TAMANHO DOS ARQUIVOS JSON")
    print("=" * 60)
    print("\n📏 Informe o tamanho máximo para cada arquivo JSON (Recomendado: 50 MB).")

    while True:
        try:
            user_input = input("\n💾 Tamanho máximo por arquivo (MB) [padrão: 50]: ").strip()
            if not user_input:
                return 50

            max_size = int(user_input)
            if max_size >= 1:
                return max_size
            else:
                print("❌ O tamanho deve ser no mínimo 1 MB.")
        except ValueError:
            print("❌ Por favor, digite um número válido.")
        except KeyboardInterrupt:
            print("\n\n⚠️  Operação cancelada.")
            sys.exit(0)


def ask_nlp_processing():
    """Pergunta ao usuário se deseja processar com NLP"""
    if not NLP_AVAILABLE:
        return False, None

    print("\n" + "=" * 60)
    print("⚙️  CONFIGURAÇÃO DE PROCESSAMENTO NLP")
    print("=" * 60)
    print("\n🧠 Deseja aplicar análise NLP avançada?")
    print("   (Extração de entidades, Sumarização, etc.)")
    print("⚠ ATENÇÃO: O processamento NLP pode levar mais tempo.")

    while True:
        response = input("\n🔹 Ativar NLP? (s/n) [padrão: s]: ").strip().lower()
        if not response or response in ['s', 'sim']:
            print("\n📊 Escolha o modo de processamento:")
            print("   1. RÁPIDO   - Apenas NER")
            print("   2. PADRÃO   - NER + Sumarização (recomendado)")
            print("   3. COMPLETO - NER + Sumarização + Embeddings")

            mode_input = input("\n🔹 Escolha o modo (1/2/3) [padrão: 2]: ").strip()
            mode_map = {'1': 'fast', '3': 'full'}
            return True, mode_map.get(mode_input, 'standard')

        elif response in ['n', 'nao', 'não']:
            return False, None
        else:
            print("❌ Resposta inválida. Digite 's' ou 'n'.")


def main():
    """Função principal do programa"""
    print("=" * 60)
    print("  🧠 SISTEMA DE IA JURÍDICA - ESTRATEGISTA COGNITIVO v2.0")
    print("  Conversor TXT/PDF → JSON + Análise NLP")
    print("=" * 60)

    folder_path = select_folder()
    if not folder_path or not os.path.isdir(folder_path):
        print("\n❌ Nenhuma pasta válida selecionada. Encerrando...")
        sys.exit(1)

    enable_nlp, config_mode = ask_nlp_processing()
    nlp_config = get_config(config_mode) if enable_nlp else None
    max_size_mb = ask_max_json_size()

    documents = process_files(folder_path, enable_nlp, nlp_config)

    if not documents:
        print("\n⚠️  Nenhum documento foi processado com sucesso.")
        sys.exit(1)

    metadata = {
        "source_directory": str(folder_path),
        "nlp_enabled": enable_nlp
    }
    knowledge_base = generate_knowledge_base_json(documents, metadata)

    folder_name = os.path.basename(folder_path.rstrip(os.sep))
    output_filename = f"knowledge_base_{folder_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_filename)

    print(f"\n🔍 Verificando tamanho do JSON...")
    json_parts = split_large_json(knowledge_base, max_size_mb)

    if len(json_parts) > 1:
        print(f"⚠️  O arquivo será dividido em {len(json_parts)} partes para respeitar o limite de {max_size_mb} MB")

    saved_files = save_multiple_json_files(json_parts, output_path)

    if saved_files:
        print(f"\n✅ {len(saved_files)} arquivo(s) salvo(s) com sucesso!")

        stats = knowledge_base.get("statistics", {})
        print(f"\n📊 ESTATÍSTICAS GERAIS:")
        print(f"   📄 Total de documentos: {stats.get('total_documents', 0)}")
        print(f"   📝 Total de caracteres: {stats.get('total_characters', 0):,}")
        print(f"   🔤 Total de palavras: {stats.get('total_words', 0):,}")

        print(f"\n📁 ARQUIVO(S) GERADO(S):")
        total_size_mb = sum(os.path.getsize(f) for f in saved_files) / (1024 * 1024)
        for file_path in saved_files:
            print(f"   • {os.path.basename(file_path)} ({os.path.getsize(file_path) / (1024 * 1024):.2f} MB)")
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
