"""
Módulo para leitura de arquivos TXT
"""

import chardet


def detect_encoding(file_path):
    """
    Detecta a codificação de um arquivo

    Args:
        file_path: Caminho do arquivo

    Returns:
        str: Nome da codificação detectada
    """
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            return result['encoding'] or 'utf-8'
    except Exception:
        return 'utf-8'


def read_txt_file(file_path):
    """
    Lê o conteúdo de um arquivo TXT com detecção automática de encoding

    Args:
        file_path: Caminho do arquivo TXT

    Returns:
        str: Conteúdo do arquivo

    Raises:
        Exception: Se houver erro na leitura do arquivo
    """
    # Tenta múltiplos encodings comuns
    encodings_to_try = [
        'utf-8',
        'utf-8-sig',  # UTF-8 com BOM
        'latin-1',
        'cp1252',  # Windows encoding
        'iso-8859-1',
    ]

    # Primeiro tenta detectar o encoding
    detected_encoding = detect_encoding(file_path)
    if detected_encoding and detected_encoding not in encodings_to_try:
        encodings_to_try.insert(0, detected_encoding)

    # Tenta ler com cada encoding
    last_error = None
    for encoding in encodings_to_try:
        try:
            with open(file_path, 'r', encoding=encoding, errors='strict') as f:
                content = f.read()
                # Remove BOM se presente
                if content.startswith('\ufeff'):
                    content = content[1:]
                return content.strip()
        except (UnicodeDecodeError, LookupError) as e:
            last_error = e
            continue

    # Se todas as tentativas falharem, tenta com errors='replace'
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
            if content.startswith('\ufeff'):
                content = content[1:]
            return content.strip()
    except Exception as e:
        raise Exception(f"Não foi possível ler o arquivo TXT: {str(e)}") from last_error


def read_txt_file_with_metadata(file_path):
    """
    Lê arquivo TXT e retorna conteúdo com metadados

    Args:
        file_path: Caminho do arquivo

    Returns:
        dict: Dicionário com conteúdo e metadados
    """
    content = read_txt_file(file_path)
    encoding = detect_encoding(file_path)

    return {
        'content': content,
        'encoding': encoding,
        'lines': len(content.split('\n')),
        'characters': len(content),
        'words': len(content.split())
    }
