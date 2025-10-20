"""
Módulo para escanear diretórios e encontrar arquivos TXT e PDF
"""

import os
from pathlib import Path


def scan_directory(root_path, extensions=None):
    """
    Escaneia um diretório recursivamente buscando arquivos com extensões específicas

    Args:
        root_path: Caminho raiz para iniciar a busca
        extensions: Lista de extensões a buscar (padrão: ['.txt', '.pdf'])

    Returns:
        list: Lista de dicionários com informações dos arquivos encontrados
    """
    if extensions is None:
        extensions = ['.txt', '.pdf']

    # Normaliza extensões para lowercase
    extensions = [ext.lower() if ext.startswith('.') else f'.{ext.lower()}'
                  for ext in extensions]

    files_found = []
    root_path = Path(root_path)

    # Percorre recursivamente todos os arquivos
    for file_path in root_path.rglob('*'):
        if file_path.is_file():
            file_ext = file_path.suffix.lower()

            if file_ext in extensions:
                # Calcula o caminho relativo à pasta raiz
                relative_path = file_path.relative_to(root_path)

                file_info = {
                    'path': str(file_path),
                    'relative_path': str(relative_path),
                    'filename': file_path.name,
                    'type': file_ext[1:],  # Remove o ponto da extensão
                    'size': file_path.stat().st_size,
                    'directory': str(file_path.parent.relative_to(root_path))
                }

                files_found.append(file_info)

    # Ordena por caminho relativo para manter organização
    files_found.sort(key=lambda x: x['relative_path'])

    return files_found


def get_directory_structure(root_path):
    """
    Retorna a estrutura de diretórios de forma hierárquica

    Args:
        root_path: Caminho raiz

    Returns:
        dict: Estrutura hierárquica de diretórios
    """
    root_path = Path(root_path)
    structure = {
        'name': root_path.name,
        'path': str(root_path),
        'type': 'directory',
        'children': []
    }

    def build_tree(path, parent_dict):
        try:
            items = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name))

            for item in items:
                if item.is_dir():
                    dir_dict = {
                        'name': item.name,
                        'path': str(item),
                        'type': 'directory',
                        'children': []
                    }
                    parent_dict['children'].append(dir_dict)
                    build_tree(item, dir_dict)
                elif item.suffix.lower() in ['.txt', '.pdf']:
                    file_dict = {
                        'name': item.name,
                        'path': str(item),
                        'type': 'file',
                        'extension': item.suffix[1:].lower()
                    }
                    parent_dict['children'].append(file_dict)
        except PermissionError:
            pass  # Ignora diretórios sem permissão

    build_tree(root_path, structure)
    return structure
