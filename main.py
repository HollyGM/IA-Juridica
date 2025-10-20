#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de IA Jurídica - Estrategista Jurídico-Cognitivo
Conversor de TXT/PDF para JSON com análise NLP avançada
Versão 3.0 - Com Logs, Relatórios e Suporte a DOCX

Autor: Desenvolvido com Claude
"""

import os
import sys
import json
import argparse
import logging
from pathlib import Path
from datetime import datetime
from tkinter import Tk, filedialog

# --- Configuração do Logging ---
log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] - %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("processing.log", encoding='utf-8')
file_handler.setFormatter(log_formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_formatter)
logger.addHandler(console_handler)

# --- Imports dos Módulos ---
from modules.file_scanner import scan_directory
from modules.txt_reader import read_txt_file
from modules.pdf_reader import read_pdf_file
from modules.docx_reader import read_docx_file
from modules.json_generator import generate_knowledge_base_json, split_large_json
from modules.report_generator import generate_html_report

try:
    from modules.nlp_processor import LegalNLPProcessor
    NLP_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Módulos NLP não disponíveis: {e}")
    NLP_AVAILABLE = False

try:
    from config import get_config
except ImportError:
    logging.warning("Arquivo de configuração não encontrado. Usando configurações padrão.")
    def get_config(mode='standard'):
        return {'enable_ner': True, 'enable_summarization': True, 'enable_embeddings': False}

def select_folder():
    """Abre diálogo para seleção de pasta"""
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    folder_path = filedialog.askdirectory(
        title="Selecione a pasta com os arquivos",
        initialdir=os.path.expanduser("~")
    )
    root.destroy()
    return folder_path

def process_files(folder_path, nlp_config=None):
    """Escaneia, lê e processa todos os arquivos, retornando uma lista de documentos."""
    logging.info(f"Escaneando pasta: {folder_path}")
    files_found = scan_directory(folder_path)

    if not files_found:
        logging.warning("Nenhum arquivo compatível encontrado!")
        return []

    logging.info(f"Encontrados {len(files_found)} arquivo(s)")
    documents = []

    for idx, file_info in enumerate(files_found, 1):
        relative_path = file_info['relative_path']
        logging.info(f"Processando [{idx}/{len(files_found)}]: {relative_path}")
        try:
            content = ""
            if file_info['type'] == 'txt':
                content = read_txt_file(file_info['path'])
            elif file_info['type'] == 'pdf':
                content = read_pdf_file(file_info['path'])
            elif file_info['type'] == 'docx':
                content = read_docx_file(file_info['path'])
            else:
                logging.warning(f"Tipo de arquivo não suportado: {relative_path}")
                continue

            documents.append({
                "id": f"doc_{idx:04d}", "filename": os.path.basename(file_info['path']),
                "relative_path": relative_path, "type": file_info['type'],
                "size_bytes": os.path.getsize(file_info['path']),
                "modified_date": datetime.fromtimestamp(os.path.getmtime(file_info['path'])).isoformat(),
                "content": content, "char_count": len(content), "word_count": len(content.split())
            })
        except Exception as e:
            logging.error(f"Erro ao processar o arquivo {relative_path}: {e}")
            continue

    if nlp_config and NLP_AVAILABLE and documents:
        logging.info("Iniciando análise NLP avançada...")
        try:
            processor = LegalNLPProcessor(nlp_config)
            documents = processor.process_batch(documents)
            logging.info("Análise NLP concluída com sucesso.")
        except Exception as e:
            logging.error(f"Erro na análise NLP: {e}")

    return documents

def save_multiple_json_files(data_list, base_output_path):
    """Salva múltiplos arquivos JSON"""
    saved_files = []
    total_parts = len(data_list)
    if total_parts == 1:
        if save_json(data_list[0], base_output_path):
            saved_files.append(base_output_path)
        return saved_files

    base_dir, base_filename = os.path.split(base_output_path)
    base_name, ext = os.path.splitext(base_filename)

    logging.info(f"Salvando {total_parts} arquivos JSON...")
    for i, data_part in enumerate(data_list, 1):
        part_filename = f"{base_name}_parte_{i}_de_{total_parts}{ext}"
        part_path = os.path.join(base_dir, part_filename)
        if save_json(data_part, part_path):
            saved_files.append(part_path)
    return saved_files

def save_json(data, output_path):
    """Salva os dados em arquivo JSON"""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logging.info(f"Salvo com sucesso: {output_path} ({os.path.getsize(output_path) / (1024*1024):.2f} MB)")
        return True
    except Exception as e:
        logging.error(f"Erro ao salvar JSON em {output_path}: {e}")
        return False

def main():
    if sys.platform == 'win32':
        try:
            os.system('chcp 65001 > nul 2>&1')
        except Exception as e:
            logging.warning(f"Não foi possível definir o encoding do console para UTF-8: {e}")

    parser = argparse.ArgumentParser(description="Sistema de IA Jurídica - Processador de Documentos")
    parser.add_argument("-p", "--pasta", help="Caminho para a pasta de documentos.")
    parser.add_argument("-n", "--nlp", choices=['nenhum', 'rapido', 'padrao', 'completo'], default='nenhum', help="Modo de processamento NLP.")
    parser.add_argument("-t", "--tamanho-max", type=int, default=50, help="Tamanho máximo de cada JSON em MB.")
    args = parser.parse_args()

    logging.info("=" * 60)
    logging.info("  🧠 SISTEMA DE IA JURÍDICA - ESTRATEGISTA COGNITIVO v3.0")
    logging.info("=" * 60)

    if args.pasta:
        folder_path = args.pasta
        enable_nlp = args.nlp != 'nenhum'
        config_mode_map = {'rapido': 'fast', 'padrao': 'standard', 'completo': 'full'}
        config_mode = config_mode_map.get(args.nlp)
        max_size_mb = args.tamanho_max
    else:
        folder_path = select_folder()
        if not folder_path: sys.exit(logging.critical("Nenhuma pasta selecionada. Encerrando."))

        enable_nlp, config_mode = ask_nlp_processing()
        max_size_mb = ask_max_json_size()

    nlp_config = get_config(config_mode) if enable_nlp else None
    documents = process_files(folder_path, nlp_config)

    if not documents:
        sys.exit(logging.critical("Nenhum documento foi processado com sucesso."))

    metadata = {"source_directory": str(folder_path), "nlp_enabled": enable_nlp}
    knowledge_base = generate_knowledge_base_json(documents, metadata)

    output_dir = os.getcwd()
    output_filename = f"knowledge_base_{Path(folder_path).name}_{datetime.now():%Y%m%d_%H%M%S}.json"
    output_path = os.path.join(output_dir, output_filename)

    json_parts = split_large_json(knowledge_base, max_size_mb)
    saved_files = save_multiple_json_files(json_parts, output_path)

    if not saved_files:
        sys.exit(logging.critical("Falha ao salvar os arquivos."))

    generate_html_report(knowledge_base, saved_files, output_dir)

    logging.info("=" * 60)
    logging.info("🎉 Processo concluído com sucesso!")
    logging.info(f"Para detalhes, veja o arquivo de log: {os.path.join(os.getcwd(), 'processing.log')}")
    logging.info("=" * 60)

def ask_max_json_size():
    print("\n" + "=" * 60 + "\n⚙️  CONFIGURAÇÃO DE TAMANHO DOS ARQUIVOS JSON\n" + "=" * 60)
    print("\n📏 Informe o tamanho máximo para cada arquivo JSON (Recomendado: 50 MB).")
    while True:
        try:
            user_input = input("\n💾 Tamanho máximo por arquivo (MB) [padrão: 50]: ").strip()
            return int(user_input) if user_input else 50
        except ValueError:
            print("❌ Por favor, digite um número válido.")
        except KeyboardInterrupt:
            print("\n\n⚠️  Operação cancelada.")
            sys.exit(0)

def ask_nlp_processing():
    if not NLP_AVAILABLE: return False, None
    print("\n" + "=" * 60 + "\n⚙️  CONFIGURAÇÃO DE PROCESSAMENTO NLP\n" + "=" * 60)
    print("\n🧠 Deseja aplicar análise NLP avançada?")
    while True:
        response = input("\n🔹 Ativar NLP? (s/n) [padrão: s]: ").strip().lower()
        if not response or response in ['s', 'sim']:
            print("\n📊 Modos: 1. RÁPIDO 2. PADRÃO 3. COMPLETO")
            mode_input = input("🔹 Escolha o modo (1/2/3) [padrão: 2]: ").strip()
            return True, {'1': 'fast', '3': 'full'}.get(mode_input, 'standard')
        elif response in ['n', 'nao', 'não']:
            return False, None
        else:
            print("❌ Resposta inválida.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(logging.warning("\nOperação cancelada pelo usuário."))
    except Exception as e:
        logging.critical(f"Erro inesperado: {e}", exc_info=True)
        sys.exit(1)
