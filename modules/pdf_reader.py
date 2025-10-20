"""
Módulo para leitura de arquivos PDF
"""

try:
    from pypdf import PdfReader
except ImportError:
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        PdfReader = None


def read_pdf_file(file_path):
    """
    Lê o conteúdo de um arquivo PDF

    Args:
        file_path: Caminho do arquivo PDF

    Returns:
        str: Conteúdo extraído do PDF

    Raises:
        Exception: Se houver erro na leitura do arquivo
    """
    if PdfReader is None:
        raise Exception(
            "Biblioteca PyPDF não instalada. "
            "Instale com: pip install pypdf"
        )

    try:
        reader = PdfReader(file_path)

        # Extrai texto de todas as páginas
        text_parts = []

        for page_num, page in enumerate(reader.pages, 1):
            try:
                text = page.extract_text()
                if text.strip():
                    # Adiciona separador de página para contexto
                    text_parts.append(f"--- Página {page_num} ---\n{text}")
            except Exception as e:
                # Se falhar em uma página, continua com as outras
                text_parts.append(f"--- Página {page_num} ---\n[Erro ao extrair texto: {str(e)}]")

        content = "\n\n".join(text_parts)
        return content.strip()

    except Exception as e:
        raise Exception(f"Erro ao ler PDF: {str(e)}")


def read_pdf_file_with_metadata(file_path):
    """
    Lê arquivo PDF e retorna conteúdo com metadados detalhados

    Args:
        file_path: Caminho do arquivo PDF

    Returns:
        dict: Dicionário com conteúdo e metadados
    """
    if PdfReader is None:
        raise Exception("Biblioteca PyPDF não instalada")

    try:
        reader = PdfReader(file_path)
        content = read_pdf_file(file_path)

        # Extrai metadados do PDF
        metadata = reader.metadata if reader.metadata else {}

        return {
            'content': content,
            'pages': len(reader.pages),
            'characters': len(content),
            'words': len(content.split()),
            'metadata': {
                'title': metadata.get('/Title', ''),
                'author': metadata.get('/Author', ''),
                'subject': metadata.get('/Subject', ''),
                'creator': metadata.get('/Creator', ''),
                'producer': metadata.get('/Producer', ''),
                'creation_date': str(metadata.get('/CreationDate', '')),
                'modification_date': str(metadata.get('/ModDate', ''))
            }
        }

    except Exception as e:
        raise Exception(f"Erro ao processar PDF: {str(e)}")


def extract_pdf_structure(file_path):
    """
    Extrai estrutura do PDF (útil para PDFs com índices/capítulos)

    Args:
        file_path: Caminho do arquivo PDF

    Returns:
        dict: Estrutura do documento
    """
    if PdfReader is None:
        raise Exception("Biblioteca PyPDF não instalada")

    try:
        reader = PdfReader(file_path)

        structure = {
            'pages': len(reader.pages),
            'outline': []
        }

        # Tenta extrair outline/bookmarks se existirem
        if hasattr(reader, 'outline') and reader.outline:
            try:
                structure['outline'] = _parse_outline(reader.outline)
            except Exception:
                pass

        return structure

    except Exception as e:
        raise Exception(f"Erro ao extrair estrutura do PDF: {str(e)}")


def _parse_outline(outline, level=0):
    """
    Parser recursivo para outline do PDF

    Args:
        outline: Objeto outline do PyPDF
        level: Nível de profundidade

    Returns:
        list: Lista de itens do outline
    """
    items = []

    for item in outline:
        if isinstance(item, list):
            items.extend(_parse_outline(item, level + 1))
        else:
            try:
                items.append({
                    'title': item.get('/Title', 'Untitled'),
                    'level': level
                })
            except Exception:
                continue

    return items
