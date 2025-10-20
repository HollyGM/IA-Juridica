"""
Módulo para gerar um relatório HTML dos resultados do processamento.
"""
import os
from datetime import datetime

def generate_html_report(knowledge_base, saved_files, output_directory):
    """
    Gera um relatório HTML com as estatísticas e resultados do processamento.

    Args:
        knowledge_base (dict): A base de conhecimento completa com metadados e documentos.
        saved_files (list): Lista dos caminhos dos arquivos JSON salvos.
        output_directory (str): O diretório onde o relatório será salvo.
    """
    stats = knowledge_base.get("statistics", {})
    metadata = knowledge_base.get("metadata", {})
    documents = knowledge_base.get("documents", [])

    # Processa a lista de arquivos para extrair apenas o nome
    saved_filenames = [os.path.basename(f) for f in saved_files]

    # Monta o conteúdo HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF--8">
        <title>Relatório de Processamento</title>
        <style>
            body {{ font-family: sans-serif; margin: 2em; }}
            h1, h2 {{ color: #333; }}
            .summary {{ background-color: #f4f4f4; padding: 1em; border-radius: 8px; }}
            .file-list {{ list-style-type: none; padding: 0; }}
            .file-list li {{ background-color: #e9e9e9; margin: 0.5em 0; padding: 0.5em; border-radius: 4px; }}
        </style>
    </head>
    <body>
        <h1>Relatório de Processamento de Documentos</h1>
        <p>Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

        <div class="summary">
            <h2>Resumo</h2>
            <p><strong>Pasta de Origem:</strong> {metadata.get('source_directory', 'N/A')}</p>
            <p><strong>Total de Documentos Processados:</strong> {stats.get('total_documents', 0)}</p>
            <p><strong>Total de Palavras:</strong> {stats.get('total_words', 0):,}</p>
        </div>

        <h2>Arquivos JSON Gerados</h2>
        <ul class="file-list">
            {''.join(f"<li>{name}</li>" for name in saved_filenames)}
        </ul>

        <h2>Documentos Processados</h2>
        <table>
            <thead>
                <tr>
                    <th>Nome do Arquivo</th>
                    <th>Tipo</th>
                    <th>Tamanho (bytes)</th>
                </tr>
            </thead>
            <tbody>
                {''.join(f"<tr><td>{doc['filename']}</td><td>{doc['type']}</td><td>{doc['size_bytes']:,}</td></tr>" for doc in documents)}
            </tbody>
        </table>
    </body>
    </html>
    """

    # Salva o arquivo HTML
    report_path = os.path.join(output_directory, f"relatorio_{datetime.now():%Y%m%d_%H%M%S}.html")
    try:
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Relatório HTML gerado com sucesso em: {report_path}")
    except Exception as e:
        print(f"Erro ao gerar o relatório HTML: {e}")
