"""
Módulo para leitura de arquivos DOCX
"""
try:
    import docx
except ImportError:
    docx = None

def read_docx_file(file_path):
    """
    Lê o conteúdo de um arquivo DOCX.

    Args:
        file_path: Caminho do arquivo DOCX.

    Returns:
        str: Conteúdo extraído do DOCX.

    Raises:
        Exception: Se houver erro na leitura do arquivo ou a biblioteca não estiver instalada.
    """
    if docx is None:
        raise ImportError(
            "A biblioteca 'python-docx' não está instalada. "
            "Instale com: pip install python-docx"
        )

    try:
        doc = docx.Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text).strip()
    except Exception as e:
        raise Exception(f"Erro ao ler o arquivo DOCX: {str(e)}")
